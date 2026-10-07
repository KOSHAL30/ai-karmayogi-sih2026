# ==============================================================================
# AI KARMAYOGI — ASSESSMENT SERVICE
# Adaptive Assessment Orchestration, 2PL IRT Item Sequencing, and Diagnostic Evaluation
# ==============================================================================

import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from fastapi import HTTPException, status

from repositories.assessment_repository import AssessmentRepository
from repositories.competency_repository import CompetencyRepository
from repositories.user_repository import UserRepository
from services.scoring_engine import ScoringEngine
from app.models.entities import _to_obj, _to_dict

class AssessmentService:
    def __init__(self, db):
        self.db = db
        self.assess_repo = AssessmentRepository(db)
        self.comp_repo = CompetencyRepository(db)
        self.user_repo = UserRepository(db)

    async def start_assessment(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Starts or resumes an adaptive diagnostic assessment for the user.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        # 1. Resolve Work Role & Competencies
        work_role_id = user.work_role_id
        competencies = []
        if work_role_id:
            competencies = list(await self.comp_repo.list_by_work_role(work_role_id))
        if not competencies:
            competencies = list(await self.comp_repo.list_all())

        if not competencies:
            raise HTTPException(status_code=500, detail="No FRAC competencies configured in the system.")

        # 2. Fetch or create Diagnostic Quiz container
        quiz = await self.assess_repo.get_diagnostic_quiz()
        if not quiz:
            quiz = {
                "_id": str(uuid.uuid4()),
                "created_by": str(user.id),
                "title": "Mission Karmayogi Role-Based Competency Diagnostic",
                "quiz_type": "DIAGNOSTIC",
                "passing_percentage": 60,
                "status": "PUBLISHED"
            }
            await self.db["quizzes"].insert_one(quiz)
            quiz = await self.assess_repo.get_diagnostic_quiz()

        # 3. Check for an ongoing active attempt (within 24 hours)
        latest_attempt = await self.assess_repo.get_latest_attempt(user.id)
        if latest_attempt and hasattr(latest_attempt, "answer_log"):
            latest_attempt.answer_log = _to_dict(latest_attempt.answer_log)
        if latest_attempt and latest_attempt.answer_log.get("status") == "IN_PROGRESS":
            # Resume existing attempt
            attempt = latest_attempt
            responses = attempt.answer_log.get("responses", [])
            current_q_id = attempt.answer_log.get("current_question_id")
            question = None
            if current_q_id:
                question = await self.assess_repo.get_question_by_id(uuid.UUID(current_q_id))
            if not question:
                question = await self._select_next_question(
                    attempt.answer_log.get("current_theta", 0.0),
                    responses,
                    competencies
                )
                attempt.answer_log["current_question_id"] = str(question.id) if question else None
                await self.assess_repo.update_attempt(str(attempt.id), {"answer_log": _to_dict(attempt.answer_log)})
        else:
            # 4. Create fresh attempt
            first_question = await self._select_next_question(0.0, [], competencies)
            if not first_question:
                raise HTTPException(status_code=500, detail="No assessment questions available.")

            attempt_id = str(uuid.uuid4())
            attempt_data = {
                "_id": attempt_id,
                "user_id": str(user.id),
                "quiz_id": str(quiz.id),
                "score_achieved": 0,
                "total_questions": 0,
                "is_passed": False,
                "time_taken_seconds": 0,
                "answer_log": {
                    "status": "IN_PROGRESS",
                    "current_theta": 0.0,
                    "responses": [],
                    "current_question_id": str(first_question.id),
                    "started_at": datetime.now(timezone.utc).isoformat(),
                },
                "attempted_at": datetime.now(timezone.utc).isoformat()
            }
            await self.db["quiz_attempts"].insert_one(attempt_data)
            attempt = await self.assess_repo.get_attempt_by_id(attempt_id)
            if attempt and hasattr(attempt, "answer_log"):
                attempt.answer_log = _to_dict(attempt.answer_log)
            question = first_question

        comp_dict_list = [
            {
                "id": str(c.id),
                "competency_code": c.competency_code,
                "competency_name": c.competency_name,
                "competency_type": c.competency_type,
                "mandated_level": c.mandated_level,
                "description": c.description,
            }
            for c in competencies
        ]

        return {
            "attempt_id": attempt.id,
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "question": self._serialize_question(question),
            "current_question_index": len(attempt.answer_log.get("responses", [])) + 1,
            "max_questions": 15,
            "min_questions": 10,
            "competencies": comp_dict_list,
            "timer_minutes": 20,
        }

    async def process_answer(
        self,
        user_id: uuid.UUID,
        attempt_id: uuid.UUID,
        question_id: uuid.UUID,
        selected_option_index: int,
        time_spent_seconds: int = 15
    ) -> Dict[str, Any]:
        """
        Evaluates submitted answer, updates IRT theta, and adaptively chooses the next question.
        """
        attempt = await self.assess_repo.get_attempt_by_id(attempt_id)
        if attempt and hasattr(attempt, "answer_log"):
            attempt.answer_log = _to_dict(attempt.answer_log)
        if not attempt or attempt.user_id != str(user_id):
            raise HTTPException(status_code=404, detail="Assessment attempt not found.")

        if attempt.answer_log.get("status") != "IN_PROGRESS":
            raise HTTPException(status_code=400, detail="Assessment has already been completed.")

        question = await self.assess_repo.get_question_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found.")

        is_correct = (selected_option_index == question.correct_option_index)

        # 1. Append response
        responses = attempt.answer_log.setdefault("responses", [])
        response_record = {
            "question_id": str(question.id),
            "competency_id": str(question.competency_id) if question.competency_id else "",
            "bloom_level": question.bloom_level,
            "selected_index": selected_option_index,
            "correct_index": question.correct_option_index,
            "is_correct": is_correct,
            "time_spent_seconds": time_spent_seconds,
            "source_citation": question.source_citation,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        responses.append(response_record)

        # 2. Update latent ability theta
        current_theta = ScoringEngine.estimate_theta(
            attempt.answer_log.get("current_theta", 0.0),
            responses
        )
        attempt.answer_log["current_theta"] = current_theta

        # 3. Check stopping condition (15 max, or >= 10 with sufficient precision)
        total_answered = len(responses)
        is_completed = total_answered >= 15

        next_question = None
        if not is_completed:
            # Resolve user's competencies
            user = await self.user_repo.get_by_id(user_id)
            competencies = []
            if user and user.work_role_id:
                competencies = list(await self.comp_repo.list_by_work_role(user.work_role_id))
            if not competencies:
                competencies = list(await self.comp_repo.list_all())

            next_question = await self._select_next_question(current_theta, responses, competencies)
            if not next_question:
                # No more unique questions available
                is_completed = True

        if next_question:
            attempt.answer_log["current_question_id"] = str(next_question.id)
        else:
            attempt.answer_log["current_question_id"] = None

        await self.assess_repo.update_attempt(str(attempt.id), {"answer_log": _to_dict(attempt.answer_log)})

        return {
            "attempt_id": attempt.id,
            "is_completed": is_completed,
            "current_question_index": total_answered + (0 if is_completed else 1),
            "total_answered": total_answered,
            "max_questions": 15,
            "next_question": self._serialize_question(next_question) if next_question else None,
            "progress_percentage": round((total_answered / 15.0) * 100.0, 1),
        }

    async def submit_assessment(self, user_id: uuid.UUID, attempt_id: uuid.UUID) -> Dict[str, Any]:
        """
        Finalizes the assessment and generates the complete diagnostic dossier.
        """
        attempt = await self.assess_repo.get_attempt_by_id(attempt_id)
        if attempt and hasattr(attempt, "answer_log"):
            attempt.answer_log = _to_dict(attempt.answer_log)
        if not attempt or attempt.user_id != str(user_id):
            raise HTTPException(status_code=404, detail="Assessment attempt not found.")

        user = await self.user_repo.get_by_id(user_id)
        work_role_title = user.work_role.role_title if user and user.work_role else "Civil Services Official"

        # Resolve competencies
        competencies = []
        if user and user.work_role_id:
            competencies = list(await self.comp_repo.list_by_work_role(user.work_role_id))
        if not competencies:
            competencies = list(await self.comp_repo.list_all())

        comp_dict_list = [
            {
                "id": str(c.id),
                "competency_code": c.competency_code,
                "competency_name": c.competency_name,
                "competency_type": c.competency_type,
                "mandated_level": c.mandated_level,
                "description": c.description,
            }
            for c in competencies
        ]

        responses = attempt.answer_log.get("responses", [])

        # Run Scoring Engine
        evaluation = ScoringEngine.calculate_competency_deficits(
            competencies=comp_dict_list,
            responses=responses,
            work_role=work_role_title
        )

        score_achieved = sum(1 for r in responses if r.get("is_correct"))
        total_questions = len(responses)
        total_time_seconds = sum(r.get("time_spent_seconds", 0) for r in responses)

        attempt.score_achieved = score_achieved
        attempt.total_questions = total_questions
        attempt.is_passed = (evaluation["overall_score"] >= 60.0)
        attempt.time_taken_seconds = total_time_seconds

        attempt.answer_log["status"] = "COMPLETED"
        attempt.answer_log["completed_at"] = datetime.now(timezone.utc).isoformat()
        attempt.answer_log["evaluation"] = evaluation

        await self.assess_repo.update_attempt(str(attempt.id), {"answer_log": _to_dict(attempt.answer_log)})

        return {
            "attempt_id": attempt.id,
            "overall_score": evaluation["overall_score"],
            "overall_status": evaluation["overall_status"],
            "is_passed": attempt.is_passed,
            "total_questions": total_questions,
            "score_achieved": score_achieved,
            "time_taken_seconds": total_time_seconds,
            "evaluation": evaluation,
        }

    async def get_result(self, user_id: uuid.UUID, attempt_id: uuid.UUID) -> Dict[str, Any]:
        """
        Retrieves complete diagnostic result for attempt.
        """
        attempt = await self.assess_repo.get_attempt_by_id(attempt_id)
        if attempt and hasattr(attempt, "answer_log"):
            attempt.answer_log = _to_dict(attempt.answer_log)
        if not attempt or attempt.user_id != str(user_id):
            raise HTTPException(status_code=404, detail="Assessment result not found.")

        if attempt.answer_log.get("status") != "COMPLETED":
            # If not yet finalized, run submission logic automatically and refresh attempt
            await self.submit_assessment(user_id, attempt_id)
            attempt = await self.assess_repo.get_attempt_by_id(attempt_id)
        if attempt and hasattr(attempt, "answer_log"):
            attempt.answer_log = _to_dict(attempt.answer_log)

        user = await self.user_repo.get_by_id(user_id)
        evaluation = attempt.answer_log.get("evaluation", {})

        return {
            "attempt_id": attempt.id,
            "officer_name": user.full_name if user else "Officer",
            "designation": user.designation if user else "Civil Servant",
            "department": user.department.name if user and user.department else "General Administration",
            "work_role": user.work_role.role_title if user and user.work_role else "Civil Services Official",
            "attempted_at": attempt.attempted_at if isinstance(attempt.attempted_at, str) else attempt.attempted_at.isoformat() if attempt.attempted_at else None,
            "time_taken_seconds": attempt.time_taken_seconds,
            "score_achieved": attempt.score_achieved,
            "total_questions": attempt.total_questions,
            "is_passed": attempt.is_passed,
            "overall_score": evaluation.get("overall_score", 0.0),
            "overall_status": evaluation.get("overall_status", "COMPETENT"),
            "behavioral_score": evaluation.get("behavioral_score", 0.0),
            "functional_score": evaluation.get("functional_score", 0.0),
            "domain_score": evaluation.get("domain_score", 0.0),
            "composite_deficit_pct": evaluation.get("composite_deficit_pct", 0.0),
            "competency_results": evaluation.get("competency_results", []),
            "strengths": evaluation.get("strengths", []),
            "weaknesses": evaluation.get("weaknesses", []),
            "recommended_action": evaluation.get("recommended_action", ""),
        }

    async def get_history(self, user_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Lists all assessment attempts for the user.
        """
        attempts = await self.assess_repo.list_attempts_by_user(user_id)
        history = []
        for att in attempts:
            answer_log = _to_dict(att.answer_log) if hasattr(att, "answer_log") else {}
            eval_data = answer_log.get("evaluation", {})
            history.append({
                "attempt_id": att.id,
                "quiz_title": att.quiz.title if att.quiz else "Diagnostic Assessment",
                "attempted_at": att.attempted_at if isinstance(att.attempted_at, str) else att.attempted_at.isoformat() if att.attempted_at else None,
                "status": answer_log.get("status", "IN_PROGRESS"),
                "score_achieved": att.score_achieved,
                "total_questions": att.total_questions,
                "overall_score": eval_data.get("overall_score"),
                "is_passed": att.is_passed,
                "time_taken_seconds": att.time_taken_seconds,
            })
        return history

    async def _select_next_question(
        self,
        current_theta: float,
        responses: List[Dict[str, Any]],
        competencies: List[Any]
    ) -> Optional[Any]:
        """
        Selects next question adaptively based on current theta and competency rotation.
        """
        answered_ids = {uuid.UUID(r["question_id"]) for r in responses if r.get("question_id")}

        comp_ids = [c.id for c in competencies]
        candidate_questions = await self.assess_repo.get_questions_for_competencies(comp_ids)
        unanswered = [q for q in candidate_questions if q.id not in answered_ids]

        if not unanswered:
            # Fallback to any quiz questions
            quiz = await self.assess_repo.get_diagnostic_quiz()
            if quiz:
                all_quiz_q = await self.assess_repo.get_questions_by_quiz(quiz.id)
                unanswered = [q for q in all_quiz_q if q.id not in answered_ids]

        if not unanswered:
            return None

        # Determine target Bloom / difficulty based on current theta
        # theta >= 0.8 -> ANALYZE / EVALUATE
        # -0.8 < theta < 0.8 -> APPLY
        # theta <= -0.8 -> REMEMBER / UNDERSTAND
        if current_theta >= 0.8:
            preferred_blooms = ["ANALYZE", "EVALUATE", "APPLY"]
        elif current_theta <= -0.8:
            preferred_blooms = ["REMEMBER", "UNDERSTAND", "APPLY"]
        else:
            preferred_blooms = ["APPLY", "UNDERSTAND", "ANALYZE"]

        # Sort unanswered questions by matching preferred bloom order
        def sort_key(q: Any):
            bloom = q.bloom_level.upper()
            try:
                rank = preferred_blooms.index(bloom)
            except ValueError:
                rank = 99
            return rank

        unanswered.sort(key=sort_key)
        return unanswered[0]

    def _serialize_question(self, question: Optional[Any]) -> Optional[Dict[str, Any]]:
        if not question:
            return None

        # Parse options from JSONB
        raw_options = question.options
        if isinstance(raw_options, list):
            options = raw_options
        else:
            options = []

        return {
            "id": question.id,
            "question_stem": question.question_stem,
            "bloom_level": question.bloom_level,
            "options": _to_dict(options),
            "competency_name": question.competency.competency_name if question.competency else "General Competency",
            "competency_type": question.competency.competency_type if question.competency else "FUNCTIONAL",
            "source_citation": question.source_citation,
        }

# ==============================================================================
# AI KARMAYOGI — LEARNING PATH & SKILL FORECAST SERVICE
# 4-Week Trajectory Milestones, Predictive Uplift & Telemetry Analytics
# ==============================================================================

import uuid
from typing import Sequence, Optional, Any, List, Dict
from datetime import datetime, timezone
from app.models.entities import _to_obj, _to_list, new_uuid, utcnow
from repositories.recommendation_repository import RecommendationRepository
from repositories.course_repository import CourseRepository
from repositories.assessment_repository import AssessmentRepository
from services.recommendation_service import RecommendationService


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    """Helper to retrieve values from either a dict or a SimpleNamespace."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class LearningPathService:
    def __init__(self, db):
        self.db = db
        if db is not None:
            self.recommendation_repo = RecommendationRepository(db)
            self.course_repo = CourseRepository(db)
            self.assessment_repo = AssessmentRepository(db)
        else:
            self.recommendation_repo = None
            self.course_repo = None
            self.assessment_repo = None
        self.rec_repo = self.recommendation_repo
        self.assess_repo = self.assessment_repo
        self.rec_service = RecommendationService(db)

    async def get_dashboard_summary(self, user_id: uuid.UUID) -> dict:
        """
        Compiles the full AI Recommendation Dashboard:
        - Overall competency score
        - Top 3 critical gaps
        - Recommended learning path roadmap
        - Estimated completion time
        - Learning priority
        - Skill improvement forecast
        - KPI cards
        """
        # Ensure recommendations exist
        recommendations = await self.rec_service.get_or_generate_recommendations(user_id)

        # Get latest assessment for baseline scores
        latest_attempt = await self.assessment_repo.get_latest_completed_attempt(user_id)
        ans_log = getattr(latest_attempt, "answer_log", None) if latest_attempt else None
        if hasattr(ans_log, "__dict__"):
            ans_log = vars(ans_log)
        elif not isinstance(ans_log, dict):
            ans_log = None

        is_cold_start = False
        if ans_log and "overall_competency_score" in ans_log:
            overall_score = float(ans_log["overall_competency_score"])
            comp_scores = ans_log.get("competency_scores", {})
            if hasattr(comp_scores, "__dict__"):
                comp_scores = vars(comp_scores)
        else:
            overall_score = 64.0  # default baseline
            comp_scores = {}
            is_cold_start = True

        # Telemetry metrics
        telemetry = await self.recommendation_repo.get_telemetry_metrics(user_id)

        # Check if recommendations were cold-start/fallback
        any_demo_rec = any(bool(getattr(r, "is_demo", False)) for r in recommendations)
        is_demo_mode = is_cold_start or any_demo_rec or not recommendations

        # Top 3 Critical Gaps
        critical_gaps = []
        if comp_scores:
            sorted_gaps = sorted(
                comp_scores.items(),
                key=lambda x: float(_get_val(x[1], "deficit_pct", 0) or 0),
                reverse=True
            )
            for code, data in sorted_gaps[:3]:
                critical_gaps.append({
                    "competency_code": code,
                    "competency_name": _get_val(data, "competency_name", code),
                    "competency_type": _get_val(data, "competency_type", "FUNCTIONAL"),
                    "mandated_level": _get_val(data, "mandated_level", 4),
                    "demonstrated_level": _get_val(data, "demonstrated_level", 2),
                    "deficit_pct": round(float(_get_val(data, "deficit_pct", 0) or 0), 1),
                    "deficit_score": round(float(_get_val(data, "deficit_score", 0) or 0), 2),
                    "is_demo": False,
                    "data_source": "live",
                })
        else:
            # Cold start top gaps
            critical_gaps = [
                {
                    "competency_code": "COMP-GFR-01",
                    "competency_name": "Public Procurement & GFR 2017 Compliance",
                    "competency_type": "FUNCTIONAL",
                    "mandated_level": 4,
                    "demonstrated_level": 2,
                    "deficit_pct": 50.0,
                    "deficit_score": 2.0,
                    "is_demo": True,
                    "data_source": "demo",
                },
                {
                    "competency_code": "COMP-MOP-01",
                    "competency_name": "Central Secretariat File Management & CSMOP",
                    "competency_type": "FUNCTIONAL",
                    "mandated_level": 4,
                    "demonstrated_level": 2,
                    "deficit_pct": 50.0,
                    "deficit_score": 2.0,
                    "is_demo": True,
                    "data_source": "demo",
                },
                {
                    "competency_code": "COMP-ETH-01",
                    "competency_name": "Ethical Governance & Conflict of Interest",
                    "competency_type": "BEHAVIORAL",
                    "mandated_level": 4,
                    "demonstrated_level": 3,
                    "deficit_pct": 25.0,
                    "deficit_score": 1.0,
                    "is_demo": True,
                    "data_source": "demo",
                }
            ]

        # Categorized Roadmaps
        immediate_courses = [r for r in recommendations if getattr(r, "trajectory_stage", "") == "IMMEDIATE"]
        this_week_courses = [r for r in recommendations if getattr(r, "trajectory_stage", "") == "RECOMMENDED_THIS_WEEK"]
        advanced_courses = [r for r in recommendations if getattr(r, "trajectory_stage", "") == "ADVANCED"]
        enrichment_courses = [r for r in recommendations if getattr(r, "trajectory_stage", "") == "OPTIONAL_ENRICHMENT"]

        # Ensure balanced distribution if any bucket is empty
        if not immediate_courses and recommendations:
            immediate_courses = recommendations[:3]
        if not this_week_courses and len(recommendations) > 3:
            this_week_courses = recommendations[3:7]
        if not advanced_courses and len(recommendations) > 7:
            advanced_courses = recommendations[7:11]
        if not enrichment_courses and len(recommendations) > 11:
            enrichment_courses = recommendations[11:]

        # Estimated total completion time
        total_minutes = sum(
            getattr(r.course, "duration_minutes", 20)
            for r in recommendations
            if getattr(r, "course", None)
        )
        estimated_hours = round(total_minutes / 60.0, 1)

        # Skill Forecast
        forecast = await self.generate_skill_forecast(user_id, recommendations, overall_score, comp_scores, is_demo=is_demo_mode)

        # Acceptance rate: Enrolled or completed / Total recommendations
        enrolled_count = telemetry["total_enrolled"]
        acceptance_rate = round((enrolled_count / max(1, len(recommendations))) * 100, 1)

        return {
            "overall_competency_score": overall_score,
            "top_critical_gaps": critical_gaps,
            "estimated_completion_hours": estimated_hours,
            "total_recommended_modules": len(recommendations),
            "is_demo": is_demo_mode,
            "data_source": "demo" if is_demo_mode else "live",
            "telemetry": {
                "completion_percentage": telemetry["completion_percentage"],
                "hours_learned": telemetry["hours_learned"],
                "completed_modules": telemetry["completed_count"],
                "enrolled_modules": telemetry["total_enrolled"],
                "acceptance_rate": min(100.0, acceptance_rate),
                "gap_reduction_achieved": round(telemetry["completion_percentage"] * 0.42, 1)  # calibrated reduction %
            },
            "roadmaps": {
                "immediate": [self._format_rec(r, is_demo_override=is_demo_mode if getattr(r, "is_demo", None) is None else None) for r in immediate_courses],
                "recommended_this_week": [self._format_rec(r, is_demo_override=is_demo_mode if getattr(r, "is_demo", None) is None else None) for r in this_week_courses],
                "advanced_modules": [self._format_rec(r, is_demo_override=is_demo_mode if getattr(r, "is_demo", None) is None else None) for r in advanced_courses],
                "optional_enrichment": [self._format_rec(r, is_demo_override=is_demo_mode if getattr(r, "is_demo", None) is None else None) for r in enrichment_courses]
            },
            "skill_forecast": forecast
        }

    async def generate_weekly_timeline(self, user_id: uuid.UUID) -> list[dict]:
        """
        Generates structured 4-week learning trajectory milestones.
        """
        recs = await self.rec_service.get_or_generate_recommendations(user_id)
        prog_list = await self.recommendation_repo.get_user_progress_list(user_id)
        completed_course_ids = {
            str(getattr(p, "course_id", ""))
            for p in prog_list
            if getattr(p, "completion_status", "") == "COMPLETED"
        }

        # Check if recommendations are demo / cold-start
        is_demo_path = not recs or any(bool(getattr(r, "is_demo", False)) for r in recs)

        if not recs:
            recs = self.rec_service.get_fallback_recommendations(user_id)
            is_demo_path = True

        import json
        from ai.llm_provider import LLMProvider
        
        latest_attempt = await self.assessment_repo.get_latest_completed_attempt(user_id)
        ans_log = getattr(latest_attempt, "answer_log", None) if latest_attempt else None
        if hasattr(ans_log, "__dict__"): ans_log = vars(ans_log)
        elif not isinstance(ans_log, dict): ans_log = None
        
        gaps_str = "No assessment gaps found."
        if ans_log and "competency_scores" in ans_log:
            comp_scores = ans_log["competency_scores"]
            if hasattr(comp_scores, "__dict__"): comp_scores = vars(comp_scores)
            sorted_gaps = sorted(
                comp_scores.items(),
                key=lambda x: float(_get_val(x[1], "deficit_pct", 0) or 0),
                reverse=True
            )
            gaps_list = []
            for code, data in sorted_gaps[:5]:
                gaps_list.append(f"- {code}: {_get_val(data, 'competency_name', code)} (Deficit: {_get_val(data, 'deficit_pct', 0)}%)")
            gaps_str = "\n".join(gaps_list)

        courses_data = []
        for r in recs:
            c = getattr(r, "course", None)
            if not c: continue
            rec_id = str(getattr(r, "recommendation_id", getattr(c, "id", "")))
            if not rec_id: continue
            courses_data.append({
                "course_id": rec_id,
                "title": str(getattr(c, "title", "")),
                "duration_minutes": getattr(c, "duration_minutes", 30),
                "priority": getattr(r, "trajectory_stage", "OPTIONAL_ENRICHMENT")
            })

        system_prompt = '''You are an expert AI Learning Path Architect for AI Karmayogi.
Your task is to organize a given list of recommended courses and a user's critical skill gaps into a structured 4-week learning timeline.
You MUST output ONLY a valid JSON array of exactly 4 objects (one for each week). No markdown formatting, no code blocks, no other text.
The JSON array must strictly follow this schema:
[
  {
    "week_number": 1,
    "title": "String (e.g. 'Week 1: Core Foundation')",
    "focus": "String (e.g. 'Resolve deficit in Rule 149')",
    "micro_learning_focus": "String (e.g. '15-min modules on GFR')",
    "expected_gain": "String (e.g. '+12% Domain Competency Uplift')",
    "practice_quiz": {
      "title": "String",
      "question_count": 5,
      "estimated_minutes": 10
    },
    "course_ids": ["String (exact course_ids from the provided input)"]
  }
]
Constraints:
- You must distribute ALL the provided courses across the 4 weeks logically based on priority and durations.
- High priority courses (IMMEDIATE) should go in week 1.
- Use ONLY the exact `course_id` strings provided in the input. Do NOT invent new course IDs.
'''

        user_prompt = f"User Skill Gaps:\n{gaps_str}\n\nAvailable Courses:\n{json.dumps(courses_data, indent=2)}"

        llm_response = await LLMProvider.generate_response(system_prompt, user_prompt)
        
        parsed_weeks = None
        if llm_response:
            try:
                txt = llm_response.strip()
                if txt.startswith("```json"): txt = txt[7:]
                if txt.startswith("```"): txt = txt[3:]
                if txt.endswith("```"): txt = txt[:-3]
                parsed_weeks = json.loads(txt.strip())
                if not isinstance(parsed_weeks, list) or len(parsed_weeks) != 4:
                    parsed_weeks = None
            except Exception as e:
                import logging
                logging.error(f"Failed to parse Learning Path JSON: {e}")
                parsed_weeks = None

        if parsed_weeks:
            recs_by_id = {}
            for r in recs:
                c = getattr(r, "course", None)
                if c:
                    rid = str(getattr(r, "recommendation_id", getattr(c, "id", "")))
                    if rid: recs_by_id[rid] = r

            # HARDENING VALIDATION
            is_valid = True
            
            week_nums = set()
            for w in parsed_weeks:
                wn = w.get("week_number")
                if isinstance(wn, int):
                    week_nums.add(wn)
                pq = w.get("practice_quiz")
                if not isinstance(pq, dict):
                    is_valid = False
                elif not ("title" in pq and "question_count" in pq and "estimated_minutes" in pq):
                    is_valid = False

            if week_nums != {1, 2, 3, 4}:
                is_valid = False

            assigned_ids = []
            if is_valid:
                for w in parsed_weeks:
                    cids = w.get("course_ids", [])
                    if not isinstance(cids, list):
                        is_valid = False
                        break
                    assigned_ids.extend(cids)
            
            if is_valid:
                if not all(cid in recs_by_id for cid in assigned_ids):
                    is_valid = False
                if is_valid:
                    if set(assigned_ids) != set(recs_by_id.keys()):
                        is_valid = False
                    if len(assigned_ids) != len(recs_by_id.keys()):
                        is_valid = False
            
            if not is_valid:
                parsed_weeks = None

        if parsed_weeks:
            for w in parsed_weeks:
                course_ids = w.pop("course_ids", [])
                w["courses"] = []
                for cid in course_ids:
                    r_obj = recs_by_id[cid]
                    w["courses"].append(self._format_rec(
                        r_obj, 
                        completed_course_ids, 
                        is_demo_override=is_demo_path if getattr(r_obj, "is_demo", None) is None else None
                    ))
                
                pq = w.get("practice_quiz", {})
                pq["is_demo"] = is_demo_path
                pq["data_source"] = "demo" if is_demo_path else "live"
                w["practice_quiz"] = pq
                w["status"] = "IN_PROGRESS" if w.get("week_number") == 1 else "UPCOMING"
                w["is_demo"] = is_demo_path
                w["data_source"] = "demo" if is_demo_path else "live"
            return parsed_weeks

        # Distribute recommendations across 4 weeks
        w1_recs = recs[0:3] if len(recs) >= 3 else recs
        w2_recs = recs[3:6] if len(recs) >= 6 else recs[1:3]
        w3_recs = recs[6:9] if len(recs) >= 9 else recs[2:4]
        w4_recs = recs[9:13] if len(recs) >= 13 else recs[3:5]

        weeks = [
            {
                "week_number": 1,
                "title": "Week 1: Urgent Foundation & Procurement GFR Remediation",
                "focus": "Resolve critical 50% deficit in GFR Rule 149 (GeM) & Rule 166 PAC thresholds.",
                "micro_learning_focus": "15-20 min micro-modules on financial code compliance.",
                "expected_gain": "+12% Functional Competency Uplift",
                "practice_quiz": {
                    "title": "GFR 2017 & GeM Direct Purchase Formative Drill",
                    "question_count": 5,
                    "estimated_minutes": 10,
                    "is_demo": is_demo_path,
                    "data_source": "demo" if is_demo_path else "live"
                },
                "courses": [self._format_rec(r, completed_course_ids, is_demo_override=is_demo_path if getattr(r, "is_demo", None) is None else None) for r in w1_recs],
                "status": "IN_PROGRESS",
                "is_demo": is_demo_path,
                "data_source": "demo" if is_demo_path else "live"
            },
            {
                "week_number": 2,
                "title": "Week 2: Central Secretariat Procedures & CSMOP Compliance",
                "focus": "Elevate e-Office noting, drafting, and 72-hour Parliamentary NFS workflows.",
                "micro_learning_focus": "Operational practice on electronic file movement & DSC validation.",
                "expected_gain": "+15% Operational Speed & File Quality",
                "practice_quiz": {
                    "title": "CSMOP 16th Ed & Parliamentary Answering Scenario Check",
                    "question_count": 5,
                    "estimated_minutes": 10,
                    "is_demo": is_demo_path,
                    "data_source": "demo" if is_demo_path else "live"
                },
                "courses": [self._format_rec(r, completed_course_ids, is_demo_override=is_demo_path if getattr(r, "is_demo", None) is None else None) for r in w2_recs],
                "status": "UPCOMING",
                "is_demo": is_demo_path,
                "data_source": "demo" if is_demo_path else "live"
            },
            {
                "week_number": 3,
                "title": "Week 3: Quasi-Judicial Adjudication & Regulatory Compliance",
                "focus": "Master RTI Section 8(1) exemptions and CCS (CCA) Rule 14 disciplinary charge sheets.",
                "micro_learning_focus": "Speaking order drafting and quasi-judicial fair hearing simulation.",
                "expected_gain": "+18% Domain & Legal Accuracy",
                "practice_quiz": {
                    "title": "RTI Appeals & Disciplinary Inquiry Case Simulation",
                    "question_count": 6,
                    "estimated_minutes": 12,
                    "is_demo": is_demo_path,
                    "data_source": "demo" if is_demo_path else "live"
                },
                "courses": [self._format_rec(r, completed_course_ids, is_demo_override=is_demo_path if getattr(r, "is_demo", None) is None else None) for r in w3_recs],
                "status": "UPCOMING",
                "is_demo": is_demo_path,
                "data_source": "demo" if is_demo_path else "live"
            },
            {
                "week_number": 4,
                "title": "Week 4: Ethical Leadership & Systemic PAC Audit Resolution",
                "focus": "Settle legacy audit paras and embed proactive integrity safeguards.",
                "micro_learning_focus": "Action Taken Note (ATN) drafting and conflict of interest recusal.",
                "expected_gain": "+22% Leadership & Accountability Index",
                "practice_quiz": {
                    "title": "Public Accounts Committee (PAC) Mock Examination",
                    "question_count": 8,
                    "estimated_minutes": 15,
                    "is_demo": is_demo_path,
                    "data_source": "demo" if is_demo_path else "live"
                },
                "courses": [self._format_rec(r, completed_course_ids, is_demo_override=is_demo_path if getattr(r, "is_demo", None) is None else None) for r in w4_recs],
                "status": "UPCOMING",
                "is_demo": is_demo_path,
                "data_source": "demo" if is_demo_path else "live"
            }
        ]

        return weeks

    async def get_default_learning_path(self, user_id: Optional[uuid.UUID] = None) -> dict:
        """
        Returns a deterministic default learning trajectory with explicit demo metadata.
        """
        if user_id is None:
            user_id = uuid.UUID("11111111-1111-1111-1111-111111111101")
        milestones = await self.generate_weekly_timeline(user_id)
        for m in milestones:
            m["is_demo"] = True
            m["data_source"] = "demo"
            if "practice_quiz" in m and isinstance(m["practice_quiz"], dict):
                m["practice_quiz"]["is_demo"] = True
                m["practice_quiz"]["data_source"] = "demo"
            for c in m.get("courses", []):
                if isinstance(c, dict):
                    c["is_demo"] = True
                    c["data_source"] = "demo"
        telemetry = await self.recommendation_repo.get_telemetry_metrics(user_id)
        return {
            "milestones": milestones,
            "telemetry": telemetry,
            "is_demo": True,
            "data_source": "demo",
        }

    async def generate_skill_forecast(
        self,
        user_id: uuid.UUID,
        recommendations: Sequence[Any],
        overall_score: float,
        comp_scores: dict,
        is_demo: bool = False
    ) -> dict:
        """
        Calculates predicted competency levels (Current -> Predicted) for 
        Behavioral, Functional, and Domain pillars plus projected score uplift.
        """
        # Baseline pillar levels
        domain_levels = []
        func_levels = []
        behav_levels = []

        for code, info in comp_scores.items():
            ptype = str(_get_val(info, "competency_type", "FUNCTIONAL")).upper()
            dem_lvl = float(_get_val(info, "demonstrated_level", 2.0) or 2.0)
            if ptype == "DOMAIN":
                domain_levels.append(dem_lvl)
            elif ptype == "BEHAVIORAL":
                behav_levels.append(dem_lvl)
            else:
                func_levels.append(dem_lvl)

        cur_func = round(sum(func_levels) / max(1, len(func_levels)), 1) if func_levels else 2.2
        cur_dom = round(sum(domain_levels) / max(1, len(domain_levels)), 1) if domain_levels else 2.5
        cur_behav = round(sum(behav_levels) / max(1, len(behav_levels)), 1) if behav_levels else 3.0

        # Predicted levels assuming full completion of 4-week trajectory
        pred_func = min(4.8, round(cur_func + 1.6, 1))
        pred_dom = min(4.8, round(cur_dom + 1.4, 1))
        pred_behav = min(5.0, round(cur_behav + 1.2, 1))

        # Projected composite score uplift
        current_composite = round(overall_score, 1)
        projected_composite = min(96.0, round(current_composite + 24.5, 1))
        score_uplift = round(projected_composite - current_composite, 1)

        return {
            "current_composite_score": current_composite,
            "projected_composite_score": projected_composite,
            "projected_score_uplift": f"+{score_uplift}%",
            "is_demo": is_demo,
            "data_source": "demo" if is_demo else "live",
            "pillars": {
                "functional": {
                    "pillar_name": "Functional Competencies",
                    "current_level": cur_func,
                    "predicted_level": pred_func,
                    "uplift": f"+{round(pred_func - cur_func, 1)}",
                    "mandated_target": 4.0
                },
                "domain": {
                    "pillar_name": "Domain Competencies",
                    "current_level": cur_dom,
                    "predicted_level": pred_dom,
                    "uplift": f"+{round(pred_dom - cur_dom, 1)}",
                    "mandated_target": 4.0
                },
                "behavioral": {
                    "pillar_name": "Behavioral Competencies",
                    "current_level": cur_behav,
                    "predicted_level": pred_behav,
                    "uplift": f"+{round(pred_behav - cur_behav, 1)}",
                    "mandated_target": 4.0
                }
            }
        }

    async def mark_course_completed(
        self,
        user_id: uuid.UUID,
        course_id: uuid.UUID,
        time_spent_minutes: int
    ) -> dict:
        """
        Marks course completed in learning_progress, updates recommendation status,
        and returns updated progress metrics.
        """
        # Upsert progress to COMPLETED
        prog = await self.recommendation_repo.upsert_progress(
            user_id=user_id,
            course_id=course_id,
            progress_percentage=100,
            time_spent_minutes=time_spent_minutes,
            completion_status="COMPLETED"
        )

        # Update recommendation status if exists
        active_recs = await self.recommendation_repo.get_active_recommendations(user_id)
        for r in active_recs:
            if str(getattr(r, "course_id", "")) == str(course_id):
                rec_id = getattr(r, "id", None) or getattr(r, "_id", None)
                if rec_id:
                    await self.recommendation_repo.update_status(rec_id, "COMPLETED")
                break

        # Telemetry metrics
        telemetry = await self.recommendation_repo.get_telemetry_metrics(user_id)
        return {
            "message": "Course marked completed successfully.",
            "course_id": str(course_id),
            "progress_percentage": 100,
            "completion_status": "COMPLETED",
            "telemetry": telemetry
        }

    def _format_rec(
        self,
        r: Any,
        completed_ids: Optional[set] = None,
        is_demo_override: Optional[bool] = None
    ) -> dict:
        r_id = getattr(r, "id", None) or getattr(r, "_id", "")
        course_id = getattr(r, "course_id", "")
        completed = completed_ids is not None and str(course_id) in completed_ids
        c = getattr(r, "course", None)
        comp = getattr(r, "competency", None)

        if is_demo_override is not None:
            is_demo = is_demo_override
        else:
            is_demo = bool(getattr(r, "is_demo", False))
        data_source = "demo" if is_demo else str(getattr(r, "data_source", "live"))

        return {
            "recommendation_id": str(r_id),
            "course_id": str(course_id),
            "igot_course_id": getattr(c, "igot_course_id", "") if c else "",
            "title": getattr(c, "title", "iGOT Module") if c else "iGOT Module",
            "ministry": getattr(c, "ministry", "Department of Personnel & Training") if c else "Department of Personnel & Training",
            "duration_minutes": getattr(c, "duration_minutes", 20) if c else 20,
            "target_level": getattr(c, "target_level", 3) if c else 3,
            "difficulty": getattr(c, "difficulty", "INTERMEDIATE") if c else "INTERMEDIATE",
            "language": getattr(c, "language", "English") if c else "English",
            "tags": getattr(c, "tags", []) if c else [],
            "learning_outcomes": getattr(c, "learning_outcomes", []) if c else [],
            "course_url": getattr(c, "course_url", "https://igotkarmayogi.gov.in") if c else "https://igotkarmayogi.gov.in",
            "competency_name": getattr(comp, "competency_name", "") if comp else "",
            "competency_code": getattr(comp, "competency_code", "") if comp else "",
            "competency_type": getattr(comp, "competency_type", "FUNCTIONAL") if comp else "FUNCTIONAL",
            "priority": getattr(r, "priority", 1),
            "confidence": float(getattr(r, "confidence", 0.0) or 0.0),
            "estimated_improvement": getattr(r, "estimated_improvement", "+0.5 Competency Level"),
            "trajectory_stage": getattr(r, "trajectory_stage", "IMMEDIATE"),
            "reason": getattr(r, "explainable_rationale", ""),
            "status": "COMPLETED" if completed else getattr(r, "status", "ACTIVE"),
            "is_completed": completed,
            "is_demo": is_demo,
            "data_source": data_source,
        }

# ==============================================================================
# AI KARMAYOGI — ASSESSMENT REPOSITORY (MongoDB)
# Data Access for Quizzes, Questions, and Diagnostic Attempts
# ==============================================================================

from typing import Optional, List
from app.models.entities import _to_obj, _to_list, new_uuid, utcnow


class AssessmentRepository:
    def __init__(self, db):
        self.db = db
        self.quizzes = db["quizzes"]
        self.questions = db["questions"]
        self.attempts = db["quiz_attempts"]

    async def get_diagnostic_quiz(self):
        quiz = await self.quizzes.find_one({"quiz_type": "DIAGNOSTIC", "status": "PUBLISHED"})
        if quiz:
            q_cursor = self.questions.find({"quiz_id": quiz["_id"]})
            q_docs = await q_cursor.to_list(length=500)
            # Enrich questions with competency info
            for q in q_docs:
                if q.get("competency_id"):
                    comp = await self.db["competencies"].find_one({"_id": q["competency_id"]})
                    if comp:
                        comp["id"] = comp.pop("_id", None)
                        q["competency"] = comp
            quiz["questions"] = q_docs
        return _to_obj(quiz)

    async def get_quiz_by_id(self, quiz_id: str):
        quiz = await self.quizzes.find_one({"_id": str(quiz_id)})
        if quiz:
            q_cursor = self.questions.find({"quiz_id": quiz_id})
            q_docs = await q_cursor.to_list(length=500)
            for q in q_docs:
                if q.get("competency_id"):
                    comp = await self.db["competencies"].find_one({"_id": q["competency_id"]})
                    if comp:
                        comp["id"] = comp.pop("_id", None)
                        q["competency"] = comp
            quiz["questions"] = q_docs
        return _to_obj(quiz)

    async def get_question_by_id(self, question_id: str):
        q = await self.questions.find_one({"_id": str(question_id)})
        if q and q.get("competency_id"):
            comp = await self.db["competencies"].find_one({"_id": q["competency_id"]})
            if comp:
                comp["id"] = comp.pop("_id", None)
                q["competency"] = comp
        return _to_obj(q)

    async def get_questions_by_quiz(self, quiz_id: str):
        cursor = self.questions.find({"quiz_id": quiz_id})
        docs = await cursor.to_list(length=500)
        for q in docs:
            if q.get("competency_id"):
                comp = await self.db["competencies"].find_one({"_id": q["competency_id"]})
                if comp:
                    comp["id"] = comp.pop("_id", None)
                    q["competency"] = comp
        return _to_list(docs)

    async def get_questions_for_competencies(self, competency_ids: list):
        if not competency_ids:
            return []
        str_ids = [str(cid) for cid in competency_ids]
        cursor = self.questions.find({"competency_id": {"$in": str_ids}})
        docs = await cursor.to_list(length=500)
        for q in docs:
            if q.get("competency_id"):
                comp = await self.db["competencies"].find_one({"_id": q["competency_id"]})
                if comp:
                    comp["id"] = comp.pop("_id", None)
                    q["competency"] = comp
        return _to_list(docs)

    async def create_attempt(self, data: dict):
        if "_id" not in data:
            data["_id"] = new_uuid()
        data.setdefault("attempted_at", utcnow())
        await self.attempts.insert_one(data)
        return _to_obj(data)

    async def update_attempt(self, attempt_id: str, update_data: dict):
        await self.attempts.update_one({"_id": str(attempt_id)}, {"$set": update_data})
        doc = await self.attempts.find_one({"_id": str(attempt_id)})
        return _to_obj(doc)

    async def get_attempt_by_id(self, attempt_id: str):
        doc = await self.attempts.find_one({"_id": str(attempt_id)})
        if doc and doc.get("quiz_id"):
            quiz = await self.quizzes.find_one({"_id": doc["quiz_id"]})
            if quiz:
                quiz["id"] = quiz.pop("_id", None)
                doc["quiz"] = quiz
        return _to_obj(doc)

    async def get_latest_attempt(self, user_id: str):
        cursor = self.attempts.find({"user_id": str(user_id)}).sort("attempted_at", -1).limit(1)
        docs = await cursor.to_list(length=1)
        if docs:
            doc = docs[0]
            if doc.get("quiz_id"):
                quiz = await self.quizzes.find_one({"_id": doc["quiz_id"]})
                if quiz:
                    quiz["id"] = quiz.pop("_id", None)
                    doc["quiz"] = quiz
            return _to_obj(doc)
        return None

    async def list_attempts_by_user(self, user_id: str):
        cursor = self.attempts.find({"user_id": str(user_id)}).sort("attempted_at", -1)
        docs = await cursor.to_list(length=500)
        for doc in docs:
            if doc.get("quiz_id"):
                quiz = await self.quizzes.find_one({"_id": doc["quiz_id"]})
                if quiz:
                    quiz["id"] = quiz.pop("_id", None)
                    doc["quiz"] = quiz
        return _to_list(docs)

    async def get_latest_completed_attempt(self, user_id: str):
        cursor = self.attempts.find({"user_id": str(user_id)}).sort("attempted_at", -1).limit(1)
        docs = await cursor.to_list(length=1)
        if docs:
            doc = docs[0]
            if doc.get("quiz_id"):
                quiz = await self.quizzes.find_one({"_id": doc["quiz_id"]})
                if quiz:
                    quiz["id"] = quiz.pop("_id", None)
                    doc["quiz"] = quiz
            return _to_obj(doc)
        return None

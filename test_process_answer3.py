import asyncio
import os
import sys
import uuid
import json

sys.path.insert(0, os.path.abspath('backend'))
from app.core.config import settings
from services.assessment_service import AssessmentService
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient('mongodb://localhost:27017')
    db = client['ai_karmayogi']
    service = AssessmentService(db=db)
    user = await db['users'].find_one({"email": "rajesh.kumar@gov.in"})
    user_id = uuid.UUID(user['_id'])
    res_start = await service.start_assessment(user_id=user_id)
    res_ans = await service.process_answer(
        user_id=user_id,
        attempt_id=uuid.UUID(res_start['attempt_id']),
        question_id=uuid.UUID(res_start['question']['id']),
        selected_option_index=0,
        time_spent_seconds=10
    )
    print(json.dumps(res_ans, default=str))

asyncio.run(run())

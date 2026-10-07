import asyncio
import os
import sys
import uuid
import json

sys.path.insert(0, os.path.abspath('backend'))
from services.assessment_service import AssessmentService
from pymongo import AsyncMongoClient

async def run():
    client = AsyncMongoClient('mongodb://localhost:27017')
    db = client['ai_karmayogi']
    service = AssessmentService(db=db)
    
    # Clean up previous attempts for the user to start fresh
    user = await db['users'].find_one({"email": "rajesh.kumar@gov.in"})
    user_id = uuid.UUID(user['_id'])
    await db['quiz_attempts'].delete_many({"user_id": str(user_id)})
    
    print("1. Starting new assessment...")
    res_start = await service.start_assessment(user_id=user_id)
    attempt_id = uuid.UUID(res_start['attempt_id'])
    question_1_id = uuid.UUID(res_start['question']['id'])
    print(f"   Started attempt: {attempt_id}")
    print(f"   Question 1 ID: {question_1_id}")
    
    print("\n2. Submitting answer to Question 1...")
    res_ans_1 = await service.process_answer(
        user_id=user_id,
        attempt_id=attempt_id,
        question_id=question_1_id,
        selected_option_index=0,
        time_spent_seconds=10
    )
    print(f"   Success! Advances to index: {res_ans_1['current_question_index']}")
    question_2_id = res_ans_1['next_question']['id']
    print(f"   Question 2 ID: {question_2_id}")
    
    print("\n3. Simulating page reload (calling start_assessment again)...")
    res_resume = await service.start_assessment(user_id=user_id)
    resume_attempt_id = uuid.UUID(res_resume['attempt_id'])
    resume_question_id = uuid.UUID(res_resume['question']['id'])
    
    print(f"   Resumed attempt: {resume_attempt_id}")
    print(f"   Resumed Question ID: {resume_question_id}")
    print(f"   Current Question Index: {res_resume['current_question_index']}")
    
    if attempt_id == resume_attempt_id and str(question_2_id) == str(resume_question_id):
        print("\nALL TESTS PASSED!")
    else:
        print("\nTEST FAILED: Resumed attempt or question mismatch.")

asyncio.run(run())

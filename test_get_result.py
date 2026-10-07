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
    
    # Use the seeded user
    user = await db['users'].find_one({"email": "rajesh.kumar@gov.in"})
    user_id = uuid.UUID(user['_id'])
    
    # Get latest attempt or create one and submit it
    attempts_cursor = db['quiz_attempts'].find({"user_id": str(user_id)}).sort("attempted_at", -1)
    attempts = await attempts_cursor.to_list(length=1)
    
    if not attempts:
        # Just create an attempt and finalize it
        res_start = await service.start_assessment(user_id=user_id)
        attempt_id = uuid.UUID(res_start['attempt_id'])
        await service.submit_assessment(user_id=user_id, attempt_id=attempt_id)
    else:
        attempt_id = uuid.UUID(attempts[0]['_id'])
    
    print(f"Testing get_result for attempt {attempt_id}...")
    try:
        res = await service.get_result(user_id=user_id, attempt_id=attempt_id)
        print("Successfully retrieved result:")
        print(json.dumps(res, default=str))
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())

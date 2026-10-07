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
    
    user = await db['users'].find_one({"email": "rajesh.kumar@gov.in"})
    user_id = uuid.UUID(user['_id'])
    
    try:
        res = await service.get_history(user_id=user_id)
        print("Successfully retrieved history:")
        print(json.dumps(res, default=str))
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(run())

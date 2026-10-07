import asyncio
from types import SimpleNamespace
from backend.app.schemas.assessment import AnswerSubmitResponse

try:
    ns = SimpleNamespace(id="A", text="Option A")
    res = AnswerSubmitResponse(
        attempt_id="11111111-1111-1111-1111-111111111111",
        is_completed=False,
        current_question_index=1,
        total_answered=1,
        max_questions=15,
        progress_percentage=10.0,
        next_question={
            "id": "22222222-2222-2222-2222-222222222222",
            "question_stem": "test",
            "bloom_level": "APPLY",
            "options": [ns],
            "competency_name": "test",
            "competency_type": "FUNCTIONAL",
            "source_citation": "test"
        }
    )
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()

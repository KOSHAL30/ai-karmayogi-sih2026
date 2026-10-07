import pytest
import uuid
import json
from unittest.mock import AsyncMock, patch
from services.learning_path_service import LearningPathService

def _setup_service():
    class MockDB:
        def __getitem__(self, key):
            return AsyncMock()
    db = MockDB()
    service = LearningPathService(db)

    class MockCourse:
        id = "test-course-1"
        title = "Mock Course 1"
        duration_minutes = 60

    class MockCourse2:
        id = "test-course-2"
        title = "Mock Course 2"
        duration_minutes = 30

    class MockRec:
        recommendation_id = "test-course-1"
        course = MockCourse()
        course_id = "test-course-1"
        trajectory_stage = "IMMEDIATE"

    class MockRec2:
        recommendation_id = "test-course-2"
        course = MockCourse2()
        course_id = "test-course-2"
        trajectory_stage = "ADVANCED"

    service.rec_service.get_or_generate_recommendations = AsyncMock(return_value=[MockRec(), MockRec2()])
    service.recommendation_repo.get_user_progress_list = AsyncMock(return_value=[])
    service.assessment_repo.get_latest_completed_attempt = AsyncMock(return_value=None)
    return service

def _valid_llm_json():
    return [
        {
            "week_number": 1,
            "title": "Week 1",
            "focus": "Immediate action",
            "micro_learning_focus": "15-min bits",
            "expected_gain": "+20%",
            "practice_quiz": {"title": "Quiz", "question_count": 5, "estimated_minutes": 10},
            "course_ids": ["test-course-1"]
        },
        {
            "week_number": 2,
            "title": "Week 2",
            "focus": "Next level",
            "micro_learning_focus": "30-min bits",
            "expected_gain": "+10%",
            "practice_quiz": {"title": "Quiz", "question_count": 5, "estimated_minutes": 10},
            "course_ids": ["test-course-2"]
        },
        {
            "week_number": 3,
            "title": "Week 3",
            "focus": "Focus",
            "micro_learning_focus": "Micro",
            "expected_gain": "Gain",
            "practice_quiz": {"title": "Quiz", "question_count": 5, "estimated_minutes": 10},
            "course_ids": []
        },
        {
            "week_number": 4,
            "title": "Week 4",
            "focus": "Focus",
            "micro_learning_focus": "Micro",
            "expected_gain": "Gain",
            "practice_quiz": {"title": "Quiz", "question_count": 5, "estimated_minutes": 10},
            "course_ids": []
        }
    ]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_valid(mock_generate):
    service = _setup_service()
    mock_generate.return_value = json.dumps(_valid_llm_json())
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert len(weeks) == 4
    assert weeks[0]["title"] == "Week 1"
    assert len(weeks[0]["courses"]) == 1
    assert weeks[0]["courses"][0].get("course_id") == "test-course-1"

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_invalid_id(mock_generate):
    service = _setup_service()
    bad_json = _valid_llm_json()
    bad_json[0]["course_ids"] = ["test-course-1", "hallucinated-id"]
    mock_generate.return_value = json.dumps(bad_json)
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert len(weeks) == 4
    # Must fallback to deterministic logic (Week 1 has title with GFR Remediation)
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_omitted_course(mock_generate):
    service = _setup_service()
    bad_json = _valid_llm_json()
    bad_json[1]["course_ids"] = [] # course-2 omitted completely
    mock_generate.return_value = json.dumps(bad_json)
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_duplicate_course(mock_generate):
    service = _setup_service()
    bad_json = _valid_llm_json()
    bad_json[0]["course_ids"] = ["test-course-1", "test-course-1"]
    mock_generate.return_value = json.dumps(bad_json)
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_invalid_week(mock_generate):
    service = _setup_service()
    bad_json = _valid_llm_json()
    bad_json[2]["week_number"] = 5
    mock_generate.return_value = json.dumps(bad_json)
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_malformed_quiz(mock_generate):
    service = _setup_service()
    bad_json = _valid_llm_json()
    bad_json[0]["practice_quiz"] = "not a dict"
    mock_generate.return_value = json.dumps(bad_json)
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_llm_unavailable(mock_generate):
    service = _setup_service()
    mock_generate.return_value = None
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

@pytest.mark.asyncio
@patch("ai.llm_provider.LLMProvider.generate_response")
async def test_dynamic_learning_path_malformed_json(mock_generate):
    service = _setup_service()
    mock_generate.return_value = "This is not JSON"
    weeks = await service.generate_weekly_timeline(uuid.uuid4())
    assert "GFR Remediation" in weeks[0]["title"]

# ==============================================================================
# AI KARMAYOGI — RECOMMENDATION ENGINE UNIT & ALGORITHM VERIFICATION
# Multi-Objective Ranking, Bayesian Confidence, XAI Rationale & Skill Forecast
# ==============================================================================

import math
import sys
import uuid

# Force utf-8 stdout for Windows console
sys.stdout.reconfigure(encoding='utf-8')

from services.recommendation_service import (
    RecommendationService,
    OMEGA_DEFICIT,
    OMEGA_SEMANTIC,
    OMEGA_DURATION,
    OMEGA_CADRE
)

def test_multi_objective_weights():
    print("\n--- Test 1: Verifying Model Weight Summation ---")
    total_weights = OMEGA_DEFICIT + OMEGA_SEMANTIC + OMEGA_DURATION + OMEGA_CADRE
    print(f"Weights: Deficit={OMEGA_DEFICIT}, Semantic={OMEGA_SEMANTIC}, Duration={OMEGA_DURATION}, Cadre={OMEGA_CADRE}")
    assert math.isclose(total_weights, 1.0, rel_tol=1e-5), f"Weights must sum to 1.0, got {total_weights}"
    print("[PASS] Multi-Objective weights sum exactly to 1.0")

def test_duration_efficiency():
    print("\n--- Test 2: Verifying Micro-learning Duration Efficiency Curve ---")
    # Instantiate mock service (dummy session)
    service = RecommendationService(None)
    
    # <= 20 mins must be 1.0
    s_15 = service.calculate_duration_efficiency(15)
    s_20 = service.calculate_duration_efficiency(20)
    assert s_15 == 1.0, f"Expected 1.0 for 15 mins, got {s_15}"
    assert s_20 == 1.0, f"Expected 1.0 for 20 mins, got {s_20}"
    
    # > 20 mins must exponentially decay
    s_30 = service.calculate_duration_efficiency(30)
    s_60 = service.calculate_duration_efficiency(60)
    assert 0.75 < s_30 < 0.80, f"Expected ~0.778 for 30 mins, got {s_30}"
    assert 0.35 < s_60 < 0.40, f"Expected ~0.368 for 60 mins, got {s_60}"
    assert s_30 > s_60, "Longer courses must have lower duration efficiency"
    print(f"[PASS] Duration efficiency: 15m={s_15:.2f}, 20m={s_20:.2f}, 30m={s_30:.3f}, 60m={s_60:.3f}")

def test_bayesian_confidence():
    print("\n--- Test 3: Verifying Bayesian Confidence Calibration ---")
    service = RecommendationService(None)
    cps = 0.88

    conf_1 = service.compute_bayesian_confidence(cps, n_eval=1)
    conf_5 = service.compute_bayesian_confidence(cps, n_eval=5)
    conf_15 = service.compute_bayesian_confidence(cps, n_eval=15)

    assert conf_1 < conf_5 < conf_15, "Confidence must monotonically increase with sample size"
    assert 0.60 <= conf_1 <= 0.98
    assert 0.60 <= conf_15 <= 0.98
    print(f"[PASS] Bayesian Confidence: N=1 -> {conf_1}, N=5 -> {conf_5}, N=15 -> {conf_15}")

def test_xai_rationale():
    print("\n--- Test 4: Verifying Deterministic XAI Narrative Generation ---")
    service = RecommendationService(None)
    
    class MockCourse:
        title = "Public Procurement Rulebook"
    class MockComp:
        competency_name = "Public Procurement & GFR 2017 Compliance"
        competency_type = "FUNCTIONAL"

    rationale = service.synthesize_explainable_rationale(
        course=MockCourse(),
        comp=MockComp(),
        demonstrated_level=2,
        mandated_level=4,
        deficit_pct=50.0
    )
    assert "Critical Desk Priority" in rationale
    assert "50.0%" in rationale
    assert "GFR 2017" in rationale
    assert "Level 2 → Level 4" in rationale
    print(f"[PASS] Generated Rationale:\n  \"{rationale}\"")

def test_fastapi_endpoints():
    print("\n--- Test 5: Verifying FastAPI Route Table Mounting ---")
    from app.main import app
    openapi_schema = app.openapi()
    paths = list(openapi_schema.get("paths", {}).keys())

    expected = [
        "/api/v1/recommendations",
        "/api/v1/recommendations/path",
        "/api/v1/recommendations/course/{course_id}",
        "/api/v1/recommendations/regenerate",
        "/api/v1/recommendations/complete",
        "/api/v1/learning-path",
        "/api/v1/learning-path/complete"
    ]
    for exp in expected:
        assert any(exp == p or exp.rstrip("/") == p.rstrip("/") for p in paths), f"Route {exp} missing in FastAPI app! Found paths: {paths}"
        print(f"  [FOUND] {exp}")
    print("[PASS] All Recommendation and Learning-Path endpoints verified in FastAPI router.")

if __name__ == "__main__":
    print("\n==================================================")
    print("AI KARMAYOGI — RECOMMENDATION ENGINE TEST SUITE")
    print("==================================================")
    test_multi_objective_weights()
    test_duration_efficiency()
    test_bayesian_confidence()
    test_xai_rationale()
    test_fastapi_endpoints()
    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! [OK]")
    print("==================================================")

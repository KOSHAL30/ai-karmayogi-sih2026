# ==============================================================================
# AI KARMAYOGI — SCORING ENGINE & ADAPTIVE IRT UNIT VERIFICATION
# ==============================================================================

from services.scoring_engine import ScoringEngine

def test_probability_calculation():
    # When ability equals difficulty (theta == b), probability should be 0.5
    p_equal = ScoringEngine.probability_2pl(theta=0.0, difficulty_b=0.0, discrimination_a=1.2)
    assert abs(p_equal - 0.5) < 1e-4, f"Expected 0.5, got {p_equal}"

    # When ability is much higher than difficulty, P -> 1
    p_high = ScoringEngine.probability_2pl(theta=2.0, difficulty_b=-1.0, discrimination_a=1.2)
    assert p_high > 0.95, f"Expected > 0.95, got {p_high}"

    # When ability is much lower than difficulty, P -> 0
    p_low = ScoringEngine.probability_2pl(theta=-2.0, difficulty_b=1.5, discrimination_a=1.2)
    assert p_low < 0.05, f"Expected < 0.05, got {p_low}"

    print("[PASS] 2PL IRT Probability calculations verified.")

def test_theta_estimation_and_levels():
    # Sequence of correct answers on hard items -> theta should rise
    responses_high = [
        {"is_correct": True, "bloom_level": "APPLY", "discrimination_a": 1.2},
        {"is_correct": True, "bloom_level": "ANALYZE", "discrimination_a": 1.4},
        {"is_correct": True, "bloom_level": "EVALUATE", "discrimination_a": 1.6},
    ]
    theta_high = ScoringEngine.estimate_theta(0.0, responses_high)
    assert theta_high > 0.5, f"Expected theta > 0.5, got {theta_high}"
    level_high = ScoringEngine.map_theta_to_level(theta_high)
    assert level_high in [4, 5], f"Expected Level 4 or 5, got {level_high}"

    # Sequence of incorrect answers on easy items -> theta should fall
    responses_low = [
        {"is_correct": False, "bloom_level": "REMEMBER", "discrimination_a": 1.0},
        {"is_correct": False, "bloom_level": "UNDERSTAND", "discrimination_a": 1.1},
        {"is_correct": False, "bloom_level": "REMEMBER", "discrimination_a": 1.0},
    ]
    theta_low = ScoringEngine.estimate_theta(0.0, responses_low)
    assert theta_low < -0.5, f"Expected theta < -0.5, got {theta_low}"
    level_low = ScoringEngine.map_theta_to_level(theta_low)
    assert level_low in [1, 2], f"Expected Level 1 or 2, got {level_low}"

    print("[PASS] Latent Trait Theta estimation and Level mapping verified.")

def test_deficit_and_xai():
    competencies = [
        {
            "id": "comp-1",
            "competency_code": "COMP-GFR-01",
            "competency_name": "Public Procurement & GFR 2017",
            "competency_type": "FUNCTIONAL",
            "mandated_level": 4,
        },
        {
            "id": "comp-2",
            "competency_code": "COMP-ETH-01",
            "competency_name": "Ethical Governance",
            "competency_type": "BEHAVIORAL",
            "mandated_level": 3,
        }
    ]

    responses = [
        {"competency_id": "comp-1", "is_correct": False, "bloom_level": "APPLY", "source_citation": "GFR Rule 149"},
        {"competency_id": "comp-1", "is_correct": False, "bloom_level": "REMEMBER", "source_citation": "GFR Rule 166"},
        {"competency_id": "comp-2", "is_correct": True, "bloom_level": "APPLY", "source_citation": "CCS Conduct Rule 3"},
        {"competency_id": "comp-2", "is_correct": True, "bloom_level": "ANALYZE", "source_citation": "CVC Manual"},
    ]

    results = ScoringEngine.calculate_competency_deficits(competencies, responses, "Under Secretary")
    assert "overall_score" in results
    assert "competency_results" in results
    assert len(results["competency_results"]) == 2

    gfr_comp = next(c for c in results["competency_results"] if c["competency_code"] == "COMP-GFR-01")
    assert gfr_comp["deficit_level"] > 0
    assert "GFR Rule 149" in gfr_comp["xai_explanation"] or "GFR Rule 166" in gfr_comp["xai_explanation"]

    eth_comp = next(c for c in results["competency_results"] if c["competency_code"] == "COMP-ETH-01")
    assert eth_comp["demonstrated_level"] >= 3

    print("[PASS] Competency deficit scoring and XAI explanation generation verified.")

if __name__ == "__main__":
    print("\n--- Running AI Karmayogi Scoring Engine Tests ---")
    test_probability_calculation()
    test_theta_estimation_and_levels()
    test_deficit_and_xai()
    print("All Scoring Engine tests passed successfully!\n")

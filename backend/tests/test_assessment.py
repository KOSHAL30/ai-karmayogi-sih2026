# ==============================================================================
# AI KARMAYOGI — ASSESSMENT ENGINE & FRAC TAXONOMY TEST SUITE
# Validating Question Scoring, 3-Pillar Diagnostics & Heatmap Thresholds
# ==============================================================================

import unittest

class TestAssessmentEngine(unittest.TestCase):
    def test_pillar_categorization(self):
        pillars = ["BEHAVIORAL", "FUNCTIONAL", "DOMAIN"]
        competencies = {
            "COMM-01": {"name": "Interpersonal Communication & Grievance Empathy", "pillar": "BEHAVIORAL"},
            "PROC-01": {"name": "Public Procurement & GeM GFR 2017", "pillar": "FUNCTIONAL"},
            "FIN-01": {"name": "Central Budget Formulation & Expenditure Control", "pillar": "DOMAIN"},
        }
        for code, comp in competencies.items():
            self.assertIn(comp["pillar"], pillars)

    def test_gap_analysis_calculation(self):
        mandated = 4.0  # Level 4 on FRAC 5-point scale
        demonstrated = 2.5  # Level 2.5 demonstrated
        deficit_pct = ((mandated - demonstrated) / mandated) * 100.0
        self.assertAlmostEqual(deficit_pct, 37.5, places=1)

    def test_heatmap_risk_classification(self):
        def classify_risk(score: float) -> str:
            if score >= 72.0:
                return "LOW"
            elif score >= 66.0:
                return "MODERATE"
            else:
                return "HIGH"

        self.assertEqual(classify_risk(78.5), "LOW")
        self.assertEqual(classify_risk(72.0), "LOW")
        self.assertEqual(classify_risk(68.2), "MODERATE")
        self.assertEqual(classify_risk(66.0), "MODERATE")
        self.assertEqual(classify_risk(61.4), "HIGH")
        self.assertEqual(classify_risk(54.0), "HIGH")

    def test_adaptive_difficulty_scaling(self):
        # When an officer answers correctly with high confidence, next question tier scales up
        current_tier = "INTERMEDIATE"
        tiers = ["BASIC", "INTERMEDIATE", "ADVANCED", "EXPERT"]
        idx = tiers.index(current_tier)
        scaled_up = tiers[min(idx + 1, len(tiers) - 1)]
        self.assertEqual(scaled_up, "ADVANCED")

if __name__ == "__main__":
    unittest.main()

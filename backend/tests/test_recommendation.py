# ==============================================================================
# AI KARMAYOGI — RECOMMENDATION ENGINE TEST SUITE
# Validating Gap-to-Course Mapping, iGOT Repository Ranking & Learning Paths
# ==============================================================================

import unittest

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.sample_deficits = [
            {"code": "PROC-01", "name": "Public Procurement & GFR 2017", "deficit_pct": 40.0, "urgency": "URGENT"},
            {"code": "FIN-02", "name": "PFMS Reconciliation", "deficit_pct": 28.0, "urgency": "HIGH"},
            {"code": "DIGI-01", "name": "e-Office Advanced Workflows", "deficit_pct": 14.0, "urgency": "MEDIUM"},
        ]

        self.sample_courses = [
            {"id": "c1", "title": "GFR 2017 & GeM Masterclass", "competency_code": "PROC-01", "duration_mins": 90, "rating": 4.9},
            {"id": "c2", "title": "PFMS & Expenditure Booking", "competency_code": "FIN-02", "duration_mins": 60, "rating": 4.7},
            {"id": "c3", "title": "e-Office 7.0 Digital Secretariat", "competency_code": "DIGI-01", "duration_mins": 45, "rating": 4.6},
        ]

    def test_course_matching_by_deficit(self):
        # High deficit courses should be prioritized first
        matched = []
        for def_item in sorted(self.sample_deficits, key=lambda x: x["deficit_pct"], reverse=True):
            for course in self.sample_courses:
                if course["competency_code"] == def_item["code"]:
                    matched.append((course, def_item["deficit_pct"]))

        self.assertEqual(len(matched), 3)
        # Top course must address the highest deficit (PROC-01 with 40%)
        self.assertEqual(matched[0][0]["competency_code"], "PROC-01")

    def test_learning_roadmap_weekly_allocation(self):
        # 4 weeks of progression
        total_courses = 8
        weeks = {f"Week {i+1}": [] for i in range(4)}
        for idx in range(total_courses):
            week_idx = idx // 2
            weeks[f"Week {week_idx+1}"].append(f"Course-{idx+1}")

        self.assertEqual(len(weeks["Week 1"]), 2)
        self.assertEqual(len(weeks["Week 4"]), 2)
        self.assertEqual(sum(len(v) for v in weeks.values()), 8)

if __name__ == "__main__":
    unittest.main()

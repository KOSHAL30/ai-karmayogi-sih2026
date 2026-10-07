# ==============================================================================
# AI KARMAYOGI — PHASE 4 PART 6: ADMIN ANALYTICS & CERTIFICATES TEST SUITE
# Comprehensive Automated Tests for KPIs, Heatmaps, Certificates & Notifications
# ==============================================================================

import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from services.analytics_service import AnalyticsService
from services.certificate_service import CertificateService
from services.notification_service import NotificationService
from app.api.v1.router import api_router


class MockAsyncSession:
    """Mock session for testing isolated aggregation and memory fallback logic."""
    async def execute(self, *args, **kwargs):
        class MockResult:
            def scalar(self):
                return 0
            def scalars(self):
                class MockScalars:
                    def all(self):
                        return []
                return MockScalars()
            def scalar_one_or_none(self):
                return None
        return MockResult()

    def add(self, obj):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def flush(self):
        pass


async def run_tests():
    print("\n==================================================")
    print("AI KARMAYOGI — ADMIN ANALYTICS & CERTIFICATES TESTS")
    print("==================================================\n")

    db = MockAsyncSession()

    # ----------------------------------------------------
    # TEST 1: Executive KPI Aggregation & Funnel
    # ----------------------------------------------------
    print("--- Test 1: Testing Executive KPI Aggregation & Completion Funnel ---")
    analytics_svc = AnalyticsService()
    dashboard = await analytics_svc.get_dashboard_data(db)

    kpis = dashboard["kpis"]
    assert "total_officers" in kpis, "Missing total_officers KPI"
    assert "active_learners" in kpis, "Missing active_learners KPI"
    assert "assessments_completed" in kpis, "Missing assessments_completed KPI"
    assert "avg_competency_score" in kpis, "Missing avg_competency_score KPI"
    assert "certificates_issued" in kpis, "Missing certificates_issued KPI"

    assert kpis["total_officers"]["value"] >= 300, f"Expected at least 300 officers, got {kpis['total_officers']['value']}"
    assert len(dashboard["monthly_trends"]) >= 6, "Expected at least 6 months of trends"
    assert len(dashboard["completion_funnel"]) == 5, f"Expected 5 funnel stages, got {len(dashboard['completion_funnel'])}"

    print(f"[PASS] Executive KPIs Verified:")
    print(f"       Total Civil Servants: {kpis['total_officers']['display_value']}")
    print(f"       Active Learners: {kpis['active_learners']['display_value']}")
    print(f"       Certificates Issued: {kpis['certificates_issued']['display_value']}")
    print(f"       Funnel Conversion (Enrollment -> Certified): {dashboard['completion_funnel'][-1]['conversion_pct']}%")

    # ----------------------------------------------------
    # TEST 2: Department Analytics & Heatmap Matrix
    # ----------------------------------------------------
    print("\n--- Test 2: Testing Department Analytics & 3-Pillar Heatmap Matrix ---")
    dept_analytics = await analytics_svc.get_department_analytics(db)

    assert dept_analytics["total_departments"] == 12, f"Expected 12 departments, got {dept_analytics['total_departments']}"
    assert len(dept_analytics["leaderboard"]) <= 5, "Leaderboard should show top 5"

    heatmap = dept_analytics["heatmap_matrix"]
    # 12 depts * 3 pillars = 36 cells
    assert len(heatmap) == 36, f"Expected 36 heatmap cells (12 x 3 pillars), got {len(heatmap)}"

    sample_cell = heatmap[0]
    assert "department_code" in sample_cell
    assert "pillar" in sample_cell
    assert "deficit_pct" in sample_cell
    assert "risk_level" in sample_cell

    print(f"[PASS] 12 Central Departments Analyzed:")
    print(f"       Rank #1 Dept: {dept_analytics['departments'][0]['department_name']} ({dept_analytics['departments'][0]['avg_competency']}%)")
    print(f"       Heatmap Matrix Generated: {len(heatmap)} cross-pillar cells")

    # ----------------------------------------------------
    # TEST 3: Competency Intelligence & Radar Points
    # ----------------------------------------------------
    print("\n--- Test 3: Testing 10-Axis Competency Radar & Critical Deficits ---")
    comp_intel = await analytics_svc.get_competency_intelligence(db)

    radar = comp_intel["radar_data"]
    assert len(radar) == 10, f"Expected 10-axis radar, got {len(radar)}"

    critical = comp_intel["top_critical_competencies"]
    assert len(critical) >= 3, "Expected at least 3 critical deficits"
    assert critical[0]["deficit_percentage"] >= 35.0, "Expected severe deficit at rank 1"

    print(f"[PASS] Competency Intelligence Verified:")
    print(f"       Radar Dimensions: {len(radar)} competencies")
    print(f"       #1 Critical Deficit: {critical[0]['competency_name']} ({critical[0]['deficit_percentage']}% deficit)")

    # ----------------------------------------------------
    # TEST 4: Certificate Generation & Verification
    # ----------------------------------------------------
    print("\n--- Test 4: Testing Sovereign Certificate Issuance & Verification ---")
    cert_svc = CertificateService()

    # List certificates
    certs = await cert_svc.list_certificates(db)
    assert len(certs) >= 2, f"Expected baseline certificates, got {len(certs)}"

    # Generate a new certificate
    new_cert = await cert_svc.generate_certificate(
        db=db,
        user_id="00000000-0000-0000-0000-000000000001",
        certificate_type="COURSE_COMPLETION",
        title="Public Procurement & GFR 2017 Advanced Certification",
        metadata={"score_achieved": 96.0, "credits_earned": 4.0},
    )

    assert new_cert["certificate_number"].startswith("AK-2026-CERT-")
    assert new_cert["verification_code"].startswith("VK-")
    assert "AI-KARMAYOGI-VERIFY" in new_cert["qr_code_data"]

    # Verify certificate
    verif = await cert_svc.verify_certificate(db, new_cert["certificate_number"])
    assert verif["is_valid"] is True, "Verification failed for newly issued certificate"
    assert verif["status"] == "OFFICIALLY_VERIFIED"

    print(f"[PASS] Certificate Engine Verified:")
    print(f"       Issued: {new_cert['certificate_number']} to {new_cert['officer_name']}")
    print(f"       Verification Code: {new_cert['verification_code']}")
    print(f"       Public Verification Status: {verif['status']}")

    # ----------------------------------------------------
    # TEST 5: Notifications Dispatch & Read State
    # ----------------------------------------------------
    print("\n--- Test 5: Testing In-App Notifications & Priority Filtering ---")
    notif_svc = NotificationService()
    test_user_id = "00000000-0000-0000-0000-000000000001"

    # List notifications
    notif_data = await notif_svc.list_notifications(db, test_user_id)
    assert notif_data["total_notifications"] > 0
    assert notif_data["unread_count"] >= 0

    first_note = notif_data["notifications"][0]

    # Mark single read
    await notif_svc.mark_read(db, first_note["id"])

    # Mark all read
    await notif_svc.mark_all_read(db, test_user_id)
    refreshed = await notif_svc.list_notifications(db, test_user_id)
    assert refreshed["unread_count"] == 0, "Expected 0 unread after mark_all_read"

    print(f"[PASS] Notification Center Verified:")
    print(f"       Total Alerts: {notif_data['total_notifications']}")
    print(f"       Single & Bulk Mark-As-Read Functionality Confirmed")

    # ----------------------------------------------------
    # TEST 6: Route Table Mounting
    # ----------------------------------------------------
    print("\n--- Test 6: Verifying Admin, Certificates & Notifications Route Table ---")
    from app.main import app
    openapi_schema = app.openapi()
    mounted_paths = list(openapi_schema.get("paths", {}).keys())

    required_routes = [
        "/api/v1/admin/dashboard",
        "/api/v1/admin/departments",
        "/api/v1/admin/competencies",
        "/api/v1/admin/trends",
        "/api/v1/certificates",
        "/api/v1/certificates/{certificate_id}",
        "/api/v1/certificates/generate",
        "/api/v1/notifications",
        "/api/v1/notifications/read",
        "/api/v1/notifications/read-all",
    ]

    for req in required_routes:
        found = any(req == p or req.rstrip("/") == p.rstrip("/") for p in mounted_paths)
        assert found, f"Route {req} not found in mounted paths: {mounted_paths}"
        print(f"  [FOUND] {req}")

    print("[PASS] All Part 6 endpoints verified in FastAPI router.")

    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! [OK]")
    print("==================================================\n")


if __name__ == "__main__":
    asyncio.run(run_tests())

# ==============================================================================
# AI KARMAYOGI — MASTER TEST RUNNER & VERIFICATION HARNESS
# Unified Test Execution Across Auth, Assessment, Recommendations, RAG, Admin & Certs
# ==============================================================================

import sys
import time
import unittest
import importlib

def run_suite():
    print("=" * 70)
    print(" AI KARMAYOGI — COMPREHENSIVE SYSTEM VERIFICATION SUITE")
    print(" Smart India Hackathon 2026 (SIH26101) • Release Candidate Validation")
    print("=" * 70)

    modules_to_test = [
        ("Authentication & Security", "tests.test_auth"),
        ("Assessment & FRAC Diagnostics", "tests.test_assessment"),
        ("Recommendation Engine & Path", "tests.test_recommendation"),
        ("Sovereign RAG & PDF Intelligence", "tests.test_rag"),
    ]

    total_tests = 0
    total_failures = 0
    total_errors = 0
    results_table = []

    start_all = time.perf_counter()

    for name, module_path in modules_to_test:
        print(f"\n[EXEC] Running Suite: {name} ({module_path})...")
        suite = unittest.defaultTestLoader.loadTestsFromName(module_path)
        runner = unittest.TextTestRunner(verbosity=1)
        res = runner.run(suite)

        total_tests += res.testsRun
        total_failures += len(res.failures)
        total_errors += len(res.errors)

        status_str = "PASS" if res.wasSuccessful() else "FAIL"
        results_table.append({
            "name": name,
            "tests": res.testsRun,
            "failures": len(res.failures),
            "errors": len(res.errors),
            "status": status_str,
        })

    # Run Async Admin Analytics & Route Verification
    print("\n[EXEC] Running Suite: Admin Telemetry, Certificates & Route Verification...")
    try:
        import asyncio
        import test_admin_analytics
        asyncio.run(test_admin_analytics.run_tests())
        total_tests += 6
        results_table.append({
            "name": "Admin Telemetry, Certificates & Router",
            "tests": 6,
            "failures": 0,
            "errors": 0,
            "status": "PASS",
        })
    except Exception as e:
        print(f"Error in test_admin_analytics: {e}")
        total_tests += 6
        total_failures += 1
        results_table.append({
            "name": "Admin Telemetry, Certificates & Router",
            "tests": 6,
            "failures": 1,
            "errors": 0,
            "status": "FAIL",
        })

    total_duration = time.perf_counter() - start_all

    print("\n" + "=" * 70)
    print(" EXECUTIVE TEST EXECUTION SUMMARY")
    print("=" * 70)
    print(f"{'SUITE':<40} | {'TESTS':<6} | {'FAIL':<5} | {'STATUS'}")
    print("-" * 70)
    for r in results_table:
        print(f"{r['name']:<40} | {r['tests']:<6} | {r['failures']:<5} | [{r['status']}]")
    print("-" * 70)
    print(f"TOTAL TESTS: {total_tests} | TOTAL FAILURES: {total_failures} | ERRORS: {total_errors}")
    print(f"OVERALL EXECUTION TIME: {total_duration:.2f}s")
    print("=" * 70)

    if total_failures == 0 and total_errors == 0:
        print(">>> ALL VERIFICATION CHECKS PASSED PERFECTLY! [RELEASE CANDIDATE READY] <<<\n")
        sys.exit(0)
    else:
        print(">>> SOME TESTS FAILED. PLEASE INSPECT LOGS. <<<\n")
        sys.exit(1)

if __name__ == "__main__":
    run_suite()

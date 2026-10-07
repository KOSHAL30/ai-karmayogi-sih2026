import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

async def test_flows():
    results = {}
    
    async with httpx.AsyncClient() as client:
        # 1. Login
        login_res = await client.post(f"{BASE_URL}/auth/login", json={"email": "rajesh.kumar@gov.in", "password": "Karmayogi2026!"})
        if login_res.status_code == 200:
            token = login_res.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            results["Login"] = "PASS"
        else:
            results["Login"] = f"FAIL (HTTP {login_res.status_code} - {login_res.text})"
            return results

        # 10. Profile
        try:
            profile_res = await client.get(f"{BASE_URL}/auth/me", headers=headers)
            results["Profile"] = "PASS" if profile_res.status_code == 200 else f"FAIL ({profile_res.status_code} - {profile_res.text})"
        except Exception as e:
            results["Profile"] = f"FAIL ({e})"

        # 3. Assessment dashboard (history)
        try:
            hist_res = await client.get(f"{BASE_URL}/assessment/history", headers=headers)
            results["Assessment dashboard"] = "PASS" if hist_res.status_code == 200 else f"FAIL ({hist_res.status_code} - {hist_res.text})"
        except Exception as e:
            results["Assessment dashboard"] = f"FAIL ({e})"

        # 4. Assessment attempt
        try:
            start_res = await client.get(f"{BASE_URL}/assessment/start", headers=headers)
            if start_res.status_code == 200:
                results["Assessment attempt"] = "PASS"
                data = start_res.json().get("data", {})
                attempt_id = data.get("attempt_id")
                question_id = data.get("question", {}).get("id")
                
                # 5. Answer submission
                try:
                    ans_res = await client.post(f"{BASE_URL}/assessment/answer", headers=headers, json={
                        "attempt_id": attempt_id,
                        "question_id": question_id,
                        "selected_option_index": 0,
                        "time_spent_seconds": 5
                    })
                    results["Answer submission"] = "PASS" if ans_res.status_code == 200 else f"FAIL ({ans_res.status_code} - {ans_res.text})"
                except Exception as e:
                    results["Answer submission"] = f"FAIL ({e})"

                # 6. Assessment result/dossier
                try:
                    res_dossier = await client.get(f"{BASE_URL}/assessment/result/{attempt_id}", headers=headers)
                    results["Assessment result/dossier"] = "PASS" if res_dossier.status_code == 200 else f"FAIL ({res_dossier.status_code} - {res_dossier.text})"
                except Exception as e:
                    results["Assessment result/dossier"] = f"FAIL ({e})"

            else:
                results["Assessment attempt"] = f"FAIL ({start_res.status_code} - {start_res.text})"
                results["Answer submission"] = "FAIL (Blocked)"
                results["Assessment result/dossier"] = "FAIL (Blocked)"
        except Exception as e:
            results["Assessment attempt"] = f"FAIL ({e})"

        # 7. Recommendations
        try:
            rec_res = await client.get(f"{BASE_URL}/recommendations/", headers=headers)
            results["Recommendations"] = "PASS" if rec_res.status_code == 200 else f"FAIL ({rec_res.status_code} - {rec_res.text})"
        except Exception as e:
            results["Recommendations"] = f"FAIL ({e})"

        # 8. Learning Path
        try:
            path_res = await client.get(f"{BASE_URL}/recommendations/path", headers=headers)
            results["Learning Path"] = "PASS" if path_res.status_code == 200 else f"FAIL ({path_res.status_code} - {path_res.text})"
        except Exception as e:
            results["Learning Path"] = f"FAIL ({e})"

        # 9. Practice Drill navigation (just checking assessment endpoint logic again)
        results["Practice Drill navigation"] = results.get("Assessment attempt", "FAIL")

        # 11. Certificates
        try:
            cert_res = await client.get(f"{BASE_URL}/certificates/", headers=headers)
            results["Certificates"] = "PASS" if cert_res.status_code == 200 else f"FAIL ({cert_res.status_code} - {cert_res.text})"
        except Exception as e:
            results["Certificates"] = f"FAIL ({e})"

        # 12. Notifications
        try:
            notif_res = await client.get(f"{BASE_URL}/notifications/", headers=headers)
            results["Notifications"] = "PASS" if notif_res.status_code == 200 else f"FAIL ({notif_res.status_code} - {notif_res.text})"
        except Exception as e:
            results["Notifications"] = f"FAIL ({e})"

        # 13. Admin Analytics
        try:
            admin_res = await client.get(f"{BASE_URL}/admin/metrics", headers=headers)
            results["Admin Analytics"] = "PASS" if admin_res.status_code == 200 else f"FAIL ({admin_res.status_code} - {admin_res.text})"
        except Exception as e:
            results["Admin Analytics"] = f"FAIL ({e})"
            
        # 14. Trainer/Document Studio
        try:
            doc_res = await client.get(f"{BASE_URL}/documents/", headers=headers)
            results["Trainer/Document Studio"] = "PASS" if doc_res.status_code == 200 else f"FAIL ({doc_res.status_code} - {doc_res.text})"
        except Exception as e:
            results["Trainer/Document Studio"] = f"FAIL ({e})"
            
        # 2. Overview/Dashboard
        try:
            dash_res = await client.get(f"{BASE_URL}/users/me/dashboard", headers=headers)
            results["Overview/Dashboard"] = "PASS" if dash_res.status_code == 200 else f"FAIL ({dash_res.status_code} - {dash_res.text})"
        except Exception as e:
            results["Overview/Dashboard"] = f"FAIL ({e})"

    for k, v in results.items():
        print(f"{k}: {v}")

asyncio.run(test_flows())

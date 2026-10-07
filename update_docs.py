with open('docs/00_PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

update_text = "- Auth offline fallback (DEMO_PERSONAS_AUTH) removed completely from backend/services/auth_service.py. Authentication now strictly fails gracefully if MongoDB is unreachable, preventing fake personas from being issued."
if "Auth offline fallback" not in content:
    content = content.replace("All P0 and P1 repairs are complete.", "All P0 and P1 repairs are complete.\n" + update_text)

with open('docs/00_PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/SESSION_HANDOFF.md', 'r', encoding='utf-8') as f:
    content = f.read()

if "Auth offline fallback (DEMO_PERSONAS_AUTH) removed" not in content:
    content = content.replace("## LAST SESSION\n", "## LAST SESSION\n- Auth offline fallback (DEMO_PERSONAS_AUTH) completely stripped from ackend/services/auth_service.py along with offline fallback logic for login and token refresh. App startup message in main.py updated to reflect the actual degraded DB state instead of a \"demo-fallback mode\".\n")

with open('docs/SESSION_HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)

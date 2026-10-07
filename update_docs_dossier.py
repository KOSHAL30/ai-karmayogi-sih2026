with open('docs/00_PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

update_text = "- Assessment dossier successfully loads without 500 error. Fixed AttributeError caused by str.isoformat() calls."
if "Assessment dossier successfully loads" not in content:
    content = content.replace("All P0 and P1 repairs are complete.", "All P0 and P1 repairs are complete.\n" + update_text)

with open('docs/00_PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/SESSION_HANDOFF.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_session_text = "- Fixed /assessment/result/{attempt_id} dossier loading flow. Corrected AttributeError: 'str' object has no attribute 'isoformat' in ackend/services/assessment_service.py where ttempted_at (already a string) was being formatted again.\n"
if "Fixed /assessment/result/{attempt_id} dossier loading flow" not in content:
    content = content.replace("## LAST SESSION\n", "## LAST SESSION\n" + new_session_text)

with open('docs/SESSION_HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)

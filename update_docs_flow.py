with open('docs/00_PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

update_text = "- Assessment attempt answers now persist successfully without 404 or 500 errors. Fixed UUID-string mismatch and Pydantic serialization."
if "Assessment attempt answers now persist successfully" not in content:
    content = content.replace("All P0 and P1 repairs are complete.", "All P0 and P1 repairs are complete.\n" + update_text)

with open('docs/00_PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/SESSION_HANDOFF.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_session_text = "- Fixed /assessment/take answer submission flow. Corrected UUID comparison throwing 404s and Pydantic serialization of SimpleNamespace throwing 500s in ackend/services/assessment_service.py.\n"
if "Fixed /assessment/take answer submission flow" not in content:
    content = content.replace("## LAST SESSION\n", "## LAST SESSION\n" + new_session_text)

with open('docs/SESSION_HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)

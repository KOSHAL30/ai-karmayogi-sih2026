with open('docs/00_PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()
if "- Registration endpoint 500 error diagnosed and fixed" not in content:
    content = content.replace("All P0 and P1 repairs are complete.", "All P0 and P1 repairs are complete.\n- Registration endpoint 500 error diagnosed and fixed: now returns strict 404 for missing role/department references instead of throwing unhandled 500 errors on unseeded DBs. (No fabricated mock objects used).")
with open('docs/00_PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/SESSION_HANDOFF.md', 'r', encoding='utf-8') as f:
    content = f.read()
if "Registration endpoint 500 error diagnosed and fixed" not in content:
    content = content.replace("## LAST SESSION\n", "## LAST SESSION\n- Registration endpoint 500 error diagnosed and fixed. Reverted incorrect SimpleNamespace mock fallback in AuthService.register() and replaced it with strict 404 client errors for missing relational records (role/department). Registration now successfully returns 201 when the required seed data is present in the database, and correctly fails when it is missing.\n")
with open('docs/SESSION_HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)

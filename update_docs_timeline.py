with open('docs/00_PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

update_text = "- Learning Path 'Start Practice Drill' button properly navigates to the assessment engine instead of throwing a UI alert."
if "Start Practice Drill" not in content:
    content = content.replace("All P0 and P1 repairs are complete.", "All P0 and P1 repairs are complete.\n" + update_text)

with open('docs/00_PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

with open('docs/SESSION_HANDOFF.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_session_text = "## LAST SESSION\n- Fixed 'Start Practice Drill' loop in WeeklyTimeline.tsx by replacing the placeholder alert() with genuine React Router navigate('/assessment/take') to properly enter the assessment flow.\n"
if "WeeklyTimeline" not in content:
    content = content.replace("## LAST SESSION\n", new_session_text)

with open('docs/SESSION_HANDOFF.md', 'w', encoding='utf-8') as f:
    f.write(content)

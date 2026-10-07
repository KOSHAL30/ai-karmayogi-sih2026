import re

with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add useNavigate
if "useNavigate" not in content:
    content = content.replace("import React from 'react';", "import React from 'react';\nimport { useNavigate } from 'react-router-dom';")

# Add navigate instance
if "const navigate = useNavigate();" not in content:
    content = content.replace("export const WeeklyTimeline: React.FC<WeeklyTimelineProps> = ({", "export const WeeklyTimeline: React.FC<WeeklyTimelineProps> = ({\n  milestones,\n  onCompleteCourse,\n}) => {\n  const navigate = useNavigate();\n")
    # Also need to remove the existing destructuring because we just replaced the opening bracket
    content = content.replace("  milestones,\n  onCompleteCourse,\n}) => {\n", "")

# Replace alert with navigate
content = re.sub(r"onClick=\{\(\) => alert\(Starting Formative Drill: \$\{milestone\.practice_quiz\.title\}\)\}", "onClick={() => navigate('/assessment/take')}", content)

with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

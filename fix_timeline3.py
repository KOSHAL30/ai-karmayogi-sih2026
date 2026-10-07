import re

with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"onClick=\{\(\) => alert\(.*?\)\}", "onClick={() => navigate('/assessment/take')}", content)

with open('frontend/src/components/recommendations/WeeklyTimeline.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

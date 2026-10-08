import sys

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Update the grid layout wrapper
content = content.replace(
    '<!-- 2-Column Dashboard Grid: Recent Cadre Activity & Sovereign Node Telemetry -->',
    '{/* 1-Column Dashboard Grid: Recent Cadre Activity */}'
)
content = content.replace(
    'className="grid grid-cols-1 lg:grid-cols-3 gap-6"',
    'className="grid grid-cols-1 gap-6"'
)
content = content.replace(
    'className="lg:col-span-2 space-y-4"',
    'className="space-y-4"'
)

# Remove the Right Column entirely
# I will use a regex to match from the comment to the end of the div
pattern = re.compile(r'\{\/\* Right Column \(1/3\): Sovereign Node Telemetry \*\/\}[\s\S]*?NIC Sovereign Security Sandbox[\s\S]*?<\/div>\s*<\/div>\s*<\/CardContent>\s*<\/Card>\s*<\/div>', re.MULTILINE)
content = re.sub(pattern, '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Telemetry deleted.")

import sys

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Match the exact Telemetry Card block to delete it.
pattern = re.compile(
    r'(\s*\{\/\* Right Column \(1/3\): Sovereign Node Telemetry \*\/\}\s*<div className="space-y-4">)\s*<Card className="border-slate-200/80  shadow-sm bg-white  text-slate-900">[\s\S]*?All 2PL-IRT calculations execute on-host\.\s*</p>\s*</div>\s*</div>\s*</CardContent>\s*</Card>',
    re.MULTILINE
)

# We want to keep the wrapper and the FRAC card
replacement = r'\1'

content = re.sub(pattern, replacement, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Telemetry Card deleted.")

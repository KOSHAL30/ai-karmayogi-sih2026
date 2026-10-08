# -*- coding: utf-8 -*-
import sys
import re

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove import of DemoModeModal
content = re.sub(r"import \{ DemoModeModal \} from '@\/components\/demo\/DemoModeModal';\n", '', content)

# Remove demoModalOpen state
content = re.sub(r"const \[demoModalOpen, setDemoModalOpen\] = useState\(false\);\n", '', content)

# Remove Global SIH Evaluator Cockpit Modal component
content = re.sub(r'\{\/\* Global SIH Evaluator Cockpit Modal \(Ctrl \+ Shift \+ D\) \*\/\}[\s\S]*?\/>', '', content)

# Remove onOpenDemo from CommandPalette
content = re.sub(r'\s*onOpenDemo=\{.*?\}', '', content)

# Remove Ctrl+Shift+D from footer
content = re.sub(r'<span className="hidden sm:inline">Press <kbd[^>]*>Ctrl\+Shift\+D<\/kbd> for Demo Mode<\/span>\s*<span>[^<]*<\/span>\s*', '', content)

# Change footer text
content = re.sub(r'<span>AI Karmayogi[^<]*Smart India Hackathon 2026 \(SIH26101\)<\/span>', '<span>AI Karmayogi Platform</span>', content)

# Remove the keyboard event listener for Ctrl+Shift+D
content = re.sub(r"if \(e\.ctrlKey && e\.shiftKey && e\.key\.toLowerCase\(\) === 'd'\) \{[\s\S]*?\}", '', content)

# Also remove SIH Badge from Hero banner in App.tsx
content = re.sub(r"\{t\('overview\.badge', 'Problem Statement SIH26101[^']*Mission Karmayogi Bharat'\)\}", "{t('overview.badge', 'Mission Karmayogi Bharat Sovereign Portal')}", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("App Demo removed.")

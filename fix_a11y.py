import sys

file_path = 'frontend/src/components/layout/Navbar.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add ARIA and semantics to Navbar
content = content.replace(
    '<nav className="',
    '<nav aria-label="Main Navigation" role="navigation" className="'
)
content = content.replace(
    '<button',
    '<button aria-label="Toggle Navigation" '
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Navbar A11y fixed.")

import sys

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the badge
content = content.replace(
    'bg-white/10 backdrop-blur-md px-3 py-1 text-xs font-semibold text-teal-200 border border-white/15',
    'bg-white/60 backdrop-blur-md px-3 py-1 text-xs font-semibold text-teal-800 border border-indigo-200/50'
)

# Fix the description
content = content.replace(
    'text-teal-100/80 leading-relaxed max-w-2xl',
    'text-slate-600 leading-relaxed max-w-2xl'
)

# Fix other random teal/indigo-200/300 strings in App.tsx
content = content.replace(
    'text-teal-200',
    'text-teal-700'
)
content = content.replace(
    'text-teal-300',
    'text-teal-700'
)
content = content.replace(
    'text-indigo-200',
    'text-indigo-700'
)
content = content.replace(
    'text-indigo-300',
    'text-indigo-700'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Landing page colors fixed.")

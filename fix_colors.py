import sys

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the welcome subtitle
content = content.replace(
    'text-sm sm:text-base text-teal-200/80 font-medium mt-1',
    'text-sm sm:text-base text-teal-700/90 font-medium mt-1'
)

# Fix the Quick Action Cards
content = content.replace(
    'bg-white/5 hover:bg-white/10 backdrop-blur-md border border-white/10',
    'bg-white/60 hover:bg-white/90 backdrop-blur-md border border-indigo-200/50'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Hero colors fixed.")

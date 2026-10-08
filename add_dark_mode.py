import os

directory = 'frontend/src'

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Make the hero banner adapt to dark mode
            content = content.replace('bg-indigo-50 border-indigo-100', 'bg-indigo-50 dark:bg-slate-900 border-indigo-100 dark:border-slate-800')
            content = content.replace('text-slate-900', 'text-slate-900 dark:text-slate-100')
            
            # Subtitle
            content = content.replace('text-teal-700/90', 'text-teal-700/90 dark:text-teal-200/80')
            content = content.replace('text-slate-600', 'text-slate-600 dark:text-slate-300')
            
            # Cards
            content = content.replace('bg-white/60', 'bg-white/60 dark:bg-white/5')
            content = content.replace('hover:bg-white/90', 'hover:bg-white/90 dark:hover:bg-white/10')
            content = content.replace('border-indigo-200/50', 'border-indigo-200/50 dark:border-white/10')
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added dark mode variants to {filepath}")

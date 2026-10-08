import os

directory = 'frontend/src'

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Leftover text colors on light backgrounds
            content = content.replace('text-teal-200/80', 'text-teal-700/90')
            content = content.replace('text-teal-100/80', 'text-slate-600')
            content = content.replace('text-teal-200', 'text-teal-700')
            content = content.replace('text-teal-300', 'text-teal-700')
            content = content.replace('text-indigo-200', 'text-indigo-700')
            content = content.replace('text-indigo-300', 'text-indigo-700')
            content = content.replace('text-slate-300', 'text-slate-600')
            content = content.replace('text-slate-200', 'text-slate-600')
            content = content.replace('text-slate-400', 'text-slate-500')
            
            # Leftover dark borders and backgrounds
            content = content.replace('border-white/10', 'border-indigo-200/50')
            content = content.replace('border-white/20', 'border-indigo-200')
            content = content.replace('bg-white/5', 'bg-white/60')
            content = content.replace('bg-white/10', 'bg-white/80')
            content = content.replace('hover:bg-white/10', 'hover:bg-white/90')
            content = content.replace('hover:border-white/20', 'hover:border-indigo-300')
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed colors in {filepath}")

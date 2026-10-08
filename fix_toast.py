import sys

file_path = 'frontend/src/context/ToastContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''              <button
                onClick={() => removeToast(t.id)}
                className="p-1 rounded-lg text-slate-600 hover:text-slate-700  transition-colors shrink-0">
              aria-label="Dismiss notification"
              
                <X className="h-3.5 w-3.5" />
              </button>'''

new_code = '''              <button
                onClick={() => removeToast(t.id)}
                aria-label="Dismiss notification"
                className="p-1 rounded-lg text-slate-600 hover:text-slate-700  transition-colors shrink-0">
                <X className="h-3.5 w-3.5" />
              </button>'''

content = content.replace(old_code, new_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Toast fixed.")

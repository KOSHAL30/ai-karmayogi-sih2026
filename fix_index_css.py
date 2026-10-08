import sys
import re

file_path = 'frontend/src/index.css'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the neutered .dark block with a real dark mode palette
pattern = re.compile(r'\.dark\s*\{[^}]*\}', re.MULTILINE)
new_dark = '''  .dark {
    --background: 222 47% 11%; /* #0f172a */
    --foreground: 210 40% 98%; /* #f8fafc */

    --card: 222 47% 11%;
    --card-foreground: 210 40% 98%;

    --popover: 222 47% 11%;
    --popover-foreground: 210 40% 98%;

    --primary: 239 84% 67%; 
    --primary-foreground: 0 0% 100%;
    --primary-light: 239 100% 20%; 

    --secondary: 217.2 32.6% 17.5%; /* #1e293b */
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%; /* #94a3b8 */

    --accent: 173 80% 40%;
    --accent-foreground: 0 0% 100%;
    --accent-light: 160 84% 20%;

    --success: 142 71% 45%;
    --success-foreground: 0 0% 100%;
    --success-light: 145 80% 20%;

    --warning: 45 93% 47%;
    --warning-foreground: 0 0% 100%;
    --warning-light: 48 100% 20%;

    --destructive: 343 88% 60%;
    --destructive-foreground: 210 40% 98%;
    --destructive-light: 355 100% 20%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 239 84% 67%;
  }'''

content = re.sub(pattern, new_dark, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.css dark mode restored.")

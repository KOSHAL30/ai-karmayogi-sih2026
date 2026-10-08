import sys

file_path = 'frontend/src/context/ThemeContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_useeffect = '''  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add('light'); // Force light mode
  }, [theme]);'''

new_useeffect = '''  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  // Listen for system theme changes
  useEffect(() => {
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => {
        const root = document.documentElement;
        root.classList.remove('light', 'dark');
        root.classList.add(mediaQuery.matches ? 'dark' : 'light');
      };
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);'''

content = content.replace(old_useeffect, new_useeffect)
content = content.replace("type Theme = 'light' | 'dark';", "type Theme = 'light' | 'dark' | 'system';")
content = content.replace("const [theme, setThemeState] = useState<Theme>('light');", "const [theme, setThemeState] = useState<Theme>('system');")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("ThemeContext adapted to system.")

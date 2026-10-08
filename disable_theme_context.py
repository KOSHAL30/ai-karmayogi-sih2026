import sys

file_path = 'frontend/src/context/ThemeContext.tsx'
new_context = '''// ==============================================================================
// AI KARMAYOGI - THEME CONTEXT PROVIDER
// Dark & Light Mode Toggle with LocalStorage Persistence
// ==============================================================================

import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<Theme>('light');

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add('light'); // Force light mode
  }, [theme]);

  const toggleTheme = () => {
    // Theme toggle disabled
  };

  const setTheme = (newTheme: Theme) => {
    // Theme setter disabled
  };

  return (
    <ThemeContext.Provider value={{ theme: 'light', toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_context)
print("ThemeContext disabled.")

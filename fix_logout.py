import sys

file_path = 'frontend/src/context/AuthContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_logout = '''  const logout = () => {
    
    
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };'''

new_logout = '''  const logout = async () => {
    try {
      await api.post('/auth/logout', {});
    } catch (e) {}
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };'''

content = content.replace(old_logout, new_logout)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Logout fixed.")

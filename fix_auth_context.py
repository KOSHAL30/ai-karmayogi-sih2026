import sys
import re

file_path = 'frontend/src/context/AuthContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the initial check in useEffect
old_useeffect = '''  useEffect(() => {
    const token = null;
    if (!token) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }
    fetchProfile(token);
  }, []);'''

new_useeffect = '''  useEffect(() => {
    fetchProfile();
  }, []);'''

content = content.replace(old_useeffect, new_useeffect)

# Replace fetchProfile
old_fetchprofile = '''  const fetchProfile = async (token: string) => {
    try {
      const user = await api.get<UserProfile>('/auth/me');
      setState({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      console.warn('Session expired or invalid token. Resetting...');
      setState((prev) => ({ ...prev, isLoading: false, isAuthenticated: false, user: null }));
      
    }
  };'''

new_fetchprofile = '''  const fetchProfile = async () => {
    try {
      const user = await api.get<UserProfile>('/auth/me');
      setState({
        user,
        token: 'cookie-based',
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      setState((prev) => ({ ...prev, isLoading: false, isAuthenticated: false, user: null }));
    }
  };'''

content = content.replace(old_fetchprofile, new_fetchprofile)

# Replace refreshProfile
old_refreshprofile = '''  const refreshProfile = async () => {
    const token = null;
    if (token) {
      await fetchProfile(token);
    }
  };'''

new_refreshprofile = '''  const refreshProfile = async () => {
    await fetchProfile();
  };'''

content = content.replace(old_refreshprofile, new_refreshprofile)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("AuthContext logic fixed.")

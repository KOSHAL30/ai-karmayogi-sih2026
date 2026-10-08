import sys

file_path = 'frontend/src/context/AuthContext.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will just rewrite the entire useEffect and fetchProfile to be robust
content = re.sub(r'useEffect\(\(\) => \{[\s\S]*?\}, \[\]\);', '''useEffect(() => {
    fetchProfile();
  }, []);''', content)

content = re.sub(r'const fetchProfile = async \(.*?\) => \{[\s\S]*?^\s*\};', '''const fetchProfile = async () => {
    try {
      const user = await api.get<UserProfile>('/auth/me');
      setState({
        user,
        token: 'cookie-based',
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      setState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  };''', content, flags=re.MULTILINE)

content = re.sub(r'const refreshProfile = async \(\) => \{[\s\S]*?^\s*\};', '''const refreshProfile = async () => {
    await fetchProfile();
  };''', content, flags=re.MULTILINE)

# Also fix the login function which expects res.access_token from api
content = re.sub(r'token: res.access_token,', "token: 'cookie-based',", content)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("AuthContext REALLY fixed.")

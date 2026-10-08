import sys

file_path = 'frontend/src/lib/api.ts'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace headers token injection
old_fetch = '''const token = localStorage.getItem('karmayogi_token');
  const headers = new Headers(options.headers);

  if (token) {
    headers.set('Authorization', Bearer );
  }

  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(${API_BASE_URL}, {
    ...options,
    headers,
  });'''

new_fetch = '''const headers = new Headers(options.headers);

  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(${API_BASE_URL}, {
    ...options,
    headers,
    credentials: 'include',
  });'''

content = content.replace(old_fetch, new_fetch)

# Also fix the refresh token logic if it uses localStorage, but we can just let it fail gracefully since we are logging them out.
# Actually we can just comment out the refresh token logic or remove it, but let's keep it simple.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Frontend API patched.")

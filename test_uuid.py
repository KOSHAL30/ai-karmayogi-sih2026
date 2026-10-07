import uuid

u = uuid.uuid4()
s = str(u)

print("UUID == string:", u == s)
print("UUID != string:", u != s)
print("str(UUID) == string:", str(u) == s)

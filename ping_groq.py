from groq import Groq
import os
import sys
from dotenv import load_dotenv

load_dotenv()
try:
    client = Groq()
    completion = client.chat.completions.create(
        model="qwen-2.5-32b",
        messages=[{"role": "user", "content": "Ping"}]
    )
    print("GROQ ONLINE:", completion.choices[0].message.content)
    sys.exit(0)
except Exception as e:
    print(f"GROQ OFFLINE: {e}")
    sys.exit(1)

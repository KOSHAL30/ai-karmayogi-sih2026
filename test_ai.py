import asyncio
from backend.app.core.config import settings
from backend.ai.llm_provider import generate_response

async def test():
    print(f"Testing Groq API with Model: {settings.GROQ_MODEL}")
    try:
        response = await generate_response("Hello, what are you?", "You are a helpful assistant.")
        print("Success:")
        print(response)
    except Exception as e:
        print("Error:")
        print(e)

asyncio.run(test())

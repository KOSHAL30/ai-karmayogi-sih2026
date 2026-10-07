# ==============================================================================
# AI KARMAYOGI — LLM PROVIDER ABSTRACTION
# Groq (Primary) and Ollama (Fallback) Support
# ==============================================================================

import os
import json
import httpx
from typing import Optional
from groq import AsyncGroq
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMProvider:
    @classmethod
    async def generate_response(
        cls, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float = 0.2, 
        top_p: float = 0.9
    ) -> Optional[str]:
        """
        Routes the request to the configured LLM provider (Groq or Ollama).
        """
        provider = settings.LLM_PROVIDER.lower()
        
        if provider == "groq" and settings.GROQ_API_KEY:
            return await cls._query_groq(system_prompt, user_prompt, temperature, top_p)
        else:
            return await cls._query_ollama(system_prompt, user_prompt, temperature, top_p)

    @classmethod
    async def _query_groq(cls, system_prompt: str, user_prompt: str, temperature: float, top_p: float) -> Optional[str]:
        try:
            client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            completion = await client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                stream=False
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            # Fallback to Ollama if Groq fails
            return await cls._query_ollama(system_prompt, user_prompt, temperature, top_p)

    @classmethod
    async def _query_ollama(cls, system_prompt: str, user_prompt: str, temperature: float, top_p: float) -> Optional[str]:
        try:
            url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    url,
                    json={
                        "model": settings.LLM_MODEL,
                        "prompt": f"{system_prompt}\n\nUser Query: {user_prompt}",
                        "stream": False,
                        "options": {"temperature": temperature, "top_p": top_p}
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    return data.get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama API Error: {e}")
        return None

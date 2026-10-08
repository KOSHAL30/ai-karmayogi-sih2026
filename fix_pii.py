import sys

file_path = 'backend/ai/llm_provider.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import_str = 'import httpx\nfrom typing import Optional'
new_import = 'import httpx\nimport re\nfrom typing import Optional'
content = content.replace(import_str, new_import)

old_method = '''    @classmethod
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
        provider = settings.LLM_PROVIDER.lower()'''

new_method = '''    @classmethod
    def _scrub_pii(cls, text: str) -> str:
        """
        Federal DLP: Masks highly sensitive Personal Identifiable Information (PII) before transmission.
        """
        # Mask Aadhaar (12 digits, optional spaces/hyphens)
        text = re.sub(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', '[REDACTED_AADHAAR]', text)
        # Mask PAN Card (5 letters, 4 numbers, 1 letter)
        text = re.sub(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', '[REDACTED_PAN]', text)
        # Mask Indian Mobile Numbers
        text = re.sub(r'\b(?:\+91[\s\-]?|91[\s\-]?)?[6-9]\d{9}\b', '[REDACTED_PHONE]', text)
        # Mask Generic Emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', '[REDACTED_EMAIL]', text)
        return text

    @classmethod
    async def generate_response(
        cls, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float = 0.2, 
        top_p: float = 0.9
    ) -> Optional[str]:
        """
        Routes the request to the configured LLM provider (Groq or Ollama) with strict PII scrubbing.
        """
        # DLP Interception
        system_prompt = cls._scrub_pii(system_prompt)
        user_prompt = cls._scrub_pii(user_prompt)
        
        provider = settings.LLM_PROVIDER.lower()'''

content = content.replace(old_method, new_method)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("PII Scrubber injected.")

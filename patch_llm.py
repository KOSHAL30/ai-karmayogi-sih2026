import sys
import re

file_path = 'backend/ai/llm_provider.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''    @classmethod
    def _firewall_prompt_injection(cls, text: str) -> None:
        """
        Federal Security: Semantic Firewall to block LLM Jailbreak and Prompt Injection attempts.
        """
        lower_text = text.lower()
        blocked_phrases = [
            "ignore all previous instructions",
            "ignore previous instructions",
            "disregard previous instructions",
            "forget all instructions",
            "dump the database",
            "system prompt",
            "you are now",
            "new instructions"
        ]
        for phrase in blocked_phrases:
            if phrase in lower_text:
                raise ValueError("SECURITY_VIOLATION: Prompt injection attempt detected. Request blocked by AI Karmayogi Semantic Firewall.")
                
    @classmethod
    def _scrub_pii(cls, text: str) -> str:'''

content = content.replace('    @classmethod\n    def _scrub_pii(cls, text: str) -> str:', replacement)

# Add it to generate_response
call_replacement = '''        # DLP Interception
        system_prompt = cls._scrub_pii(system_prompt)
        user_prompt = cls._scrub_pii(user_prompt)
        
        # Injection Firewall
        cls._firewall_prompt_injection(user_prompt)'''

content = content.replace('        # DLP Interception\n        system_prompt = cls._scrub_pii(system_prompt)\n        user_prompt = cls._scrub_pii(user_prompt)', call_replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("LLM Provider patched.")

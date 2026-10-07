# ==============================================================================
# AI KARMAYOGI — SOVEREIGN SECURITY & DEFENSE GUARD
# Prompt Injection Neutralization, PDF File Integrity & Strict Payload Validation
# ==============================================================================

import re
import html
from typing import Tuple, Optional
from fastapi import HTTPException, status, UploadFile

# Adversarial prompt injection keywords & jailbreak patterns
PROMPT_INJECTION_PATTERNS = [
    r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions|prompts|directions)",
    r"(?i)\bdisregard\s+(?:all\s+)?(?:previous|prior|system)\s+(?:instructions|guidelines)",
    r"(?i)\byou\s+are\s+now\s+(?:DAN|unrestricted|jailbroken|an\s+AI\s+without\s+rules)",
    r"(?i)\breveal\s+(?:your\s+)?(?:system\s+prompt|hidden\s+instructions|master\s+directive)",
    r"(?i)\bprint\s+(?:the\s+)?system\s+prompt",
    r"(?i)\bshow\s+me\s+(?:the\s+)?initial\s+prompt",
    r"(?i)\bdo\s+anything\s+now\b",
    r"(?i)\bpretend\s+you\s+have\s+no\s+(?:ethics|rules|safeguards|filters)",
    r"(?i)\boutput\s+(?:the\s+)?raw\s+(?:database|password|secret|credentials)",
]

COMPILED_PATTERNS = [re.compile(p) for p in PROMPT_INJECTION_PATTERNS]

# Maximum policy document file size: 50MB
MAX_PDF_SIZE_BYTES = 50 * 1024 * 1024

class SecurityGuard:
    """
    Sovereign defense heuristics for input sanitization and threat prevention.
    """

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Escapes HTML characters, removes non-printable control characters,
        and normalizes whitespace.
        """
        if not text:
            return ""
        # Strip non-printable ASCII control characters except \n, \r, \t
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
        return html.escape(cleaned.strip())

    @staticmethod
    def inspect_prompt_injection(user_input: str) -> Tuple[bool, Optional[str]]:
        """
        Scans queries and RAG input against known prompt injection and jailbreak signatures.
        Returns: (is_flagged, threat_reason)
        """
        if not user_input:
            return False, None

        normalized = user_input.strip()
        for pattern in COMPILED_PATTERNS:
            match = pattern.search(normalized)
            if match:
                return True, f"Adversarial instruction detected: '{match.group(0)}'"

        return False, None

    @staticmethod
    def validate_user_query(query: str) -> str:
        """
        Validates query length, checks for adversarial injection, and returns sanitized text.
        Raises HTTPException if suspicious.
        """
        if not query or len(query.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query must contain at least 2 characters.",
            )

        if len(query) > 4000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query exceeds maximum allowed length (4,000 characters).",
            )

        flagged, reason = SecurityGuard.inspect_prompt_injection(query)
        if flagged:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security Policy Violation: Prompt injection blocked. ({reason})",
            )

        return query.strip()

    @staticmethod
    async def validate_pdf_upload(file: UploadFile) -> bytes:
        """
        Performs strict verification of uploaded government PDFs:
        1. Checks filename safety against path traversal attacks.
        2. Validates content length does not exceed 50MB.
        3. Enforces PDF magic byte header check ('%PDF-').
        """
        filename = file.filename or ""

        # Block path traversal attacks
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security Violation: Illegal filename contains path traversal sequence.",
            )

        if not filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format: Only official PDF documents (.pdf) are permitted.",
            )

        # Read file contents and verify size
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty (0 bytes).",
            )

        if len(content) > MAX_PDF_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum permissible size of 50MB (Uploaded: {len(content) / (1024 * 1024):.1f}MB).",
            )

        # Magic byte signature check: PDF files must start with %PDF-
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security Validation Failed: File header signature does not match authentic PDF standard (%PDF-).",
            )

        # Reset file pointer for downstream consumers
        await file.seek(0)
        return content

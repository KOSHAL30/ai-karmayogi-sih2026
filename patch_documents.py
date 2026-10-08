import sys
import re

file_path = 'backend/app/api/v1/endpoints/documents.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the vulnerable upload logic
replacement = '''    """
    Validates, extracts, chunks and embeds sovereign government PDFs.
    """
    import os
    from werkzeug.utils import secure_filename if False else None
    
    # 1. Path Traversal Fix: Sanitize filename
    safe_filename = os.path.basename(file.filename) if file.filename else "unknown.pdf"
    safe_filename = safe_filename.replace("/", "").replace("\\\\", "")

    if not safe_filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported for sovereign intelligence parsing."
        )

    # 2. DoS Fix: Check size before loading fully into memory
    if file.size and file.size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of 50 MB."
        )
        
    # Read content safely
    contents = await file.read()
    file_size = len(contents)
    
    # 3. File Signature Spoofing Fix: Verify Magic Bytes
    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file signature. File is not a genuine PDF."
        )

    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of 50 MB ({round(file_size / (1024*1024), 2)} MB)."
        )

    # Compute SHA-256 for duplicate detection'''

pattern = re.compile(r'    """\s*Validates, extracts, chunks and embeds sovereign government PDFs.\s*"""[\s\S]*?# Compute SHA-256 for duplicate detection')
content = re.sub(pattern, replacement, content)

# Also fix the save_filename = f"{doc_id}_{file.filename}" line to use safe_filename
content = content.replace('save_filename = f"{doc_id}_{file.filename}"', 'save_filename = f"{doc_id}_{safe_filename}"')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Documents upload patched.")

# ==============================================================================
# AI KARMAYOGI — PDF EXTRACTION & INTELLIGENT RECURSIVE CHUNKER
# PyMuPDF Structure Extraction, Breadcrumbs & Administrative Metadata Detection
# ==============================================================================

import re
import os
from typing import List, Dict, Any, Optional
import pymupdf

class PDFService:
    @staticmethod
    def extract_document_metadata(doc: pymupdf.Document, raw_text: str) -> Dict[str, Any]:
        """
        Extracts sovereign administrative metadata from document headers and content.
        """
        total_pages = len(doc)
        
        # 1. Ministry / Department Detection
        ministry = "Department of Personnel & Training"
        if "ministry of finance" in raw_text.lower():
            ministry = "Ministry of Finance"
        elif "ministry of commerce" in raw_text.lower():
            ministry = "Ministry of Commerce & Industry"
        elif "ministry of home affairs" in raw_text.lower():
            ministry = "Ministry of Home Affairs"
        elif "ministry of law" in raw_text.lower():
            ministry = "Ministry of Law & Justice"
        elif "darpg" in raw_text.lower() or "administrative reforms" in raw_text.lower():
            ministry = "Department of Administrative Reforms & Public Grievances (DARPG)"

        # 2. OM / Gazette / File Number Detection
        om_number = None
        om_match = re.search(r'(?:No\.|F\.No\.|File No\.|Notification No\.)\s*([A-Za-z0-9\/\-\(\)\.]+)', raw_text, re.IGNORECASE)
        if om_match:
            om_number = om_match.group(0).strip()

        # 3. Issue Date Detection
        issue_date = None
        date_match = re.search(r'(?:Dated|Date):\s*([0-9]{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+,?\s+[0-9]{4}|[0-9]{2}[\/\.\-][0-9]{2}[\/\.\-][0-9]{4})', raw_text, re.IGNORECASE)
        if date_match:
            issue_date = date_match.group(1).strip()

        # 4. Title Extraction
        # Look for first prominent capitalized line or fallback
        lines = [l.strip() for l in raw_text.splitlines() if len(l.strip()) > 5]
        title = "Official Government Notification"
        for line in lines[:10]:
            if line.isupper() or "OFFICE MEMORANDUM" in line.upper() or "RULES" in line.upper() or "ACT" in line.upper():
                title = line.strip()
                break
        if len(title) > 200:
            title = title[:200] + "..."

        return {
            "title": title,
            "ministry": ministry,
            "department": "Central Civil Services Division",
            "om_number": om_number or "N/A",
            "issue_date": issue_date or "Current Fiscal Year",
            "language": "English",
            "total_pages": total_pages,
        }

    @classmethod
    def process_pdf(
        cls,
        file_path: str,
        chunk_size_tokens: int = 512,
        chunk_overlap_tokens: int = 64
    ) -> Dict[str, Any]:
        """
        Parses PDF using PyMuPDF, extracts text with breadcrumb references,
        and partitions into recursive statutory chunks.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at: {file_path}")

        doc = pymupdf.open(file_path)
        full_text_accum = []
        page_records = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_text = page.get_text("text")
            page_records.append({
                "page_number": page_idx + 1,
                "text": page_text
            })
            full_text_accum.append(page_text)

        combined_raw_text = "\n".join(full_text_accum)
        metadata = cls.extract_document_metadata(doc, combined_raw_text)

        # Recursive Statutory Chunking
        chunks = []
        chunk_index = 0
        current_act = metadata["title"]
        current_chapter = "General Provisions"
        current_rule = "General"

        # Character approximations: ~4 chars per token
        max_chunk_chars = chunk_size_tokens * 4
        overlap_chars = chunk_overlap_tokens * 4

        for page in page_records:
            page_num = page["page_number"]
            text = page["text"]
            lines = text.splitlines()

            page_buffer = []

            for line in lines:
                clean = line.strip()
                if not clean:
                    continue

                # Heading / Structural Detection
                if re.match(r'^(?:CHAPTER|PART)\s+[0-9IVXLCDM]+', clean, re.IGNORECASE):
                    current_chapter = clean
                elif re.match(r'^(?:Rule|Section|Clause)\s+[0-9A-Za-z\.\(\)]+', clean, re.IGNORECASE):
                    current_rule = clean

                page_buffer.append(clean)

            page_full_text = " ".join(page_buffer)
            if not page_full_text:
                continue

            # Split text of page with overlap
            pos = 0
            while pos < len(page_full_text):
                end = pos + max_chunk_chars
                chunk_slice = page_full_text[pos:end]

                # Breadcrumb format: Act > Chapter > Rule
                breadcrumb = f"{current_act[:35]} > {current_chapter[:30]} > {current_rule[:30]}"
                sec_ref = current_rule if current_rule != "General" else f"Page {page_num}"

                tokens = len(chunk_slice.split())
                if tokens > 15: # Ignore trivial whitespace fragments
                    chunks.append({
                        "chunk_index": chunk_index,
                        "chunk_content": chunk_slice,
                        "token_count": tokens,
                        "section_reference": sec_ref,
                        "breadcrumb": breadcrumb,
                        "page_number": page_num,
                    })
                    chunk_index += 1

                pos += (max_chunk_chars - overlap_chars)

        doc.close()

        return {
            "metadata": metadata,
            "total_chunks": len(chunks),
            "chunks": chunks
        }

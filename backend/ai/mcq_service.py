# ==============================================================================
# AI KARMAYOGI — BLOOM-CLASSIFIED AI MCQ GENERATOR
# Grounded Comprehension & Extraction Questions, Distractors & Citation Metadata
# ==============================================================================

import re
import uuid
import random
from typing import List, Dict, Any, Optional

BLOOM_LEVELS = ["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE", "EVALUATE"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

STOPWORDS = {
    'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'also', 'although',
    'always', 'among', 'an', 'and', 'another', 'any', 'are', 'around', 'as', 'at',
    'back', 'be', 'became', 'because', 'become', 'been', 'before', 'being', 'below',
    'between', 'both', 'but', 'by', 'can', 'cannot', 'could', 'did', 'do', 'does',
    'doing', 'down', 'during', 'each', 'even', 'every', 'few', 'for', 'from', 'further',
    'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'him', 'his', 'how',
    'if', 'in', 'into', 'is', 'it', 'its', 'just', 'may', 'might', 'more', 'most', 'must',
    'my', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'our', 'out', 'over', 'own', 'same', 'shall', 'she', 'should', 'so', 'some', 'such',
    'than', 'that', 'the', 'their', 'theirs', 'them', 'then', 'there', 'these', 'they',
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'upon', 'very',
    'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom',
    'why', 'will', 'with', 'within', 'would', 'you', 'your'
}

START_WORDS = {
    'under', 'for', 'in', 'according', 'where', 'when', 'the', 'this', 'that',
    'these', 'those', 'with', 'as', 'by', 'if', 'on', 'at', 'pursuant', 'upon'
}


class MCQService:
    @classmethod
    def _extract_candidates_from_sentence(cls, sentence: str, sec_ref: str = "") -> List[tuple]:
        """
        Extracts candidate key terms, figures, entities, and phrases from a sentence
        to formulate grounded fill-in-the-blank comprehension and extraction questions.
        """
        candidates = []
        seen = set()

        def add(item: str, kind: str):
            clean = item.strip(' ,.:;[]"\'()\n\r\t')
            if clean.count('(') > clean.count(')'):
                clean = clean.rstrip('(')
            elif clean.count(')') > clean.count('('):
                clean = clean.rstrip(')')
            clean = clean.strip()
            if clean and clean.lower() not in seen and len(clean) >= 2:
                seen.add(clean.lower())
                candidates.append((clean, kind))

        # 1. Currency expressions (e.g. ₹25,000, Rs. 50,000)
        for m in re.finditer(r'(?:[\u20b9]|Rs\.?)\s*[\d,]+(?:\.\d+)?', sentence):
            add(m.group(0), 'currency')

        # 2. Numbers with units or thresholds (e.g. 3 manufacturers, 21 days, 50%, 0.5% per week)
        for m in re.finditer(
            r'\b\d+(?:,\d+)*(?:\.\d+)?\s*(?:working days?|calendar days?|days?|months?|years?|manufacturers?|vendors?|lakh|crore|percent|%|hours?|weeks?|quarters?)(?:\s+(?:per|of)\s+[a-zA-Z0-9% -]+)?\b',
            sentence,
            re.IGNORECASE
        ):
            add(m.group(0), 'quantity')

        # 3. Multi-word capitalized phrases (Proper nouns / specialized entities)
        for m in re.finditer(r'\b[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)+\b', sentence):
            phrase = m.group(0)
            first_word = phrase.split()[0].lower()
            if first_word in START_WORDS:
                rem = ' '.join(phrase.split()[1:])
                if rem and len(rem.split()) >= 2:
                    add(rem, 'entity')
            else:
                add(phrase, 'entity')

        # 4. Acronyms & codes (e.g. PAC, GeM, IFD, L-1, CRAC, DDO, OEM)
        for m in re.finditer(r'\b[A-Z][A-Za-z0-9]*(?:-[0-9A-Za-z]+)?\b', sentence):
            val = m.group(0)
            if (val.isupper() and 2 <= len(val) <= 8) or ('-' in val and len(val) <= 8):
                if val.lower() not in STOPWORDS:
                    add(val, 'acronym')

        # 5. Meaningful 2-to-3 word content phrases
        words = re.findall(r'\b[a-zA-Z0-9-]+\b', sentence)
        for idx in range(len(words) - 1):
            w1, w2 = words[idx], words[idx + 1]
            if (w1.lower() not in STOPWORDS and w2.lower() not in STOPWORDS and
                len(w1) >= 3 and len(w2) >= 3 and not (w1.isdigit() and w2.isdigit())):
                phrase_match = re.search(r'\b' + re.escape(w1) + r'\s+' + re.escape(w2) + r'\b', sentence)
                if phrase_match:
                    add(phrase_match.group(0), 'phrase')

        # 6. Plain numbers (>= 2 digits)
        for m in re.finditer(r'\b\d+(?:,\d+)*\b', sentence):
            add(m.group(0), 'number')

        # 7. Document section references found in text (e.g. Rule 149(i), Section 12)
        for m in re.finditer(
            r'\b(?:Rule|Section|Clause|Sub-rule|Article|Schedule|Chapter|Paragraph)\s+[0-9]+(?:\([a-zA-Z0-9]+\))*(?!\w)',
            sentence,
            re.IGNORECASE
        ):
            add(m.group(0), 'reference')

        # 8. Significant single content words
        for w in re.findall(r'\b[a-zA-Z]{5,}\b', sentence):
            if w.lower() not in STOPWORDS:
                add(w, 'keyword')

        # Prioritize domain content over duplicating section references already in stem
        sec_clean = sec_ref.strip().lower()
        preferred = []
        deprioritized = []
        for cand, kind in candidates:
            cand_clean = cand.strip().lower()
            if sec_clean and (cand_clean in sec_clean or sec_clean in cand_clean):
                deprioritized.append((cand, kind))
            else:
                preferred.append((cand, kind))

        return preferred + deprioritized

    @classmethod
    def _extract_text_phrases(cls, text: str) -> List[str]:
        """
        Extracts small meaningful phrases (2-4 words) and substantive words
        strictly from the chunk text to serve as grounded distractors.
        Zero hardcoded or invented terms are used.
        """
        phrases: List[str] = []
        seen = set()

        def add_phrase(p: str):
            clean = p.strip(' ,.:;[]"\'()\n\r\t')
            if clean.count('(') > clean.count(')'):
                clean = clean.rstrip('(')
            elif clean.count(')') > clean.count('('):
                clean = clean.rstrip(')')
            clean = clean.strip()
            if clean and clean.lower() not in seen and 2 <= len(clean) <= 45:
                words = clean.lower().split()
                if all(w in STOPWORDS for w in words):
                    return
                seen.add(clean.lower())
                phrases.append(clean)

        # 1. Multi-word capitalized phrases (Proper nouns / entities)
        for m in re.finditer(r'\b[A-Z][a-zA-Z0-9]*(?:\s+[A-Z][a-zA-Z0-9]*)+\b', text):
            add_phrase(m.group(0))

        # 2. Extract 2-to-4 word phrases with non-stopword boundaries
        clauses = re.split(r'[,;:.!?\n]+', text)
        for clause in clauses:
            tokens = re.findall(r'\b[a-zA-Z0-9\u20b9$-]+\b', clause)
            if len(tokens) < 2:
                continue
            for n in (3, 2, 4):
                for i in range(len(tokens) - n + 1):
                    gram = tokens[i:i + n]
                    first_w, last_w = gram[0].lower(), gram[-1].lower()
                    if first_w in STOPWORDS or last_w in STOPWORDS:
                        continue
                    if not any(len(w) >= 3 and w.lower() not in STOPWORDS for w in gram):
                        continue
                    pattern = r'\b' + r'\s+'.join(re.escape(w) for w in gram) + r'\b'
                    match = re.search(pattern, clause, re.IGNORECASE)
                    if match:
                        add_phrase(match.group(0))

        # 3. Substantive single content words (length >= 4, not stopwords, not pure digits)
        for w in re.findall(r'\b[a-zA-Z]{4,}\b', text):
            if w.lower() not in STOPWORDS:
                add_phrase(w)

        return phrases

    @classmethod
    def generate_mcqs_from_chunks(
        cls,
        document_title: str,
        ministry: str,
        chunks: List[Dict[str, Any]],
        num_questions: int = 5,
        target_bloom: Optional[str] = None,
        target_difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates grounded, Bloom-classified multiple-choice questions purely
        from the provided document_chunks. All questions, answers, and distractors
        are derived strictly from phrases and facts in the chunk text.
        Never invents statutory rules or generic hardcoded distractors.
        """
        if not chunks:
            return []

        # 1. Parse sentences and collect candidate terms across all chunks
        parsed_sentences = []
        global_pools: Dict[str, List[str]] = {
            'currency': [],
            'quantity': [],
            'reference': [],
            'entity': [],
            'acronym': [],
            'phrase': [],
            'number': [],
            'keyword': []
        }
        all_terms: List[str] = []
        all_text_phrases: List[str] = []

        for c_idx, chunk in enumerate(chunks):
            content = (
                (chunk.get("chunk_content") if isinstance(chunk, dict) else getattr(chunk, "chunk_content", None)) or
                (chunk.get("content") if isinstance(chunk, dict) else getattr(chunk, "content", None)) or
                (chunk.get("text") if isinstance(chunk, dict) else getattr(chunk, "text", None)) or
                ""
            ).strip()

            sec_ref = (
                (chunk.get("section_reference") if isinstance(chunk, dict) else getattr(chunk, "section_reference", None)) or
                (chunk.get("section") if isinstance(chunk, dict) else getattr(chunk, "section", None)) or
                ""
            )

            page_num = (
                (chunk.get("page_number") if isinstance(chunk, dict) else getattr(chunk, "page_number", None)) or
                (chunk.get("page") if isinstance(chunk, dict) else getattr(chunk, "page", None)) or
                1
            )

            bcrumb = (
                (chunk.get("breadcrumb") if isinstance(chunk, dict) else getattr(chunk, "breadcrumb", None)) or
                document_title or
                sec_ref or
                f"Page {page_num}"
            )

            if not content:
                continue

            # Extract small phrases directly from chunk text for grounded distractors
            chunk_phrases = cls._extract_text_phrases(content)
            for p in chunk_phrases:
                if p not in all_text_phrases:
                    all_text_phrases.append(p)

            raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', content) if s.strip()]
            valid_sentences = [s for s in raw_sentences if len(s) >= 20]
            if not valid_sentences and raw_sentences:
                valid_sentences = raw_sentences

            for s in valid_sentences:
                candidates = cls._extract_candidates_from_sentence(s, sec_ref)
                parsed_sentences.append({
                    "sentence": s,
                    "section_reference": sec_ref,
                    "page_number": page_num,
                    "breadcrumb": bcrumb,
                    "candidates": candidates
                })

                for cand, kind in candidates:
                    if cand not in global_pools.get(kind, []):
                        global_pools.setdefault(kind, []).append(cand)
                    if cand not in all_terms:
                        all_terms.append(cand)

        if not parsed_sentences:
            return []

        # Grounded comprehension & extraction question templates mapped to Bloom levels
        # Formulated neutrally to never invent statutory rules or procedures
        stem_templates = {
            "REMEMBER": [
                "Based on {section}, which term or detail correctly completes the following statement?\n\"{blanked}\"",
                "According to {section}, identify the correct detail to complete the statement:\n\"{blanked}\""
            ],
            "UNDERSTAND": [
                "According to the passage in {section}, what correctly fills the blank in the statement below?\n\"{blanked}\"",
                "Based on {section}, complete the following excerpt:\n\"{blanked}\""
            ],
            "APPLY": [
                "Applying the information provided in {section}, which option correctly completes the statement?\n\"{blanked}\"",
                "Based on the provisions stated in {section}, identify the correct requirement:\n\"{blanked}\""
            ],
            "ANALYZE": [
                "Analyzing the details described in {section}, which phrase or value accurately completes the statement?\n\"{blanked}\"",
                "Upon review of {section}, which detail accurately completes the excerpt:\n\"{blanked}\""
            ],
            "EVALUATE": [
                "Evaluating the text in {section}, which option correctly fulfills the statement?\n\"{blanked}\"",
                "Based on the criteria stated in {section}, what is the correct term to complete the excerpt:\n\"{blanked}\""
            ]
        }

        generated_questions = []

        # Generate the requested number of questions
        for i in range(num_questions):
            sent_info = parsed_sentences[i % len(parsed_sentences)]
            sentence = sent_info["sentence"]
            sec_ref = sent_info["section_reference"]
            page_num = sent_info["page_number"]
            bcrumb = sent_info["breadcrumb"]
            candidates = sent_info["candidates"]

            bloom = target_bloom or BLOOM_LEVELS[i % len(BLOOM_LEVELS)]
            difficulty = target_difficulty or DIFFICULTIES[i % len(DIFFICULTIES)]

            # Select candidate target
            target = None
            target_kind = "keyword"
            if candidates:
                cand_idx = (i // len(parsed_sentences)) % len(candidates)
                target, target_kind = candidates[cand_idx]

            if not target or target not in sentence:
                tokens = [w for w in re.findall(r'\b[a-zA-Z0-9-]+\b', sentence) if w.lower() not in STOPWORDS and len(w) >= 4]
                if tokens:
                    target = tokens[0]
                    target_kind = "keyword"
                else:
                    target = sentence.split()[-1].strip(' ,.:;[]"\'()')
                    target_kind = "keyword"

            # Create fill-in-the-blank representation
            pattern = r'\b' + re.escape(target) + r'\b'
            if re.search(pattern, sentence):
                blanked = re.sub(pattern, "________", sentence, count=1)
            else:
                blanked = sentence.replace(target, "________", 1)

            # Assemble distractors purely and strictly from document chunk text
            distractor_pool: List[str] = []

            # 1. Prefer items of the same kind from global chunk pool
            same_kind_items = [item for item in global_pools.get(target_kind, []) if item.lower() != target.lower()]
            shuffled_same = list(same_kind_items)
            random.shuffle(shuffled_same)
            distractor_pool.extend(shuffled_same)

            # 2. Related candidate terms from document chunks
            related_kinds = ['entity', 'phrase', 'acronym', 'quantity', 'currency', 'keyword', 'reference', 'number']
            for rk in related_kinds:
                if len(distractor_pool) >= 10:
                    break
                if rk != target_kind:
                    items = [item for item in global_pools.get(rk, []) if item.lower() != target.lower()]
                    random.shuffle(items)
                    for item in items:
                        if item.lower() not in [d.lower() for d in distractor_pool]:
                            distractor_pool.append(item)

            # 3. Grounded small phrases extracted directly from the chunk text
            # ("If distractors are hard to generate, just extract random small phrases from the text.")
            shuffled_phrases = [p for p in all_text_phrases if p.lower() != target.lower()]
            random.shuffle(shuffled_phrases)
            for phrase in shuffled_phrases:
                if len(distractor_pool) >= 15:
                    break
                if phrase.lower() not in [d.lower() for d in distractor_pool]:
                    distractor_pool.append(phrase)

            # 4. General terms from chunks
            for term in all_terms:
                if len(distractor_pool) >= 15:
                    break
                if term.lower() != target.lower() and term.lower() not in [d.lower() for d in distractor_pool]:
                    distractor_pool.append(term)

            # Select 3 unique distractors strictly from document text
            selected_distractors: List[str] = []
            for d in distractor_pool:
                if d.lower() != target.lower() and d.lower() not in [sd.lower() for sd in selected_distractors]:
                    selected_distractors.append(d)
                if len(selected_distractors) == 3:
                    break

            # If document is sparse, extract additional tokens from document title, ministry, or breadcrumb
            if len(selected_distractors) < 3:
                fallback_sources = [bcrumb, document_title, ministry, sentence]
                for src in fallback_sources:
                    if not src:
                        continue
                    src_words = [w for w in re.findall(r'\b[a-zA-Z0-9-]+\b', src) if w.lower() not in STOPWORDS and len(w) >= 3]
                    for w in src_words:
                        if w.lower() != target.lower() and w.lower() not in [sd.lower() for sd in selected_distractors]:
                            selected_distractors.append(w)
                        if len(selected_distractors) == 3:
                            break
                    if len(selected_distractors) == 3:
                        break

            # Guarantee exactly 4 options using sub-slices of text if ultra-sparse
            while len(selected_distractors) < 3:
                offset = len(selected_distractors) + 1
                words = sentence.split()
                if len(words) >= offset:
                    sub_val = words[offset - 1].strip(' ,.:;[]"\'()')
                    if sub_val.lower() != target.lower() and sub_val.lower() not in [sd.lower() for sd in selected_distractors] and len(sub_val) >= 2:
                        selected_distractors.append(sub_val)
                        continue
                selected_distractors.append(f"{target[:10]} - excerpt {offset}")

            # Assemble and shuffle options
            option_texts = [target] + selected_distractors[:3]
            random.shuffle(option_texts)
            correct_idx = option_texts.index(target)
            ans_letter = chr(65 + correct_idx)

            options = [
                {
                    "id": chr(65 + o_idx),
                    "text": opt_text,
                    "option_text": opt_text,
                    "is_correct": (o_idx == correct_idx)
                }
                for o_idx, opt_text in enumerate(option_texts)
            ]

            # Construct grounded section label without inventing statutory rules
            section_label = sec_ref if sec_ref else (bcrumb if bcrumb else "the provided text")

            templates = stem_templates.get(bloom, stem_templates["UNDERSTAND"])
            stem_tmpl = templates[i % len(templates)]
            stem = stem_tmpl.format(section=section_label, blanked=blanked)

            # Pedagogical explanation grounded purely in the chunk sentence
            sec_display = sec_ref if sec_ref else "the document"
            explanation = (
                f"Based on {sec_display} (Page {page_num}), the text explicitly states: \"{sentence}\" "
                f"This directly confirms '{target}' as the correct requirement."
            )

            # Actual citation metadata
            if sec_ref and bcrumb and sec_ref.strip().lower() != bcrumb.strip().lower():
                citation = f"{bcrumb} ({sec_ref}, Page {page_num})"
            elif bcrumb:
                citation = f"{bcrumb} (Page {page_num})"
            elif sec_ref:
                citation = f"{sec_ref} (Page {page_num})"
            else:
                citation = f"{document_title} (Page {page_num})" if document_title else f"Page {page_num}"

            q_id = str(uuid.uuid4())

            generated_questions.append({
                "id": q_id,
                "question": stem,
                "question_stem": stem,
                "options": options,
                "correct_answer": ans_letter,
                "correct_option_index": correct_idx,
                "correct_index": correct_idx,
                "difficulty": difficulty,
                "bloom_level": bloom,
                "explanation": explanation,
                "pedagogical_explanation": explanation,
                "citation": citation,
                "source_citation": citation,
                "source_page": page_num,
                "section_reference": sec_ref,
                "breadcrumb": bcrumb,
                "status": "DRAFT",
                "document_title": document_title
            })

        return generated_questions

    @classmethod
    async def generate_mcqs_ai(
        cls,
        document_title: str,
        ministry: str,
        chunks: List[Dict[str, Any]],
        num_questions: int = 5,
        target_bloom: Optional[str] = None,
        target_difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Attempts AI-based MCQ generation using LLMProvider, with seamless fallback
        to the grounded deterministic chunk extractor.
        """
        if not chunks:
            return []

        try:
            try:
                from ai.llm_provider import LLMProvider
            except ImportError:
                try:
                    from backend.ai.llm_provider import LLMProvider
                except ImportError:
                    from app.ai.llm_provider import LLMProvider
            import json

            context_text = "\n\n".join([
                f"[{c.get('section_reference', '')} p.{c.get('page_number', 1)}] {c.get('chunk_content', '')}"
                for c in chunks[:5]
            ])

            system_prompt = (
                "You are an expert Government of India examination setter. "
                "Generate a JSON array of multiple choice questions based STRICTLY on the provided text. "
                "Output ONLY a valid JSON array of objects. Each object must have: "
                "question (string), options (array of 4 strings), correct_idx (integer 0-3), explanation (string), citation (string)."
            )

            user_prompt = f"Text:\n{context_text}\n\nGenerate {num_questions} questions."

            llm_response = await LLMProvider.generate_response(system_prompt, user_prompt, temperature=0.3)

            if llm_response:
                start = llm_response.find('[')
                end = llm_response.rfind(']') + 1
                if start >= 0 and end > start:
                    json_str = llm_response[start:end]
                    data = json.loads(json_str)

                    if isinstance(data, list) and len(data) > 0:
                        questions = []
                        # Extract fallback phrases in case LLM gave fewer than 4 options
                        fallback_phrases = []
                        for c in chunks:
                            c_text = c.get('chunk_content', '') or c.get('content', '') or ''
                            fallback_phrases.extend(cls._extract_text_phrases(c_text))

                        for i, q in enumerate(data):
                            correct_idx = q.get("correct_idx", 0)
                            if not (0 <= correct_idx < 4):
                                correct_idx = 0
                            raw_opts = q.get("options", [])[:4]
                            fb_idx = 0
                            while len(raw_opts) < 4:
                                if fb_idx < len(fallback_phrases) and fallback_phrases[fb_idx] not in raw_opts:
                                    raw_opts.append(fallback_phrases[fb_idx])
                                else:
                                    raw_opts.append(f"Detail {len(raw_opts) + 1}")
                                fb_idx += 1

                            options = [
                                {
                                    "id": chr(65 + j),
                                    "text": opt,
                                    "option_text": opt,
                                    "is_correct": (j == correct_idx)
                                }
                                for j, opt in enumerate(raw_opts)
                            ]
                            q_stem = q.get("question", "")
                            explanation = q.get("explanation", "")
                            citation = q.get("citation", f"From {document_title}")
                            difficulty = target_difficulty or "Medium"
                            bloom = target_bloom or "UNDERSTAND"
                            first_chunk = chunks[0] if chunks else {}
                            sec_ref = first_chunk.get("section_reference", "")
                            bcrumb = first_chunk.get("breadcrumb", document_title)
                            page_num = first_chunk.get("page_number", 1)

                            questions.append({
                                "id": str(uuid.uuid4()),
                                "question": q_stem,
                                "question_stem": q_stem,
                                "options": options,
                                "correct_answer": chr(65 + correct_idx),
                                "correct_option_index": correct_idx,
                                "correct_index": correct_idx,
                                "difficulty": difficulty,
                                "bloom_level": bloom,
                                "explanation": explanation,
                                "pedagogical_explanation": explanation,
                                "citation": citation,
                                "source_citation": citation,
                                "source_page": page_num,
                                "section_reference": sec_ref,
                                "breadcrumb": bcrumb,
                                "status": "DRAFT",
                                "document_title": document_title
                            })
                        return questions
        except Exception as e:
            print(f"AI MCQ Generation failed: {e}")

        # Fallback to deterministic grounded generator
        return cls.generate_mcqs_from_chunks(
            document_title, ministry, chunks, num_questions, target_bloom, target_difficulty
        )

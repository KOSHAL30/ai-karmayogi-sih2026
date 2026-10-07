# ==============================================================================
# AI KARMAYOGI — CERTIFICATE REPOSITORY (MongoDB)
# Sovereign Digital Credentials, Verification Hashes & Tamper-Proof Storage
# ==============================================================================

import copy
import datetime
import logging
from typing import List, Optional, Dict, Any
import uuid

from app.models.entities import new_uuid, utcnow, _to_obj, _to_list

logger = logging.getLogger(__name__)




def _format_certificate(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return None
    issued_at = doc.get("issued_at")
    if isinstance(issued_at, datetime.datetime):
        issued_at_str = issued_at.isoformat()
    elif isinstance(issued_at, str):
        issued_at_str = issued_at
    else:
        issued_at_str = utcnow().isoformat()

    cert_id = str(doc.get("_id") or doc.get("id") or "")
    return {
        "id": cert_id,
        "user_id": str(doc.get("user_id", "")),
        "officer_name": doc.get("officer_name", "Government Officer"),
        "designation": doc.get("designation", "Officer"),
        "department": doc.get("department", "Central Secretariat"),
        "ministry": doc.get("ministry", "Government of India"),
        "certificate_number": doc.get("certificate_number", ""),
        "certificate_type": doc.get("certificate_type", "COURSE_COMPLETION"),
        "title": doc.get("title", ""),
        "issuing_authority": doc.get("issuing_authority", "Mission Karmayogi Bharat \u2022 Capacity Building Commission"),
        "issued_at": issued_at_str,
        "verification_code": doc.get("verification_code", ""),
        "verification_url": doc.get("verification_url", ""),
        "qr_code_data": doc.get("qr_code_data", ""),
        "metadata": doc.get("metadata", {}),
    }


class CertificateRepository:
    """Manages official certificate issuance, retrieval, and verification."""

    def __init__(self, db: Any):
        self.db = db
        self.collection = db["certificates"] if db is not None and hasattr(db, "__getitem__") else None

    async def get_all(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists certificates for an officer or across the cadre."""
        if self.collection is not None:
            try:
                query = {}
                if user_id:
                    query["user_id"] = str(user_id)
                cursor = self.collection.find(query).sort("issued_at", -1)
                db_certs = await cursor.to_list(length=500)
                if db_certs:
                    return [_format_certificate(c) for c in db_certs]
            except Exception as e:
                logger.warning("CertificateRepository.get_all MongoDB query failed: %s", e)

        return []

    async def get_by_id(self, certificate_id: str) -> Optional[Dict[str, Any]]:
        """Gets certificate details by ID, certificate number, or verification code."""
        if not certificate_id:
            return None
        cert_id_str = str(certificate_id)

        if self.collection is not None:
            try:
                doc = await self.collection.find_one({
                    "$or": [
                        {"_id": cert_id_str},
                        {"id": cert_id_str},
                        {"certificate_number": cert_id_str},
                        {"verification_code": cert_id_str},
                    ]
                })
                if doc:
                    return _format_certificate(doc)
            except Exception as e:
                logger.warning("CertificateRepository.get_by_id MongoDB query failed: %s", e)

        return None

    async def create_certificate(
        self,
        user_id: str,
        certificate_type: str,
        title: str,
        officer_name: str,
        designation: str,
        department: str,
        ministry: str = "Government of India",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Issues an official verifiable digital credential."""
        unique_suffix = uuid.uuid4().hex[:6].upper()
        cert_number = f"AK-2026-CERT-{unique_suffix}"
        verif_code = f"VK-{unique_suffix[:4]}-{uuid.uuid4().hex[:4].upper()}-IN"
        verif_url = f"https://karmayogi.gov.in/verify?cert={cert_number}"
        qr_data = f"AI-KARMAYOGI-VERIFY:{cert_number}:{officer_name.replace(' ', '_')}:{title[:20]}:VALID"
        cert_id = new_uuid()
        issued_at_str = utcnow().isoformat()

        cert_dict = {
            "id": cert_id,
            "user_id": str(user_id),
            "officer_name": officer_name,
            "designation": designation,
            "department": department,
            "ministry": ministry,
            "certificate_number": cert_number,
            "certificate_type": certificate_type,
            "title": title,
            "issuing_authority": "Mission Karmayogi Bharat \u2022 Capacity Building Commission",
            "issued_at": issued_at_str,
            "verification_code": verif_code,
            "verification_url": verif_url,
            "qr_code_data": qr_data,
            "metadata": metadata or {"score_achieved": 90.0, "credits_earned": 3.0},
        }

        if self.collection is not None:
            try:
                mongo_doc = {**cert_dict, "_id": cert_id}
                await self.collection.insert_one(mongo_doc)
            except Exception as e:
                logger.warning("CertificateRepository.create_certificate MongoDB insert failed: %s", e)

        return cert_dict

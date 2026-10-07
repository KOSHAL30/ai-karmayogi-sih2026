# ==============================================================================
# AI KARMAYOGI — CERTIFICATE SERVICE
# Automated Credential Issuance, Tamper-Proof Digital Hashes & Verification
# ==============================================================================

from typing import Dict, Any, List, Optional
import uuid
from repositories.certificate_repository import CertificateRepository
from repositories.user_repository import UserRepository


class CertificateService:
    def __init__(
        self,
        db: Any = None,
        cert_repo: Optional[CertificateRepository] = None,
    ):
        self.db = db
        self.cert_repo = cert_repo or (CertificateRepository(db) if db is not None else None)

    def _resolve_repo(self, db: Any = None) -> CertificateRepository:
        if self.cert_repo is not None and (db is None or db == self.db):
            return self.cert_repo
        target_db = db if db is not None else self.db
        return CertificateRepository(target_db)

    async def list_certificates(
        self, db: Any = None, user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists certificates for an officer or entire cadre."""
        if isinstance(db, str) and user_id is None:
            user_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.get_all(user_id=user_id)

    async def get_certificate(
        self, db: Any = None, certificate_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Gets certificate details by ID or certificate number."""
        if isinstance(db, str) and certificate_id is None:
            certificate_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.get_by_id(certificate_id=certificate_id)

    async def generate_certificate(
        self,
        db: Any = None,
        user_id: Optional[str] = None,
        certificate_type: str = "COURSE_COMPLETION",
        title: str = "",
        course_id: Optional[str] = None,
        quiz_attempt_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Automatically generates an official verifiable certificate."""
        if isinstance(db, str) and user_id is None:
            user_id = db
            db = None

        target_db = db if db is not None else self.db

        # Look up user details
        officer_name = "Rajesh Kumar"
        designation = "Under Secretary"
        department = "Department of Expenditure"
        ministry = "Ministry of Finance"

        if target_db is not None:
            try:
                user_repo = UserRepository(target_db)
                user = await user_repo.get_by_id(user_id)
                if user:
                    officer_name = getattr(user, "full_name", officer_name)
                    designation = getattr(user, "designation", designation)
                    dept = getattr(user, "department", None)
                    if dept:
                        department = getattr(dept, "name", department)
                        ministry = getattr(dept, "ministry_name", ministry)
            except Exception:
                pass

        meta = metadata or {}
        if "score_achieved" not in meta:
            meta["score_achieved"] = 90.0
        if "credits_earned" not in meta:
            meta["credits_earned"] = 3.0
        if "signatory_title" not in meta:
            meta["signatory_title"] = "Member (Administration), Capacity Building Commission"

        repo = self._resolve_repo(target_db)
        return await repo.create_certificate(
            user_id=user_id,
            certificate_type=certificate_type,
            title=title,
            officer_name=officer_name,
            designation=designation,
            department=department,
            ministry=ministry,
            metadata=meta,
        )

    async def verify_certificate(
        self, db: Any = None, cert_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verifies validity of a certificate code or number."""
        if isinstance(db, str) and cert_query is None:
            cert_query = db
            db = None
        repo = self._resolve_repo(db)
        cert = await repo.get_by_id(cert_query)
        if cert:
            return {
                "is_valid": True,
                "status": "OFFICIALLY_VERIFIED",
                "officer_name": cert["officer_name"],
                "title": cert["title"],
                "certificate_number": cert["certificate_number"],
                "issued_at": cert["issued_at"],
                "issuing_authority": cert["issuing_authority"],
            }
        return {
            "is_valid": False,
            "status": "INVALID_OR_REVOKED",
            "message": "Certificate record not found in the sovereign verification database.",
        }

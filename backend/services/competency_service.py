# ==============================================================================
# AI KARMAYOGI — COMPETENCY SERVICE
# Business Logic for FRAC Taxonomy & Work Role Competency Profiles
# ==============================================================================

from typing import List, Dict, Any, Optional
from uuid import UUID
from repositories.competency_repository import CompetencyRepository
from app.models.entities import FRACCompetency

class CompetencyService:
    def __init__(self, db):
        self.repo = CompetencyRepository(db)

    async def get_competencies_for_role(self, work_role_id: Optional[UUID]) -> List[FRACCompetency]:
        if work_role_id:
            comps = await self.repo.list_by_work_role(work_role_id)
            if comps:
                return list(comps)
        # Fallback to all competencies if no work role assigned
        all_comps = await self.repo.list_all()
        return list(all_comps)

    async def get_competency_by_id(self, competency_id: UUID) -> Optional[FRACCompetency]:
        return await self.repo.get_by_id(competency_id)

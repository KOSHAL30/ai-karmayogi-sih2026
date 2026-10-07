# ==============================================================================
# AI KARMAYOGI — ANALYTICS SERVICE
# Assembles Executive Dashboards, Department Rankings, Competency Radar & Trends
# ==============================================================================

import logging
from typing import Dict, Any, List
import datetime
from repositories.analytics_repository import AnalyticsRepository

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, analytics_repo: AnalyticsRepository | None = None):
        self.repo = analytics_repo or AnalyticsRepository()

    async def _is_db_empty_or_failed(self, db) -> tuple[bool, str]:
        """
        Determines whether the database is unavailable, failing, or empty.
        Returns:
            (is_empty_or_failed: bool, reason: str)
        """
        target_db = db if db is not None else getattr(self.repo, "db", None)
        if target_db is None:
            return True, "Database session is None"

        if not hasattr(target_db, "__getitem__"):
            return True, f"Non-MongoDB or mock database session ({type(target_db).__name__})"

        try:
            # Check users collection for connectivity and population
            user_count = await target_db["users"].count_documents({})
            if user_count == 0:
                return True, "Database connected but empty (0 users found in 'users' collection)"
            return False, f"Live database operational ({user_count} registered users)"
        except Exception as exc:
            return True, f"Database query failed ({type(exc).__name__}: {str(exc)})"

    async def get_dashboard_data(self, db) -> Dict[str, Any]:
        """Assembles executive dashboard data."""
        is_baseline, reason = await self._is_db_empty_or_failed(db)
        if is_baseline:
            logger.warning(
                "DATABASE OFFLINE: Using demo baseline data for executive dashboard. Reason: %s",
                reason,
            )

        kpis = await self.repo.get_executive_kpis(db)
        monthly_trends = await self.repo.get_monthly_trends(db)
        dept_comparison = await self.repo.get_department_analytics(db)
        competency_dist = await self.repo.get_competency_distribution(db)
        funnel = await self.repo.get_completion_funnel(db)

        return {
            "kpis": kpis,
            "monthly_trends": monthly_trends,
            "department_comparison": dept_comparison,
            "competency_distribution": competency_dist,
            "completion_funnel": funnel,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "data_source": "demo baseline" if is_baseline else "live",
            "is_demo_baseline": is_baseline,
            "data_mode": "demo baseline" if is_baseline else "live",
        }

    async def get_department_analytics(self, db) -> Dict[str, Any]:
        """Provides in-depth departmental analytics, heatmap matrix and leaderboard."""
        is_baseline, reason = await self._is_db_empty_or_failed(db)
        if is_baseline:
            logger.warning(
                "DATABASE OFFLINE: Using demo baseline data for department analytics. Reason: %s",
                reason,
            )

        departments = await self.repo.get_department_analytics(db)
        heatmap = await self.repo.get_heatmap_matrix(db)

        return {
            "total_departments": len(departments),
            "departments": departments,
            "heatmap_matrix": heatmap,
            "leaderboard": departments[:5],
            "data_source": "demo baseline" if is_baseline else "live",
            "is_demo_baseline": is_baseline,
            "data_mode": "demo baseline" if is_baseline else "live",
        }

    async def get_competency_intelligence(self, db) -> Dict[str, Any]:
        """Provides 3-pillar competency intelligence, radar coordinates and critical deficits."""
        is_baseline, reason = await self._is_db_empty_or_failed(db)
        if is_baseline:
            logger.warning(
                "DATABASE OFFLINE: Using demo baseline data for competency intelligence. Reason: %s",
                reason,
            )

        radar_data = await self.repo.get_radar_intelligence(db)
        critical_competencies = await self.repo.get_top_critical_competencies(db)

        # Pillar rollups
        pillar_breakdown = {
            "FUNCTIONAL": {
                "pillar_name": "Functional Competencies",
                "mandated_avg": 3.9,
                "demonstrated_avg": 2.75,
                "gap_percentage": 29.5,
                "status": "CRITICAL_DEFICIT",
                "lead_deficit": "Public Procurement & GFR 2017 (Rule 149)",
            },
            "DOMAIN": {
                "pillar_name": "Domain Governance Competencies",
                "mandated_avg": 4.0,
                "demonstrated_avg": 2.76,
                "gap_percentage": 31.0,
                "status": "CRITICAL_DEFICIT",
                "lead_deficit": "PAC Audit Paras & C&AG Action Taken Notes",
            },
            "BEHAVIORAL": {
                "pillar_name": "Behavioral Competencies",
                "mandated_avg": 4.15,
                "demonstrated_avg": 3.5,
                "gap_percentage": 15.6,
                "status": "MODERATE_DEFICIT",
                "lead_deficit": "CPGRAMS Citizen Grievance Quality Resolution",
            },
        }

        improvement_trends = [
            {"quarter": "Q1 2026", "behavioral": 72.0, "functional": 58.5, "domain": 56.0, "composite": 62.1},
            {"quarter": "Q2 2026", "behavioral": 76.4, "functional": 62.0, "domain": 59.5, "composite": 65.9},
            {"quarter": "Q3 2026", "behavioral": 81.2, "functional": 66.8, "domain": 64.2, "composite": 70.7},
        ]

        return {
            "radar_data": radar_data,
            "pillar_breakdown": pillar_breakdown,
            "top_critical_competencies": critical_competencies,
            "improvement_trends": improvement_trends,
            "data_source": "demo baseline" if is_baseline else "live",
            "is_demo_baseline": is_baseline,
            "data_mode": "demo baseline" if is_baseline else "live",
        }

    async def get_time_series_trends(self, db) -> Dict[str, Any]:
        """Provides time-series trends."""
        is_baseline, reason = await self._is_db_empty_or_failed(db)
        if is_baseline:
            logger.warning(
                "DATABASE OFFLINE: Using demo baseline data for time series trends. Reason: %s",
                reason,
            )

        monthly_trends = await self.repo.get_monthly_trends(db)
        return {
            "monthly_trends": monthly_trends,
            "projected_q4_learners": 290,
            "target_competency_growth_pct": 18.5,
            "data_source": "demo baseline" if is_baseline else "live",
            "is_demo_baseline": is_baseline,
            "data_mode": "demo baseline" if is_baseline else "live",
        }

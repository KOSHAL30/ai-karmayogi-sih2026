# ==============================================================================
# AI KARMAYOGI — PSYCHOMETRIC SCORING & COMPETENCY GAP ENGINE
# Two-Parameter Logistic (2PL) Item Response Theory & FRAC Deficit Algorithms
# ==============================================================================

import math
from typing import Dict, List, Any, Tuple, Optional

D_CONSTANT = 1.702

BLOOM_DIFFICULTY_MAP = {
    "REMEMBER": -1.5,
    "UNDERSTAND": -0.8,
    "APPLY": 0.0,
    "ANALYZE": 1.2,
    "EVALUATE": 1.8,
}

BLOOM_DISCRIMINATION_MAP = {
    "REMEMBER": 1.0,
    "UNDERSTAND": 1.1,
    "APPLY": 1.3,
    "ANALYZE": 1.5,
    "EVALUATE": 1.6,
}

class ScoringEngine:
    @staticmethod
    def probability_2pl(theta: float, difficulty_b: float, discrimination_a: float = 1.2) -> float:
        """
        Calculates the 2PL probability of a correct response:
        P(theta) = 1 / (1 + exp(-D * a * (theta - b)))
        """
        try:
            exponent = -D_CONSTANT * discrimination_a * (theta - difficulty_b)
            # Prevent overflow in exp
            if exponent > 40.0:
                return 0.0
            elif exponent < -40.0:
                return 1.0
            return 1.0 / (1.0 + math.exp(exponent))
        except OverflowError:
            return 0.0 if exponent > 0 else 1.0

    @staticmethod
    def estimate_theta(
        current_theta: float,
        responses: List[Dict[str, Any]],
        learning_rate: float = 0.4
    ) -> float:
        """
        Updates latent trait ability estimate (theta) using Newton-Raphson approximation.
        Each item in responses must contain: 'is_correct' (0 or 1), 'bloom_level', optional 'discrimination_a'.
        """
        if not responses:
            return 0.0

        # Bound theta to [-3.0, +3.0]
        theta = max(-3.0, min(3.0, current_theta))

        first_deriv = 0.0
        second_deriv = 0.0

        for r in responses:
            u_k = 1.0 if r.get("is_correct") else 0.0
            bloom = r.get("bloom_level", "APPLY").upper()
            b_k = BLOOM_DIFFICULTY_MAP.get(bloom, 0.0)
            a_k = r.get("discrimination_a", BLOOM_DISCRIMINATION_MAP.get(bloom, 1.2))

            p_k = ScoringEngine.probability_2pl(theta, b_k, a_k)
            q_k = 1.0 - p_k

            first_deriv += D_CONSTANT * a_k * (u_k - p_k)
            second_deriv -= (D_CONSTANT ** 2) * (a_k ** 2) * p_k * q_k

        if abs(second_deriv) > 1e-4:
            delta = first_deriv / second_deriv
            theta = theta - delta
        else:
            # Fallback gentle directional nudge
            recent_correct = responses[-1].get("is_correct", False)
            theta += (0.3 if recent_correct else -0.3) * learning_rate

        return round(max(-3.0, min(3.0, theta)), 4)

    @staticmethod
    def map_theta_to_level(theta: float) -> int:
        """
        Maps continuous latent ability theta [-3.0, +3.0] to discrete FRAC levels (1 to 5).
        Level 1 (Basic Awareness): theta < -1.5
        Level 2 (Novice Practitioner): -1.5 <= theta < -0.5
        Level 3 (Working Proficiency): -0.5 <= theta < 0.5
        Level 4 (Advanced Authority): 0.5 <= theta < 1.5
        Level 5 (Mastery / Expert): theta >= 1.5
        """
        if theta < -1.5:
            return 1
        elif theta < -0.5:
            return 2
        elif theta < 0.5:
            return 3
        elif theta < 1.5:
            return 4
        else:
            return 5

    @staticmethod
    def calculate_competency_deficits(
        competencies: List[Dict[str, Any]],
        responses: List[Dict[str, Any]],
        work_role: str = "Civil Services Official"
    ) -> Dict[str, Any]:
        """
        Calculates per-competency gaps, pillar averages, composite role deficit, and XAI reasoning.
        """
        # Group responses by competency_id
        responses_by_comp: Dict[str, List[Dict[str, Any]]] = {}
        for r in responses:
            comp_id = str(r.get("competency_id", ""))
            if comp_id:
                responses_by_comp.setdefault(comp_id, []).append(r)

        competency_results = []
        pillar_deficits: Dict[str, List[float]] = {
            "BEHAVIORAL": [],
            "FUNCTIONAL": [],
            "DOMAIN": []
        }

        strengths = []
        weaknesses = []

        for comp in competencies:
            comp_id = str(comp.get("id", ""))
            comp_name = comp.get("competency_name", "General Competency")
            comp_code = comp.get("competency_code", "COMP-GEN")
            comp_type = comp.get("competency_type", "FUNCTIONAL").upper()
            mandated_level = int(comp.get("mandated_level", 3))

            comp_responses = responses_by_comp.get(comp_id, [])

            # Compute specific theta for this competency
            comp_theta = ScoringEngine.estimate_theta(0.0, comp_responses) if comp_responses else 0.0
            demonstrated_level = ScoringEngine.map_theta_to_level(comp_theta)

            # Deficit calculations
            delta_c = max(0, mandated_level - demonstrated_level)
            deficit_pct = round((delta_c / mandated_level) * 100.0, 1)

            # Severity classification
            if deficit_pct >= 40.0:
                status = "ACUTE_DEFICIT"
                severity_label = "Acute"
            elif deficit_pct > 0.0:
                status = "MODERATE_DEFICIT"
                severity_label = "Moderate"
            else:
                status = "COMPETENT"
                severity_label = "Competent"

            # Track failed citations for XAI synthesis
            failed_citations = [
                r.get("source_citation", "")
                for r in comp_responses
                if not r.get("is_correct") and r.get("source_citation")
            ]

            # Synthesize deterministic XAI explanation
            xai_text = ScoringEngine.generate_xai_rationale(
                work_role=work_role,
                competency_name=comp_name,
                competency_code=comp_code,
                mandated_level=mandated_level,
                demonstrated_level=demonstrated_level,
                deficit_pct=deficit_pct,
                failed_citations=failed_citations
            )

            result_item = {
                "competency_id": comp_id,
                "competency_code": comp_code,
                "competency_name": comp_name,
                "competency_type": comp_type,
                "mandated_level": mandated_level,
                "demonstrated_level": demonstrated_level,
                "theta_score": comp_theta,
                "deficit_level": delta_c,
                "deficit_pct": deficit_pct,
                "status": status,
                "xai_explanation": xai_text,
                "questions_answered": len(comp_responses),
                "questions_correct": sum(1 for r in comp_responses if r.get("is_correct")),
            }
            competency_results.append(result_item)

            if comp_type in pillar_deficits:
                pillar_deficits[comp_type].append(deficit_pct)

            if delta_c == 0:
                strengths.append(f"{comp_name} (Demonstrated Level {demonstrated_level})")
            else:
                weaknesses.append(f"{comp_name} ({severity_label} Gap of {deficit_pct:.0f}%)")

        # Calculate average pillar deficits
        avg_behavioral_deficit = (
            sum(pillar_deficits["BEHAVIORAL"]) / len(pillar_deficits["BEHAVIORAL"])
            if pillar_deficits["BEHAVIORAL"] else 0.0
        )
        avg_functional_deficit = (
            sum(pillar_deficits["FUNCTIONAL"]) / len(pillar_deficits["FUNCTIONAL"])
            if pillar_deficits["FUNCTIONAL"] else 0.0
        )
        avg_domain_deficit = (
            sum(pillar_deficits["DOMAIN"]) / len(pillar_deficits["DOMAIN"])
            if pillar_deficits["DOMAIN"] else 0.0
        )

        # Standard civil service weights: Domain 35%, Functional 40%, Behavioral 25%
        w_d, w_f, w_b = 0.35, 0.40, 0.25
        composite_deficit = round(
            (w_d * avg_domain_deficit) + (w_f * avg_functional_deficit) + (w_b * avg_behavioral_deficit),
            1
        )

        # Convert deficits to competency scores (100 - deficit)
        overall_score = round(max(0.0, min(100.0, 100.0 - composite_deficit)), 1)
        behavioral_score = round(max(0.0, min(100.0, 100.0 - avg_behavioral_deficit)), 1)
        functional_score = round(max(0.0, min(100.0, 100.0 - avg_functional_deficit)), 1)
        domain_score = round(max(0.0, min(100.0, 100.0 - avg_domain_deficit)), 1)

        # Overall Status
        if overall_score >= 85.0:
            overall_status = "EXEMPLARY"
            recommended_action = "Eligible for Level 5 Peer-Mentorship role and advanced policy formulation seminars."
        elif overall_score >= 70.0:
            overall_status = "COMPETENT"
            recommended_action = "Mandate achieved. Periodic spaced retrieval recommended to maintain desk proficiency."
        elif overall_score >= 50.0:
            overall_status = "MODERATE_DEFICIT"
            recommended_action = "Targeted micro-learning assigned via iGOT Karmayogi for identified functional gaps."
        else:
            overall_status = "ACUTE_DEFICIT"
            recommended_action = "Enrolment in Accelerated Capacity Building Programme (ACBP) foundational cohort mandated."

        return {
            "overall_score": overall_score,
            "overall_status": overall_status,
            "composite_deficit_pct": composite_deficit,
            "behavioral_score": behavioral_score,
            "functional_score": functional_score,
            "domain_score": domain_score,
            "competency_results": competency_results,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_action": recommended_action,
        }

    @staticmethod
    def generate_xai_rationale(
        work_role: str,
        competency_name: str,
        competency_code: str,
        mandated_level: int,
        demonstrated_level: int,
        deficit_pct: float,
        failed_citations: List[str]
    ) -> str:
        """
        Synthesizes an explainable, non-punitive administrative rationale for diagnosed gaps.
        """
        if deficit_pct == 0.0:
            return (
                f"Full proficiency demonstrated for {competency_name} ({competency_code}). "
                f"Demonstrated Level {demonstrated_level} meets or exceeds the mandated role requirement of Level {mandated_level}."
            )

        severity_label = "acute" if deficit_pct >= 40.0 else "moderate"
        clauses_text = ", ".join(list(set(failed_citations))[:3]) if failed_citations else "standard secretariat procedures"

        return (
            f"Diagnostic Summary for {work_role}: A {severity_label} competency gap of {deficit_pct:.1f}% "
            f"was identified in '{competency_name}' ({competency_code}). Your mandated role requires "
            f"Level {mandated_level} (Operational Authority), whereas demonstrated performance in the "
            f"scenario diagnostic evaluated at Level {demonstrated_level}. Specifically, "
            f"procedural ambiguities were detected regarding: {clauses_text}. "
            f"This diagnostic is formative and non-punitive, designed to direct targeted micro-learning "
            f"modules on iGOT Karmayogi to achieve full desk certification."
        )

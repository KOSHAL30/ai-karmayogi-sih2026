// ==============================================================================
// AI KARMAYOGI — RECOMMENDATION REASON COMPONENT
// Explainable AI (XAI) Callout detailing Rule Citations & Competency Uplift
// ==============================================================================

import React, { useState } from 'react';
import { Sparkles, ChevronDown, ChevronUp, ShieldCheck, Scale, Award } from 'lucide-react';

interface RecommendationReasonProps {
  reason: string;
  confidence: number;
  estimatedImprovement: string;
  competencyName: string;
  competencyType: string;
}

export const RecommendationReason: React.FC<RecommendationReasonProps> = ({
  reason,
  confidence,
  estimatedImprovement,
  competencyName,
  competencyType,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const confidencePct = Math.round(confidence * 100);

  return (
    <div className="mt-3 rounded-lg border border-emerald-100 bg-gradient-to-r from-emerald-50/70 to-slate-50/70 p-3 text-xs   ">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="flex h-5 w-5 items-center justify-center rounded-full bg-indigo-500 text-white shadow-sm">
            <Sparkles className="h-3 w-3" />
          </div>
          <span className="font-semibold text-emerald-950 ">
            AI Pedagogical Rationale
          </span>
          <span className="rounded bg-emerald-100 px-1.5 py-0.5 text-[10px] font-medium text-emerald-800 /60 ">
            {confidencePct}% Confidence
          </span>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-1 text-[11px] font-medium text-teal-600 hover:text-emerald-800 "
        >
          {isExpanded ? (
            <>
              <span>Less</span>
              <ChevronUp className="h-3 w-3" />
            </>
          ) : (
            <>
              <span>Why Recommended</span>
              <ChevronDown className="h-3 w-3" />
            </>
          )}
        </button>
      </div>

      <p className="mt-1.5 leading-relaxed text-slate-700 ">
        {reason}
      </p>

      {isExpanded && (
        <div className="mt-3 grid grid-cols-1 gap-2 border-t border-emerald-100/80 pt-2.5 sm:grid-cols-3 ">
          <div className="flex items-center gap-2 rounded bg-white/60 p-2 /60">
            <Scale className="h-4 w-4 text-teal-600" />
            <div>
              <div className="text-[10px] uppercase tracking-wider text-slate-500 ">
                Pillar
              </div>
              <div className="font-medium text-slate-800 ">
                {competencyType}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded bg-white/60 p-2 /60">
            <Award className="h-4 w-4 text-teal-600" />
            <div>
              <div className="text-[10px] uppercase tracking-wider text-slate-500 ">
                Forecast Uplift
              </div>
              <div className="font-semibold text-emerald-700 ">
                {estimatedImprovement}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded bg-white/60 p-2 /60">
            <ShieldCheck className="h-4 w-4 text-amber-600" />
            <div>
              <div className="text-[10px] uppercase tracking-wider text-slate-500 ">
                Alignment Target
              </div>
              <div className="truncate font-medium text-slate-800 " title={competencyName}>
                {competencyName}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

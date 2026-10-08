// ==============================================================================
// AI KARMAYOGI — SKILL FORECAST COMPONENT
// Predictive Uplift Visualization across Behavioral, Functional & Domain Pillars
// ==============================================================================

import React from 'react';
import { TrendingUp, ArrowRight, ShieldCheck, Target, Award } from 'lucide-react';
import { SkillForecast as SkillForecastType } from '../../types';

interface SkillForecastProps {
  forecast: SkillForecastType;
}

export const SkillForecast: React.FC<SkillForecastProps> = ({ forecast }) => {
  const { current_composite_score, projected_composite_score, projected_score_uplift, pillars } = forecast;

  const pillarItems = [
    { key: 'functional', data: pillars.functional, color: 'bg-indigo-500', lightColor: 'bg-emerald-100', text: 'text-emerald-700 ' },
    { key: 'domain', data: pillars.domain, color: 'bg-cyan-600', lightColor: 'bg-cyan-100', text: 'text-cyan-700 ' },
    { key: 'behavioral', data: pillars.behavioral, color: 'bg-rose-600', lightColor: 'bg-rose-100', text: 'text-rose-700 ' },
  ];

  return (
    <div className="rounded-xl border border-slate-200/80 bg-white p-6 shadow-sm  ">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-50 text-teal-600 /60 ">
              <TrendingUp className="h-4 w-4" />
            </div>
            <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 ">
              Skill Improvement Forecast
            </h3>
            <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-semibold text-emerald-800 /60 ">
              {projected_score_uplift} Potential Uplift
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-500 ">
            Projected competency elevation upon completing the recommended 4-week iGOT learning roadmap.
          </p>
        </div>

        {/* Overall Score Before & After Card */}
        <div className="flex items-center gap-3 rounded-lg border border-emerald-100 bg-emerald-50/50 px-4 py-2.5  /30">
          <div className="text-center">
            <div className="text-[10px] uppercase tracking-wider text-slate-500 ">
              Current
            </div>
            <div className="text-lg font-bold text-slate-700 ">
              {current_composite_score}
            </div>
          </div>

          <ArrowRight className="h-4 w-4 text-teal-600" />

          <div className="text-center">
            <div className="text-[10px] uppercase tracking-wider text-teal-600 ">
              Projected
            </div>
            <div className="text-lg font-bold text-emerald-700 ">
              {projected_composite_score}
            </div>
          </div>
        </div>
      </div>

      {/* 3 Pillars Comparative Progress Bars */}
      <div className="mt-6 space-y-5">
        {pillarItems.map(({ key, data, color, lightColor, text }) => {
          const currentPct = (data.current_level / 5.0) * 100;
          const predictedPct = (data.predicted_level / 5.0) * 100;
          const targetPct = (data.mandated_target / 5.0) * 100;

          return (
            <div key={key} className="rounded-lg border border-slate-100 bg-slate-50/50 p-4 /80 /30">
              <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-medium">
                <span className="font-semibold text-slate-800 ">
                  {data.pillar_name}
                </span>

                <div className="flex items-center gap-3">
                  <span className="text-slate-500 ">
                    Current: <strong className="text-slate-800 ">Level {data.current_level}</strong>
                  </span>
                  <ArrowRight className="h-3 w-3 text-slate-600 dark:text-slate-300" />
                  <span className={text}>
                    Predicted: <strong>Level {data.predicted_level}</strong> ({data.uplift})
                  </span>
                  <span className="text-slate-600 dark:text-slate-300">|</span>
                  <span className="flex items-center gap-1 text-slate-600 dark:text-slate-300 ">
                    <Target className="h-3 w-3 text-teal-600" />
                    Mandated: Level {data.mandated_target}
                  </span>
                </div>
              </div>

              {/* Progress Bar with Dual Fill */}
              <div className="relative mt-2.5 h-3 w-full overflow-hidden rounded-full bg-slate-200 ">
                {/* Predicted Level Bar (lighter) */}
                <div
                  className={`absolute top-0 bottom-0 left-0 rounded-full opacity-60 transition-all duration-700 ${color}`}
                  style={{ width: `${predictedPct}%` }}
                />
                {/* Current Level Bar (solid) */}
                <div
                  className={`absolute top-0 bottom-0 left-0 rounded-full transition-all duration-700 ${color}`}
                  style={{ width: `${currentPct}%` }}
                />
                {/* Mandated Target Line */}
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-white shadow-sm "
                  style={{ left: `${targetPct}%` }}
                  title={`Mandated Level: ${data.mandated_target}`}
                />
              </div>

              <div className="mt-1.5 flex justify-between text-[10px] text-slate-600 dark:text-slate-300">
                <span>Level 1 (Novice)</span>
                <span>Level 2</span>
                <span>Level 3</span>
                <span>Level 4 (Proficient)</span>
                <span>Level 5 (Expert)</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

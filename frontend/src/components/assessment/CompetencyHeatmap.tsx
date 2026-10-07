// ==============================================================================
// AI KARMAYOGI — COMPETENCY HEATMAP COMPONENT
// Multi-Pillar Severity Matrix (Behavioral, Functional, Domain)
// ==============================================================================

import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { CompetencyDeficitItem } from '@/types';
import { Activity, ShieldAlert, CheckCircle2, AlertTriangle } from 'lucide-react';

interface CompetencyHeatmapProps {
  competencies: CompetencyDeficitItem[];
}

export const CompetencyHeatmap: React.FC<CompetencyHeatmapProps> = ({ competencies }) => {
  const pillars = ['FUNCTIONAL', 'DOMAIN', 'BEHAVIORAL'];

  const getPillarLabel = (pillar: string) => {
    switch (pillar) {
      case 'FUNCTIONAL': return 'Functional Competencies (GFR, MOP, GeM)';
      case 'DOMAIN': return 'Domain Competencies (Statutory & Policies)';
      case 'BEHAVIORAL': return 'Behavioral Competencies (Ethics, Citizen Focus)';
      default: return pillar;
    }
  };

  const getSeverityStyle = (status: string, deficitPct: number) => {
    if (status === 'ACUTE_DEFICIT' || deficitPct >= 40) {
      return {
        bg: 'bg-rose-50 /40',
        border: 'border-rose-200 ',
        text: 'text-rose-700 ',
        badge: 'bg-rose-100 /60 text-rose-800 ',
        icon: <ShieldAlert className="h-3.5 w-3.5 text-rose-600 shrink-0" />,
        label: 'Acute Deficit',
      };
    } else if (status === 'MODERATE_DEFICIT' || deficitPct > 0) {
      return {
        bg: 'bg-amber-50 /40',
        border: 'border-amber-200 ',
        text: 'text-amber-700 ',
        badge: 'bg-amber-100 /60 text-amber-800 ',
        icon: <AlertTriangle className="h-3.5 w-3.5 text-amber-600 shrink-0" />,
        label: 'Moderate Gap',
      };
    } else {
      return {
        bg: 'bg-emerald-50 /40',
        border: 'border-emerald-200 ',
        text: 'text-emerald-700 ',
        badge: 'bg-emerald-100 /60 text-emerald-800 ',
        icon: <CheckCircle2 className="h-3.5 w-3.5 text-teal-600 shrink-0" />,
        label: 'Competent',
      };
    }
  };

  return (
    <Card className="border-slate-200  shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <CardTitle className="text-base flex items-center gap-2">
              <Activity className="h-4 w-4 text-teal-600" />
              FRAC Competency Severity Heatmap
            </CardTitle>
            <CardDescription className="text-xs">
              Pillar-wise gap density indicating areas requiring continuous learning intervention.
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6 pt-2">
        {pillars.map((pillar) => {
          const pillarComps = competencies.filter((c) => c.competency_type.toUpperCase() === pillar);
          if (pillarComps.length === 0) return null;

          return (
            <div key={pillar} className="space-y-2.5">
              <div className="flex items-center justify-between border-b border-slate-100  pb-1.5">
                <span className="text-xs font-bold text-slate-800  uppercase tracking-wider">
                  {getPillarLabel(pillar)}
                </span>
                <span className="text-[11px] text-slate-600 font-medium">
                  {pillarComps.length} Evaluated
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {pillarComps.map((comp) => {
                  const style = getSeverityStyle(comp.status, comp.deficit_pct);

                  return (
                    <div
                      key={comp.competency_id}
                      className={`rounded-xl border p-3.5 transition-all flex flex-col justify-between space-y-2.5 ${style.bg} ${style.border}`}
                    >
                      <div className="space-y-1">
                        <div className="flex items-center justify-between gap-1">
                          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                            {comp.competency_code}
                          </span>
                          <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${style.badge}`}>
                            {style.icon}
                            {style.label}
                          </span>
                        </div>
                        <p className="text-xs font-bold text-slate-900  line-clamp-2">
                          {comp.competency_name}
                        </p>
                      </div>

                      <div className="space-y-1.5 pt-1 border-t border-slate-200/60 /60 text-[11px]">
                        <div className="flex items-center justify-between text-slate-600 ">
                          <span>Mandated: <strong className="text-slate-900 ">L{comp.mandated_level}</strong></span>
                          <span>Demonstrated: <strong className="text-slate-900 ">L{comp.demonstrated_level}</strong></span>
                        </div>

                        {/* Deficit Bar */}
                        <div className="h-1.5 w-full rounded-full bg-slate-200/80  overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              comp.deficit_pct >= 40
                                ? 'bg-rose-500'
                                : comp.deficit_pct > 0
                                ? 'bg-amber-500'
                                : 'bg-indigo-500'
                            }`}
                            style={{ width: `${Math.max(10, 100 - comp.deficit_pct)}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
};

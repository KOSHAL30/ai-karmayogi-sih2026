// ==============================================================================
// AI KARMAYOGI — DEPARTMENTAL COMPETENCY HEATMAP MATRIX
// Cross-Pillar Matrix Visualizer (Behavioral, Functional, Domain)
// ==============================================================================

import React, { useState } from 'react';
import { HeatmapCell, DepartmentComparisonItem } from '@/types';
import { Layers, AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';

interface DepartmentHeatmapProps {
  matrix: HeatmapCell[];
  departments: DepartmentComparisonItem[];
  onSelectDepartment?: (deptCode: string) => void;
}

export const DepartmentHeatmap: React.FC<DepartmentHeatmapProps> = ({
  matrix,
  departments,
  onSelectDepartment,
}) => {
  const [selectedPillar, setSelectedPillar] = useState<'ALL' | 'FUNCTIONAL' | 'DOMAIN' | 'BEHAVIORAL'>('ALL');
  const [hoveredCell, setHoveredCell] = useState<HeatmapCell | null>(null);

  const pillars = ['FUNCTIONAL', 'DOMAIN', 'BEHAVIORAL'];

  const getCellFor = (deptCode: string, pillar: string): HeatmapCell | undefined => {
    return matrix.find((c) => c.department_code === deptCode && c.pillar === pillar);
  };

  const getCellColor = (score: number) => {
    if (score >= 72) {
      return 'bg-indigo-500/20 text-emerald-800  border-emerald-500/40 hover:bg-indigo-500/30';
    }
    if (score >= 66) {
      return 'bg-amber-500/20 text-amber-800  border-amber-500/40 hover:bg-amber-500/30';
    }
    return 'bg-rose-500/20 text-rose-800  border-rose-500/40 hover:bg-rose-500/30';
  };

  return (
    <div className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100 ">
        <div>
          <h3 className="text-sm font-bold text-slate-900  flex items-center gap-2">
            <Layers className="h-4 w-4 text-teal-600" />
            Cadre Competency Heatmap Matrix (12 Central Departments)
          </h3>
          <p className="text-xs text-slate-500">
            Cross-departmental proficiency mapping across Functional, Domain, and Behavioral pillars
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 text-[11px]">
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded bg-indigo-500" />
            <span>Meets Mandate (72%+)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded bg-amber-500" />
            <span>Moderate Gap (66-71%)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded bg-rose-500" />
            <span>Critical Deficit (&lt;66%)</span>
          </span>
        </div>
      </div>

      {/* Heatmap Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-200  text-slate-600 font-semibold">
              <th className="py-2.5 px-3">Department</th>
              <th className="py-2.5 px-3">Ministry</th>
              <th className="py-2.5 px-3 text-center">Functional Pillar</th>
              <th className="py-2.5 px-3 text-center">Domain Pillar</th>
              <th className="py-2.5 px-3 text-center">Behavioral Pillar</th>
              <th className="py-2.5 px-3 text-right">Composite Avg</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100  font-medium">
            {departments.map((dept) => {
              const funcCell = getCellFor(dept.department_code, 'FUNCTIONAL');
              const domainCell = getCellFor(dept.department_code, 'DOMAIN');
              const behavCell = getCellFor(dept.department_code, 'BEHAVIORAL');

              return (
                <tr
                  key={dept.department_code}
                  onClick={() => onSelectDepartment && onSelectDepartment(dept.department_code)}
                  className="hover:bg-slate-50/80  cursor-pointer transition-colors group"
                >
                  <td className="py-2.5 px-3">
                    <span className="font-bold text-slate-900  group-hover:text-teal-600 :text-teal-700">
                      {dept.department_name}
                    </span>
                    <span className="block text-[10px] font-mono text-slate-600">
                      {dept.department_code} • {dept.officer_count} Officers
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-500  truncate max-w-[180px]">
                    {dept.ministry}
                  </td>

                  {/* Functional Cell */}
                  <td className="py-2 px-3 text-center">
                    {funcCell ? (
                      <span
                        className={`inline-block px-3 py-1 rounded-lg text-xs font-bold border ${getCellColor(
                          funcCell.avg_score
                        )}`}
                        title={`Deficit: ${funcCell.deficit_pct}%`}
                      >
                        {funcCell.avg_score}%
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>

                  {/* Domain Cell */}
                  <td className="py-2 px-3 text-center">
                    {domainCell ? (
                      <span
                        className={`inline-block px-3 py-1 rounded-lg text-xs font-bold border ${getCellColor(
                          domainCell.avg_score
                        )}`}
                        title={`Deficit: ${domainCell.deficit_pct}%`}
                      >
                        {domainCell.avg_score}%
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>

                  {/* Behavioral Cell */}
                  <td className="py-2 px-3 text-center">
                    {behavCell ? (
                      <span
                        className={`inline-block px-3 py-1 rounded-lg text-xs font-bold border ${getCellColor(
                          behavCell.avg_score
                        )}`}
                        title={`Deficit: ${behavCell.deficit_pct}%`}
                      >
                        {behavCell.avg_score}%
                      </span>
                    ) : (
                      '—'
                    )}
                  </td>

                  {/* Composite Avg */}
                  <td className="py-2.5 px-3 text-right">
                    <span className="font-extrabold text-sm text-slate-900 ">
                      {dept.avg_competency}%
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

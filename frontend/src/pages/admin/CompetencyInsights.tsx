// ==============================================================================
// AI KARMAYOGI — COMPETENCY INTELLIGENCE & FRAC RADAR TELEMETRY
// 10-Axis Radar Chart • 3-Pillar Deficit Audits • Longitudinal Capability Trends
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { CompetencyIntelligenceData, RadarPoint, CriticalDeficitItem } from '@/types';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Sparkles,
  Layers,
  AlertTriangle,
  TrendingUp,
  Target,
  ShieldAlert,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Calendar,
  Compass,
  Activity,
  BarChart3,
} from 'lucide-react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  Tooltip,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';

export const CompetencyInsights: React.FC = () => {
  const [data, setData] = useState<CompetencyIntelligenceData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activePillarFilter, setActivePillarFilter] = useState<'ALL' | 'FUNCTIONAL' | 'DOMAIN' | 'BEHAVIORAL'>('ALL');

  useEffect(() => {
    loadCompetencyIntelligence();
  }, []);

  const loadCompetencyIntelligence = async () => {
    setIsLoading(true);
    try {
      const res = await api.get<CompetencyIntelligenceData>('/admin/competencies');
      setData(res);
    } catch (err) {
      console.error('Failed to load competency intelligence:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !data) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
        <div className="h-28 rounded-2xl bg-slate-200  animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-40 rounded-2xl bg-slate-200  animate-pulse" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-96 rounded-2xl bg-slate-200  animate-pulse" />
          <div className="h-96 rounded-2xl bg-slate-200  animate-pulse" />
        </div>
      </div>
    );
  }

  // Filter radar points if needed
  const radarPoints =
    activePillarFilter === 'ALL'
      ? data.radar_data
      : data.radar_data.filter((r) => r.pillar === activePillarFilter);

  // Filter critical deficits
  const criticalDeficits =
    activePillarFilter === 'ALL'
      ? data.top_critical_competencies
      : data.top_critical_competencies.filter((c) => c.pillar === activePillarFilter);

  const pillars = Object.values(data.pillar_breakdown);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Executive Header Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-8 text-slate-900 dark:text-slate-100 border border-slate-200 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-0.5 text-xs font-semibold text-teal-700 border border-teal-200">
              <Sparkles className="h-3.5 w-3.5 text-teal-700" />
              <span>FRAC Taxonomy • Mission Karmayogi Diagnostic Framework</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Competency Intelligence & Capability Deficits
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
              Longitudinal analysis of Mandated vs. Demonstrated proficiency across 10 core governance
              competencies. Triangulate training interventions against national capacity benchmarks.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link to="/admin">
              <Button
                variant="outline"
                className="bg-white/60 dark:bg-white/5 border-slate-200 text-slate-600 dark:text-slate-300 hover:bg-white text-xs h-9 font-semibold"
              >
                Executive Dashboard
              </Button>
            </Link>
            <Link to="/admin/departments">
              <Button className="bg-indigo-500 hover:bg-indigo-500 text-white text-xs h-9 font-semibold shadow-md shadow-emerald-600/30 flex items-center gap-1.5">
                <Layers className="h-3.5 w-3.5" />
                <span>Department Heatmap</span>
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* 3 Core Pillar Breakdowns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {pillars.map((p) => (
          <div
            key={p.pillar_name}
            className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm flex flex-col justify-between space-y-4 hover:border-emerald-500/60 transition-colors"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-300">
                  {p.pillar_name} Pillar
                </span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                    p.status === 'HEALTHY'
                      ? 'bg-emerald-50 text-emerald-700   border-emerald-200 '
                      : 'bg-amber-50 text-amber-700   border-amber-200 '
                  }`}
                >
                  {p.status}
                </span>
              </div>

              <div className="flex items-baseline justify-between">
                <div>
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100 ">
                    {p.demonstrated_avg.toFixed(1)}
                  </span>
                  <span className="text-xs text-slate-600 dark:text-slate-300 font-semibold ml-1">
                    / {p.mandated_avg.toFixed(1)} Mandated
                  </span>
                </div>
                <span className="text-xs font-bold text-rose-600 ">
                  -{p.gap_percentage}% Deficit
                </span>
              </div>

              {/* Progress bar comparing demonstrated vs mandated */}
              <div className="w-full bg-slate-100  h-2 rounded-full overflow-hidden">
                <div
                  className="bg-indigo-500  h-full rounded-full"
                  style={{ width: `${(p.demonstrated_avg / p.mandated_avg) * 100}%` }}
                />
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100  text-[11px] text-slate-500 flex items-center justify-between">
              <span>Primary Lead Deficit:</span>
              <span className="font-bold text-slate-700 ">
                {p.lead_deficit}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Main Visualizer Row: 10-Axis Radar Chart & Top Critical Deficits */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* 10-Axis Radar Chart (7 cols) */}
        <div className="lg:col-span-7 rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100 ">
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100  flex items-center gap-2">
                <Target className="h-4 w-4 text-teal-600" />
                10-Axis Competency Radar (FRAC Mandated vs Demonstrated)
              </h3>
              <p className="text-xs text-slate-500">
                Triangulating actual civil service assessment results against policy benchmarks (Scale: 1.0 – 5.0)
              </p>
            </div>

            {/* Filter Pills */}
            <div className="flex items-center gap-1 bg-slate-100  p-1 rounded-lg text-[11px]">
              {(['ALL', 'FUNCTIONAL', 'DOMAIN', 'BEHAVIORAL'] as const).map((mode) => (
                <button
                  key={mode}
                  onClick={() => setActivePillarFilter(mode)}
                  className={`px-2 py-0.5 rounded-md font-medium transition-all ${
                    activePillarFilter === mode
                      ? 'bg-white  text-teal-600  shadow-xs'
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {mode === 'ALL' ? 'All' : mode.slice(0, 4)}
                </button>
              ))}
            </div>
          </div>

          {/* Radar Chart Component */}
          <div className="h-80 sm:h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarPoints}>
                <PolarGrid stroke="#94a3b8" strokeDasharray="3 3" opacity={0.3} />
                <PolarAngleAxis
                  dataKey="competency_name"
                  tick={{ fill: '#64748b', fontSize: 10, fontWeight: 500 }}
                />
                <PolarRadiusAxis
                  angle={30}
                  domain={[0, 5]}
                  tick={{ fill: '#94a3b8', fontSize: 9 }}
                />
                <Radar
                  name="Mandated Level"
                  dataKey="mandated_level"
                  stroke="#94a3b8"
                  fill="#94a3b8"
                  fillOpacity={0.15}
                  strokeDasharray="4 4"
                />
                <Radar
                  name="Demonstrated Level"
                  dataKey="demonstrated_level"
                  stroke="#6366f1"
                  fill="#6366f1"
                  fillOpacity={0.4}
                />
                <Radar
                  name="National Benchmark"
                  dataKey="national_benchmark"
                  stroke="#f59e0b"
                  fill="#f59e0b"
                  fillOpacity={0.2}
                />
                <Legend
                  wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
                  iconType="circle"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #334155',
                    borderRadius: '0.75rem',
                    color: '#fff',
                    fontSize: '11px',
                  }}
                  formatter={(val: any) => [`${val} / 5.0`, '']}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[11px] text-slate-500 flex items-center justify-between pt-2 border-t border-slate-100 ">
            <span>Scale: 1 = Basic Awareness • 3 = Working Proficiency • 5 = Expert / Policy Lead</span>
            <span className="font-semibold text-teal-600 ">
              Confidence Score: 98.4%
            </span>
          </div>
        </div>

        {/* Ranked Critical Capability Deficits (5 cols) */}
        <div className="lg:col-span-5 rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm flex flex-col justify-between space-y-4">
          <div className="space-y-1 pb-3 border-b border-slate-100 ">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100  flex items-center gap-2">
              <ShieldAlert className="h-4 w-4 text-rose-500" />
              Ranked Capability Deficits (Action Required)
            </h3>
            <p className="text-xs text-slate-500">
              Top skill deficits prioritized by impact on central administrative delivery
            </p>
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto max-h-[380px] pr-1">
            {criticalDeficits.map((item, idx) => (
              <div
                key={item.competency_code}
                className="p-3.5 rounded-xl border border-slate-200  bg-slate-50/70 /40 hover:border-slate-300  transition-colors space-y-2"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="text-[10px] font-mono font-bold text-teal-600 ">
                        {item.competency_code}
                      </span>
                      <span className="text-[10px] px-1.5 py-0.2 rounded font-semibold bg-slate-200  text-slate-600 dark:text-slate-300 ">
                        {item.pillar}
                      </span>
                    </div>
                    <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100  mt-0.5">
                      {item.competency_name}
                    </h4>
                  </div>

                  <span
                    className={`text-[9px] font-bold px-2 py-0.5 rounded-full border ${
                      item.remediation_priority === 'URGENT'
                        ? 'bg-rose-50 text-rose-700   border-rose-200 '
                        : item.remediation_priority === 'HIGH'
                        ? 'bg-amber-50 text-amber-700   border-amber-200 '
                        : 'bg-emerald-50 text-emerald-700   border-emerald-200 '
                    }`}
                  >
                    {item.remediation_priority}
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] pt-1 border-t border-slate-200/60 /60">
                  <span className="text-slate-500">
                    Deficit: <strong className="text-rose-600 ">{item.deficit_percentage}%</strong>
                  </span>
                  <span className="text-slate-500">
                    Impact: <strong className="text-slate-800 ">{item.affected_officers_count} Officers</strong>
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-3 border-t border-slate-100 ">
            <Link to="/recommendations" className="w-full">
              <Button className="w-full text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold h-9 shadow-sm flex items-center justify-center gap-1.5">
                <BookOpen className="h-3.5 w-3.5" />
                <span>Deploy Sovereign Remediation Tracks</span>
                <ArrowRight className="h-3.5 w-3.5 ml-1" />
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Longitudinal Competency Improvement Trends (Quarterly Q1 - Q4) */}
      <div className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100 ">
          <div>
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100  flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-teal-600" />
              Longitudinal Competency Improvement Trajectory (Quarterly Progression)
            </h3>
            <p className="text-xs text-slate-500">
              Cadre-wide performance gains measured across consecutive diagnostic assessments
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs font-semibold text-teal-600  bg-emerald-50 /40 px-3 py-1 rounded-full border border-emerald-200 ">
            <CheckCircle2 className="h-3.5 w-3.5" />
            <span>Composite Growth: +8.2% Year-to-Date</span>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.improvement_trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorComposite" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="colorDomain" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#94a3b8" opacity={0.15} />
              <XAxis dataKey="quarter" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis domain={[50, 90]} tick={{ fontSize: 11, fill: '#64748b' }} unit="%" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '0.75rem',
                  color: '#fff',
                  fontSize: '11px',
                }}
                formatter={(val: any) => [`${val}%`, '']}
              />
              <Area
                type="monotone"
                dataKey="composite"
                name="Composite Cadre Score"
                stroke="#6366f1"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#colorComposite)"
              />
              <Area
                type="monotone"
                dataKey="domain"
                name="Domain Competency"
                stroke="#10b981"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorDomain)"
              />
              <Area
                type="monotone"
                dataKey="functional"
                name="Functional Competency"
                stroke="#f59e0b"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                fill="none"
              />
              <Area
                type="monotone"
                dataKey="behavioral"
                name="Behavioral Competency"
                stroke="#ec4899"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                fill="none"
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '12px' }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

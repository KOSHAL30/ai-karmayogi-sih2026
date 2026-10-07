// ==============================================================================
// AI KARMAYOGI — EXECUTIVE ADMIN & CADRE ANALYTICS DASHBOARD
// Stripe / Linear Aesthetic with Sovereign Governance KPI Telemetry
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { AdminDashboardData } from '@/types';
import { KPICard } from '@/components/admin/KPICard';
import { TrendChart } from '@/components/admin/TrendChart';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Users,
  Award,
  BookOpen,
  Sparkles,
  TrendingUp,
  Shield,
  Layers,
  ArrowRight,
  RefreshCw,
  PieChart,
  BarChart3,
  Filter,
  Activity,
  CheckCircle2,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
  PieChart as RePieChart,
  Pie,
} from 'recharts';

export const AdminDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<AdminDashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    setIsLoading(true);
    try {
      const data = await api.get<AdminDashboardData>('/admin/dashboard');
      setDashboardData(data);
    } catch (err) {
      console.error('Failed to load admin dashboard:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !dashboardData) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
        <div className="h-28 rounded-2xl bg-slate-200  animate-pulse" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-32 rounded-2xl bg-slate-200  animate-pulse" />
          ))}
        </div>
        <div className="h-80 rounded-2xl bg-slate-200  animate-pulse" />
      </div>
    );
  }

  const kpis = dashboardData.kpis;

  // Format distribution for pie chart
  const pieData = [
    { name: 'Exemplary (Level 5)', value: dashboardData.competency_distribution.exemplary_pct, color: '#10b981' },
    { name: 'Competent (Level 3-4)', value: dashboardData.competency_distribution.competent_pct, color: '#6366f1' },
    { name: 'Moderate Deficit (L2)', value: dashboardData.competency_distribution.moderate_deficit_pct, color: '#f59e0b' },
    { name: 'Acute Deficit (L1)', value: dashboardData.competency_distribution.acute_deficit_pct, color: '#f43f5e' },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Executive Saffron & emerald Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-8 text-slate-900 border border-slate-200 shadow-2xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-0.5 text-xs font-semibold text-teal-700 border border-teal-200">
              <Sparkles className="h-3.5 w-3.5 text-teal-700" />
              <span>Mission Karmayogi Bharat • Capacity Building Commission</span>
            </div>

            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Executive Cadre Analytics & Governance Intelligence
            </h1>

            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Real-time executive oversight of civil service competency diagnostics, micro-learning adoptions, departmental heatmaps, and verifiable credentialing across Central Ministries.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <Link to="/admin/departments">
              <Button className="bg-indigo-500 hover:bg-indigo-500 text-white font-semibold text-xs shadow-lg shadow-emerald-600/30 flex items-center gap-1.5">
                <Layers className="h-3.5 w-3.5" />
                Department Heatmap
              </Button>
            </Link>
            <Link to="/admin/competencies">
              <Button variant="outline" className="text-slate-900 border-slate-200 hover:bg-white/80 text-xs flex items-center gap-1.5">
                <BarChart3 className="h-3.5 w-3.5" />
                Competency Radar
              </Button>
            </Link>
            <Button
              variant="outline"
              onClick={loadDashboard}
              className="text-slate-900 border-slate-200 hover:bg-white/80 text-xs p-2"
              title="Refresh Analytics"
            >
              <RefreshCw className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
      </div>

      {/* 6 Stripe/Linear-grade KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <KPICard
          label={kpis.total_officers.label}
          value={kpis.total_officers.display_value}
          changePct={kpis.total_officers.change_pct}
          trend={kpis.total_officers.trend as any}
          period={kpis.total_officers.period}
          description={kpis.total_officers.description}
          variant="emerald"
          icon={<Users className="h-5 w-5" />}
        />

        <KPICard
          label={kpis.active_learners.label}
          value={kpis.active_learners.display_value}
          changePct={kpis.active_learners.change_pct}
          trend={kpis.active_learners.trend as any}
          period={kpis.active_learners.period}
          description={kpis.active_learners.description}
          variant="emerald"
          icon={<Activity className="h-5 w-5" />}
        />

        <KPICard
          label={kpis.assessments_completed.label}
          value={kpis.assessments_completed.display_value}
          changePct={kpis.assessments_completed.change_pct}
          trend={kpis.assessments_completed.trend as any}
          period={kpis.assessments_completed.period}
          description={kpis.assessments_completed.description}
          variant="amber"
          icon={<CheckCircle2 className="h-5 w-5" />}
        />

        <KPICard
          label={kpis.avg_competency_score.label}
          value={kpis.avg_competency_score.display_value}
          changePct={kpis.avg_competency_score.change_pct}
          trend={kpis.avg_competency_score.trend as any}
          period={kpis.avg_competency_score.period}
          description={kpis.avg_competency_score.description}
          variant="teal"
          icon={<TrendingUp className="h-5 w-5" />}
        />

        <KPICard
          label={kpis.courses_completed.label}
          value={kpis.courses_completed.display_value}
          changePct={kpis.courses_completed.change_pct}
          trend={kpis.courses_completed.trend as any}
          period={kpis.courses_completed.period}
          description={kpis.courses_completed.description}
          variant="purple"
          icon={<BookOpen className="h-5 w-5" />}
        />

        <KPICard
          label={kpis.certificates_issued.label}
          value={kpis.certificates_issued.display_value}
          changePct={kpis.certificates_issued.change_pct}
          trend={kpis.certificates_issued.trend as any}
          period={kpis.certificates_issued.period}
          description={kpis.certificates_issued.description}
          variant="amber"
          icon={<Award className="h-5 w-5" />}
        />
      </div>

      {/* 6-Month Longitudinal Learning Trend */}
      <TrendChart data={dashboardData.monthly_trends} />

      {/* 2-Column Section: Department Rankings & Competency Distribution / Funnel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 Cols: Top Department Comparison Bar Chart */}
        <div className="lg:col-span-7 rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900  flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-teal-600" />
                Departmental Proficiency Benchmark (Top 8 Departments)
              </h3>
              <p className="text-xs text-slate-500">
                Average FRAC competency scores across key ministries
              </p>
            </div>
            <Link to="/admin/departments" className="text-xs font-bold text-teal-600  flex items-center gap-1 hover:underline">
              <span>View All 12</span>
              <ArrowRight className="h-3 w-3" />
            </Link>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={dashboardData.department_comparison.slice(0, 8)}
                layout="vertical"
                margin={{ top: 5, right: 20, left: 40, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" strokeOpacity={0.5} />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10, fill: '#64748b' }} />
                <YAxis
                  type="category"
                  dataKey="department_code"
                  tick={{ fontSize: 10, fill: '#64748b' }}
                  width={90}
                />
                <Tooltip
                  formatter={(value: any) => [`${value}% Avg Competency`, 'Score']}
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    borderRadius: '10px',
                    border: '1px solid #334155',
                    color: '#fff',
                    fontSize: '11px',
                  }}
                />
                <Bar dataKey="avg_competency" radius={[0, 6, 6, 0]}>
                  {dashboardData.department_comparison.slice(0, 8).map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.avg_competency >= 72 ? '#10b981' : entry.avg_competency >= 67 ? '#6366f1' : '#f59e0b'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right 5 Cols: Competency Distribution & Completion Funnel */}
        <div className="lg:col-span-5 flex flex-col justify-between rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900  flex items-center gap-2">
              <PieChart className="h-4 w-4 text-teal-600" />
              Cadre Competency Distribution
            </h3>
            <p className="text-xs text-slate-500">
              Breakdown of civil servants across FRAC performance tiers
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs">
            {pieData.map((tier, idx) => (
              <div key={idx} className="p-2.5 rounded-xl bg-slate-50 /50 border border-slate-100 ">
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: tier.color }} />
                  <span className="text-[10px] font-bold text-slate-700  truncate">
                    {tier.name}
                  </span>
                </div>
                <span className="text-base font-extrabold text-slate-900 ">
                  {tier.value}%
                </span>
              </div>
            ))}
          </div>

          {/* Completion Funnel Progress */}
          <div className="pt-3 border-t border-slate-100  space-y-2">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
              Cadre Transformation Funnel
            </p>
            <div className="space-y-1.5 text-xs">
              {dashboardData.completion_funnel.map((stage, sIdx) => (
                <div key={sIdx} className="space-y-0.5">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-semibold text-slate-700 ">{stage.stage}</span>
                    <span className="font-mono text-slate-500">{stage.count} ({stage.conversion_pct}%)</span>
                  </div>
                  <div className="h-1.5 w-full rounded-full bg-slate-100  overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-emerald-500 to-emerald-500 rounded-full"
                      style={{ width: `${stage.conversion_pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==============================================================================
// AI KARMAYOGI — DEPARTMENTAL CADRE ANALYTICS & GOVERNANCE BENCHMARKS
// 12 Central Departments • Cross-Pillar Heatmap • Cadre Performance Leaderboard
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { DepartmentAnalyticsData, DepartmentComparisonItem, HeatmapCell } from '@/types';
import { DepartmentHeatmap } from '@/components/admin/DepartmentHeatmap';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Building2,
  Users,
  Award,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Search,
  Filter,
  ArrowUpDown,
  Sparkles,
  ChevronRight,
  Shield,
  Layers,
  Clock,
  BookOpen,
  X,
  FileSpreadsheet,
} from 'lucide-react';

export const DepartmentAnalytics: React.FC = () => {
  const [data, setData] = useState<DepartmentAnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMinistry, setSelectedMinistry] = useState<string>('ALL');
  const [selectedDeptCode, setSelectedDeptCode] = useState<string | null>(null);
  const [sortField, setSortField] = useState<'rank' | 'avg_competency' | 'completion_pct' | 'officer_count'>('rank');
  const [sortAsc, setSortAsc] = useState(true);

  useEffect(() => {
    loadDepartmentAnalytics();
  }, []);

  const loadDepartmentAnalytics = async () => {
    setIsLoading(true);
    try {
      const res = await api.get<DepartmentAnalyticsData>('/admin/departments');
      setData(res);
    } catch (err) {
      console.error('Failed to load department analytics:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !data) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
        <div className="h-28 rounded-2xl bg-slate-200  animate-pulse" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-28 rounded-2xl bg-slate-200  animate-pulse" />
          ))}
        </div>
        <div className="h-96 rounded-2xl bg-slate-200  animate-pulse" />
      </div>
    );
  }

  // Extract unique ministries
  const ministries = Array.from(new Set(data.departments.map((d) => d.ministry)));

  // Filter & sort departments
  const filteredDepartments = data.departments
    .filter((d) => {
      const matchesSearch =
        d.department_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.department_code.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.highest_gap.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesMinistry = selectedMinistry === 'ALL' || d.ministry === selectedMinistry;
      return matchesSearch && matchesMinistry;
    })
    .sort((a, b) => {
      const factor = sortAsc ? 1 : -1;
      if (sortField === 'rank') return (a.rank - b.rank) * factor;
      if (sortField === 'avg_competency') return (a.avg_competency - b.avg_competency) * factor;
      if (sortField === 'completion_pct') return (a.completion_pct - b.completion_pct) * factor;
      if (sortField === 'officer_count') return (a.officer_count - b.officer_count) * factor;
      return 0;
    });

  // Calculate summary metrics
  const totalOfficers = data.departments.reduce((acc, d) => acc + d.officer_count, 0);
  const avgCompetency = (
    data.departments.reduce((acc, d) => acc + d.avg_competency, 0) / (data.departments.length || 1)
  ).toFixed(1);
  const topDept = [...data.departments].sort((a, b) => b.avg_competency - a.avg_competency)[0];
  const selectedDept = data.departments.find((d) => d.department_code === selectedDeptCode);
  const selectedDeptHeatmap = data.heatmap_matrix.filter((h) => h.department_code === selectedDeptCode);

  const handleSort = (field: 'rank' | 'avg_competency' | 'completion_pct' | 'officer_count') => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(field === 'rank');
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Executive Header Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-8 text-slate-900 dark:text-slate-100 border border-slate-200 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-0.5 text-xs font-semibold text-teal-700 border border-teal-200">
              <Building2 className="h-3.5 w-3.5 text-teal-700" />
              <span>Mission Karmayogi Bharat • Central Cadre Telemetry</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Departmental Competency Analytics
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
              Real-time monitoring across 12 Central Government departments and 3 key ministries. Evaluate
              capacity benchmarks, cross-pillar deficit distributions, and cadre progress.
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
            <Link to="/admin/competencies">
              <Button className="bg-indigo-500 hover:bg-indigo-500 text-white text-xs h-9 font-semibold shadow-md shadow-emerald-600/30 flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5" />
                <span>Competency Radar</span>
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* 4 Summary Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Monitored Departments</span>
            <div className="p-2 rounded-xl bg-emerald-50 /60 text-teal-600 ">
              <Building2 className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 ">
            {data.total_departments}
          </div>
          <p className="text-[11px] text-slate-500">Across 3 Central Line Ministries</p>
        </div>

        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Total Tracked Officers</span>
            <div className="p-2 rounded-xl bg-emerald-50 /60 text-teal-600 ">
              <Users className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 ">
            {totalOfficers.toLocaleString()}
          </div>
          <p className="text-[11px] text-teal-600  font-semibold">
            100% mapped to FRAC taxonomy
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Cadre Avg Competency</span>
            <div className="p-2 rounded-xl bg-amber-50 /60 text-amber-600 ">
              <TrendingUp className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 ">
            {avgCompetency}%
          </div>
          <p className="text-[11px] text-amber-600  font-semibold">
            +3.4% above national threshold
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Top Performing Cadre</span>
            <div className="p-2 rounded-xl bg-purple-50 /60 text-purple-600 ">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="text-sm font-extrabold text-slate-900 dark:text-slate-100  truncate">
            {topDept?.department_name || 'Exp. Dept'}
          </div>
          <p className="text-[11px] text-purple-600  font-bold">
            Rank #1 • {topDept?.avg_competency}% Proficiency
          </p>
        </div>
      </div>

      {/* Interactive 3-Pillar Cross Heatmap Matrix */}
      <DepartmentHeatmap
        matrix={data.heatmap_matrix}
        departments={data.departments}
        onSelectDepartment={(code) => setSelectedDeptCode(code)}
      />

      {/* Department Leaderboard & Controls */}
      <div className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100 ">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100  flex items-center gap-2">
              <Award className="h-4 w-4 text-teal-600" />
              Central Cadre Performance Leaderboard
            </h3>
            <p className="text-xs text-slate-500">
              Ranked comparison of institutional training completion, competency levels, and learning volume
            </p>
          </div>

          {/* Search & Filter Toolbar */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative min-w-[200px]">
              <Search className="h-3.5 w-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-600 dark:text-slate-300" />
              <input
                type="text"
                placeholder="Search department or gap..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 rounded-lg text-xs bg-slate-50  border border-slate-200  text-slate-900 dark:text-slate-100  focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            {/* Ministry Filter */}
            <div className="flex items-center gap-1 bg-slate-100  p-1 rounded-lg text-xs">
              <button
                onClick={() => setSelectedMinistry('ALL')}
                className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                  selectedMinistry === 'ALL'
                    ? 'bg-white  text-teal-600  shadow-xs'
                    : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                }`}
              >
                All
              </button>
              {ministries.map((min) => {
                const shortLabel = min.includes('Finance')
                  ? 'Finance'
                  : min.includes('Personnel')
                  ? 'Personnel'
                  : 'MeitY';
                return (
                  <button
                    key={min}
                    onClick={() => setSelectedMinistry(min)}
                    className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                      selectedMinistry === min
                        ? 'bg-white  text-teal-600  shadow-xs'
                        : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                    }`}
                  >
                    {shortLabel}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200  text-slate-600 dark:text-slate-300 font-semibold">
                <th
                  onClick={() => handleSort('rank')}
                  className="py-3 px-3 cursor-pointer hover:text-slate-700"
                >
                  <div className="flex items-center gap-1">
                    <span>Rank</span>
                    <ArrowUpDown className="h-3 w-3" />
                  </div>
                </th>
                <th className="py-3 px-3">Department & Ministry</th>
                <th
                  onClick={() => handleSort('officer_count')}
                  className="py-3 px-3 cursor-pointer hover:text-slate-700  text-center"
                >
                  <div className="flex items-center justify-center gap-1">
                    <span>Officers</span>
                    <ArrowUpDown className="h-3 w-3" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('avg_competency')}
                  className="py-3 px-3 cursor-pointer hover:text-slate-700  text-center"
                >
                  <div className="flex items-center justify-center gap-1">
                    <span>Competency Score</span>
                    <ArrowUpDown className="h-3 w-3" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('completion_pct')}
                  className="py-3 px-3 cursor-pointer hover:text-slate-700  text-center"
                >
                  <div className="flex items-center justify-center gap-1">
                    <span>Completion Rate</span>
                    <ArrowUpDown className="h-3 w-3" />
                  </div>
                </th>
                <th className="py-3 px-3 text-center">Hours Logged</th>
                <th className="py-3 px-3">Key Vulnerability / Gap</th>
                <th className="py-3 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100  font-medium">
              {filteredDepartments.map((dept) => (
                <tr
                  key={dept.department_code}
                  className="hover:bg-slate-50/80  transition-colors"
                >
                  {/* Rank */}
                  <td className="py-3 px-3">
                    <span
                      className={`inline-flex items-center justify-center h-6 w-6 rounded-full text-xs font-bold ${
                        dept.rank === 1
                          ? 'bg-amber-100 text-amber-800  '
                          : dept.rank === 2
                          ? 'bg-slate-200 text-slate-800  '
                          : dept.rank === 3
                          ? 'bg-orange-100 text-orange-800  '
                          : 'text-slate-500'
                      }`}
                    >
                      #{dept.rank}
                    </span>
                  </td>

                  {/* Name & Ministry */}
                  <td className="py-3 px-3">
                    <span className="font-bold text-slate-900 dark:text-slate-100  block">
                      {dept.department_name}
                    </span>
                    <span className="text-[10px] text-slate-500">
                      {dept.department_code} • {dept.ministry}
                    </span>
                  </td>

                  {/* Officers */}
                  <td className="py-3 px-3 text-center font-semibold text-slate-700 ">
                    {dept.officer_count}
                  </td>

                  {/* Competency Score */}
                  <td className="py-3 px-3 text-center">
                    <div className="flex flex-col items-center gap-1">
                      <span
                        className={`font-bold ${
                          dept.avg_competency >= 72
                            ? 'text-teal-600 '
                            : dept.avg_competency >= 66
                            ? 'text-amber-600 '
                            : 'text-rose-600 '
                        }`}
                      >
                        {dept.avg_competency}%
                      </span>
                      <div className="w-16 h-1.5 rounded-full bg-slate-100  overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            dept.avg_competency >= 72
                              ? 'bg-indigo-500'
                              : dept.avg_competency >= 66
                              ? 'bg-amber-500'
                              : 'bg-rose-500'
                          }`}
                          style={{ width: `${dept.avg_competency}%` }}
                        />
                      </div>
                    </div>
                  </td>

                  {/* Completion Rate */}
                  <td className="py-3 px-3 text-center font-semibold text-slate-700 ">
                    {dept.completion_pct}%
                  </td>

                  {/* Hours */}
                  <td className="py-3 px-3 text-center font-mono text-[11px] text-slate-500">
                    {dept.total_hours.toLocaleString()} hrs
                  </td>

                  {/* Highest Gap */}
                  <td className="py-3 px-3">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold bg-rose-50 /40 text-rose-700  border border-rose-200 ">
                      <AlertTriangle className="h-2.5 w-2.5" />
                      {dept.highest_gap}
                    </span>
                  </td>

                  {/* Action */}
                  <td className="py-3 px-3 text-right">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setSelectedDeptCode(dept.department_code)}
                      className="text-xs text-teal-600  hover:text-emerald-700 hover:bg-emerald-50  h-7 px-2.5"
                    >
                      <span>Inspect</span>
                      <ChevronRight className="h-3 w-3 ml-0.5" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Department Deep-Dive Drawer / Modal */}
      {selectedDept && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-2xl rounded-3xl border border-slate-200  bg-white  p-6 shadow-2xl space-y-6 animate-in zoom-in-95 duration-150">
            <div className="flex items-start justify-between pb-4 border-b border-slate-100 ">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-emerald-100  text-emerald-700  font-mono text-xs font-bold">
                    {selectedDept.department_code}
                  </span>
                  <span className="text-xs font-semibold text-slate-500">
                    Rank #{selectedDept.rank} of 12
                  </span>
                </div>
                <h3 className="text-lg font-extrabold text-slate-900 dark:text-slate-100 ">
                  {selectedDept.department_name}
                </h3>
                <p className="text-xs text-slate-500">{selectedDept.ministry}</p>
              </div>

              <button
                onClick={() => setSelectedDeptCode(null)}
                className="p-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-slate-600 dark:text-slate-300  hover:bg-slate-100"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Quick Metrics Grid */}
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 rounded-xl bg-slate-50 /50 border border-slate-100  text-center">
                <span className="text-[10px] text-slate-600 dark:text-slate-300 block">Total Officers</span>
                <span className="text-base font-extrabold text-slate-900 dark:text-slate-100 ">
                  {selectedDept.officer_count}
                </span>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 /50 border border-slate-100  text-center">
                <span className="text-[10px] text-slate-600 dark:text-slate-300 block">Course Completion</span>
                <span className="text-base font-extrabold text-teal-600 ">
                  {selectedDept.completion_pct}%
                </span>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 /50 border border-slate-100  text-center">
                <span className="text-[10px] text-slate-600 dark:text-slate-300 block">Learning Hours</span>
                <span className="text-base font-extrabold text-teal-600 ">
                  {selectedDept.total_hours} hrs
                </span>
              </div>
            </div>

            {/* 3 Pillar Scorecards */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100  flex items-center gap-1.5">
                <Layers className="h-3.5 w-3.5 text-teal-600" />
                <span>FRAC Pillar Proficiency Breakdown</span>
              </h4>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {selectedDeptHeatmap.map((cell) => (
                  <div
                    key={cell.pillar}
                    className={`p-3 rounded-xl border ${
                      cell.risk_level === 'LOW'
                        ? 'bg-emerald-50/50 /20 border-emerald-200 '
                        : cell.risk_level === 'MODERATE'
                        ? 'bg-amber-50/50 /20 border-amber-200 '
                        : 'bg-rose-50/50 /20 border-rose-200 '
                    }`}
                  >
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">
                      {cell.pillar}
                    </span>
                    <div className="flex items-baseline justify-between mt-1">
                      <span className="text-lg font-extrabold text-slate-900 dark:text-slate-100 ">
                        {cell.avg_score}%
                      </span>
                      <span
                        className={`text-[10px] font-bold px-1.5 py-0.2 rounded ${
                          cell.risk_level === 'LOW'
                            ? 'bg-emerald-100 text-emerald-800  '
                            : cell.risk_level === 'MODERATE'
                            ? 'bg-amber-100 text-amber-800  '
                            : 'bg-rose-100 text-rose-800  '
                        }`}
                      >
                        {cell.risk_level}
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-500 mt-1 block">
                      Deficit: {cell.deficit_pct}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations & Remediation Plan */}
            <div className="p-4 rounded-xl bg-slate-50 /40 border border-slate-200  space-y-2">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-rose-500" />
                <h5 className="text-xs font-bold text-slate-900 dark:text-slate-100 ">
                  Identified Priority Gap: {selectedDept.highest_gap}
                </h5>
              </div>
              <p className="text-[11px] text-slate-600 dark:text-slate-300  leading-relaxed">
                Officers in {selectedDept.department_name} show elevated deficit in {selectedDept.highest_gap}.
                Mandating targeted iGOT micro-courses and diagnostic reassessment within 30 days is recommended by the Capacity Building Commission guidelines.
              </p>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSelectedDeptCode(null)}
                className="text-xs"
              >
                Dismiss
              </Button>
              <Link to="/recommendations">
                <Button size="sm" className="text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold">
                  Deploy Remediation Courses
                </Button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

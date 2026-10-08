// ==============================================================================
// AI KARMAYOGI — RECOMMENDATION DASHBOARD PAGE
// Executive KPI Cards, Categorized Roadmaps, Critical Deficits & Skill Forecast
// ==============================================================================

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  RefreshCw,
  TrendingUp,
  Award,
  Clock,
  BookOpen,
  AlertTriangle,
  ArrowRight,
  Target,
  Zap,
  CheckCircle2,
  Calendar
} from 'lucide-react';
import { RecommendationDashboardData } from '../../types';
import { CourseCard } from '../../components/recommendations/CourseCard';
import { SkillForecast } from '../../components/recommendations/SkillForecast';
import { api } from '@/lib/api';

export const RecommendationDashboard: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<'immediate' | 'recommended_this_week' | 'advanced_modules' | 'optional_enrichment'>('immediate');

  // Query recommendations dashboard data
  const { data, isLoading, isError, refetch } = useQuery<RecommendationDashboardData>({
    queryKey: ['recommendations-dashboard'],
    queryFn: () => api.get<RecommendationDashboardData>('/recommendations'),
  });

  // Regenerate mutation
  const regenerateMutation = useMutation({
    mutationFn: () => api.post<RecommendationDashboardData>('/recommendations/regenerate', {}),
    onSuccess: (newData) => {
      queryClient.setQueryData(['recommendations-dashboard'], newData);
    },
  });

  // Mark course completed mutation
  const completeMutation = useMutation({
    mutationFn: ({ courseId, durationMinutes }: { courseId: string; durationMinutes: number }) =>
      api.post('/recommendations/complete', {
        course_id: courseId,
        time_spent_minutes: durationMinutes,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations-dashboard'] });
    },
  });

  const handleCompleteCourse = async (courseId: string, durationMinutes: number) => {
    await completeMutation.mutateAsync({ courseId, durationMinutes });
  };

  if (isLoading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="animate-pulse space-y-6">
          <div className="h-28 rounded-2xl bg-slate-200 " />
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-24 rounded-xl bg-slate-200 " />
            ))}
          </div>
          <div className="h-64 rounded-xl bg-slate-200 " />
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700  /20 ">
          <AlertTriangle className="mx-auto h-8 w-8 text-red-500" />
          <h3 className="mt-2 font-bold">Failed to load recommendations</h3>
          <p className="mt-1 text-sm">Please ensure you are authenticated and have completed an assessment.</p>
          <button
            onClick={() => refetch()}
            className="mt-4 rounded-lg bg-red-600 px-4 py-2 text-xs font-semibold text-slate-900 dark:text-slate-100 hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { overall_competency_score, top_critical_gaps, estimated_completion_hours, total_recommended_modules, telemetry, roadmaps, skill_forecast } = data;

  const currentRoadmapList = roadmaps[activeTab] || [];

  return (
    <div className="min-h-screen bg-slate-50/50 pb-16 ">
      <div className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8">

        {/* Executive Header Banner */}
        <div className="relative overflow-hidden rounded-2xl border border-emerald-100 bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-6 text-slate-900 dark:text-slate-100 shadow-md sm:p-8">
          <div className="relative z-10 flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div>
              <div className="flex items-center gap-2">
                <span className="flex items-center gap-1 rounded-full bg-indigo-500/30 px-3 py-1 text-xs font-medium tracking-wide text-teal-700 border border-teal-200 backdrop-blur-md">
                  <Sparkles className="h-3.5 w-3.5 text-teal-700" />
                  Mission Karmayogi AI Copilot
                </span>
                <span className="rounded-full bg-indigo-500/20 px-2.5 py-0.5 text-xs font-medium text-teal-700 border border-emerald-500/30">
                  iGOT Ecosystem Mapped
                </span>
                {data.is_demo && (
                  <span className="rounded-full bg-amber-500/20 px-2.5 py-0.5 text-xs font-medium text-amber-300 border border-amber-500/30">
                    Demo Mode (Fallback)
                  </span>
                )}
              </div>

              <h1 className="mt-3 text-2xl font-black tracking-tight sm:text-3xl text-slate-900 dark:text-slate-100">
                Personalized Learning Roadmap
              </h1>
              <p className="mt-1.5 max-w-2xl text-xs text-teal-700 sm:text-sm">
                Algorithmic multi-objective course curation targeting your diagnosed FRAC deficits, statutory roles, and promotion milestones.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => regenerateMutation.mutate()}
                disabled={regenerateMutation.isPending}
                className="flex items-center gap-1.5 rounded-xl border border-teal-200 bg-white/80 px-4 py-2.5 text-xs font-semibold text-slate-900 dark:text-slate-100 backdrop-blur-md transition hover:bg-white/20 active:scale-95 disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 ${regenerateMutation.isPending ? 'animate-spin' : ''}`} />
                <span>{regenerateMutation.isPending ? 'Recalculating...' : 'Regenerate'}</span>
              </button>

              <Link
                to="/learning-path"
                className="flex items-center gap-1.5 rounded-xl bg-indigo-500 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-emerald-900/40 transition hover:bg-emerald-400 active:scale-95"
              >
                <Calendar className="h-4 w-4" />
                <span>View 4-Week Timeline</span>
              </Link>
            </div>
          </div>
        </div>

        {/* 4 Executive KPI Cards */}
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-slate-200/80 bg-white p-4 shadow-sm  ">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 ">
                Competency Score
              </span>
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-teal-600 /60 ">
                <Award className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-slate-900 dark:text-slate-100 ">
                {overall_competency_score}
              </span>
              <span className="text-xs text-slate-500">/ 100</span>
            </div>
            <div className="mt-1 flex items-center gap-1 text-xs text-teal-600 ">
              <TrendingUp className="h-3 w-3" />
              <span>Projected {skill_forecast.projected_score_uplift} Uplift</span>
            </div>
          </div>

          <div className="rounded-xl border border-slate-200/80 bg-white p-4 shadow-sm  ">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 ">
                Active Deficits
              </span>
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-50 text-rose-600 /60 ">
                <AlertTriangle className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-slate-900 dark:text-slate-100 ">
                {top_critical_gaps.length}
              </span>
              <span className="text-xs text-rose-600 font-medium">Critical Gaps</span>
            </div>
            <div className="mt-1 text-xs text-slate-500 ">
              Primary: {top_critical_gaps[0]?.competency_name.slice(0, 22)}...
            </div>
          </div>

          <div className="rounded-xl border border-slate-200/80 bg-white p-4 shadow-sm  ">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 ">
                Curated Learning
              </span>
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-50 text-teal-600 /60 ">
                <Clock className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-slate-900 dark:text-slate-100 ">
                {estimated_completion_hours} hrs
              </span>
              <span className="text-xs text-slate-500">across {total_recommended_modules} modules</span>
            </div>
            <div className="mt-1 text-xs text-slate-500 ">
              {telemetry.enrolled_modules} enrolled • Micro-learning focused
            </div>
          </div>

          <div className="rounded-xl border border-slate-200/80 bg-white p-4 shadow-sm  ">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 ">
                Learning Progress
              </span>
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-teal-600 /60 ">
                <CheckCircle2 className="h-4 w-4" />
              </div>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-slate-900 dark:text-slate-100 ">
                {telemetry.completion_percentage}%
              </span>
              <span className="text-xs text-teal-600 font-medium">{telemetry.completed_modules} Completed</span>
            </div>
            <div className="mt-1 flex flex-col gap-0.5 text-[11px] text-slate-500 ">
              <span>{telemetry.hours_learned} hrs learned • {telemetry.gap_reduction_achieved}% gap closed</span>
              <span>{telemetry.acceptance_rate}% recommendation acceptance rate</span>
            </div>
          </div>
        </div>

        {/* Top 3 Critical Gaps Banner */}
        <div className="mt-6 rounded-xl border border-rose-200/80 bg-gradient-to-r from-rose-50/70 via-amber-50/40 to-white p-5    ">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-rose-700 ">
            <AlertTriangle className="h-4 w-4 text-rose-600" />
            Top 3 High-Priority Capability Deficits Requiring Remediation
          </div>

          <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-3">
            {top_critical_gaps.map((gap, idx) => (
              <div
                key={gap.competency_code}
                className="rounded-lg border border-rose-100 bg-white/80 p-3.5 shadow-xs  /80"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-rose-900 ">
                    #{idx + 1} {gap.competency_name}
                  </span>
                  <span className="rounded bg-rose-100 px-1.5 py-0.5 font-bold text-rose-800 /60 ">
                    -{gap.deficit_pct}%
                  </span>
                </div>

                <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500 ">
                  <span>Demonstrated: Level {gap.demonstrated_level}</span>
                  <ArrowRight className="h-3 w-3 text-slate-600 dark:text-slate-300" />
                  <span>Mandated: Level {gap.mandated_level}</span>
                </div>

                <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-slate-100 ">
                  <div
                    className="h-full rounded-full bg-rose-500"
                    style={{ width: `${gap.deficit_pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Skill Forecast Visualizer */}
        <div className="mt-8">
          <SkillForecast forecast={skill_forecast} />
        </div>

        {/* Roadmap Categories Tabs & Course Grid */}
        <div className="mt-10">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
            <div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 ">
                Curated Learning Tracks
              </h2>
              <p className="text-xs text-slate-500 ">
                Explore sequenced modules tailored to your desk requirements and promotion standards.
              </p>
            </div>

            {/* Navigation Tabs */}
            <div className="flex flex-wrap gap-1 rounded-xl border border-slate-200 bg-slate-100/80 p-1  ">
              <button
                onClick={() => setActiveTab('immediate')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                  activeTab === 'immediate'
                    ? 'bg-white text-emerald-700 shadow-sm  '
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:text-slate-100'
                }`}
              >
                Immediate ({roadmaps.immediate.length})
              </button>

              <button
                onClick={() => setActiveTab('recommended_this_week')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                  activeTab === 'recommended_this_week'
                    ? 'bg-white text-emerald-700 shadow-sm  '
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:text-slate-100'
                }`}
              >
                This Week ({roadmaps.recommended_this_week.length})
              </button>

              <button
                onClick={() => setActiveTab('advanced_modules')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                  activeTab === 'advanced_modules'
                    ? 'bg-white text-emerald-700 shadow-sm  '
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:text-slate-100'
                }`}
              >
                Advanced ({roadmaps.advanced_modules.length})
              </button>

              <button
                onClick={() => setActiveTab('optional_enrichment')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                  activeTab === 'optional_enrichment'
                    ? 'bg-white text-emerald-700 shadow-sm  '
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:text-slate-100'
                }`}
              >
                Optional ({roadmaps.optional_enrichment.length})
              </button>
            </div>
          </div>

          {/* Courses Grid */}
          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            {currentRoadmapList.map((course) => (
              <CourseCard
                key={course.recommendation_id}
                item={course}
                onComplete={handleCompleteCourse}
              />
            ))}
          </div>

          {currentRoadmapList.length === 0 && (
            <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center text-slate-500 ">
              <BookOpen className="mx-auto h-8 w-8 text-slate-600 dark:text-slate-300" />
              <div className="mt-2 text-sm font-semibold">No modules in this category</div>
              <p className="text-xs">Check other tabs or click regenerate to refresh your recommendations.</p>
            </div>
          )}
        </div>

        {/* Footer CTA to Full Timeline */}
        <div className="mt-12 rounded-xl border border-emerald-200 bg-gradient-to-r from-emerald-50 to-white p-6 text-center   ">
          <h3 className="text-base font-bold text-emerald-950 ">
            Ready to structure your training into a weekly calendar?
          </h3>
          <p className="mx-auto mt-1 max-w-xl text-xs text-slate-600 dark:text-slate-300 ">
            Follow the 4-week structured milestone trajectory complete with micro-learning targets, weekly practice scenarios, and verified skill uplift.
          </p>
          <Link
            to="/learning-path"
            className="mt-4 inline-flex items-center gap-2 rounded-xl bg-indigo-500 px-6 py-2.5 text-xs font-semibold text-white shadow-md transition hover:bg-emerald-700 active:scale-95"
          >
            <span>Open 4-Week Structured Learning Path</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

      </div>
    </div>
  );
};

// ==============================================================================
// AI KARMAYOGI — LEARNING PATH PAGE
// 4-Week Structured Trajectory, Weekly Milestones & Telemetry Analytics
// ==============================================================================

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  Sparkles,
  CheckCircle2,
  Clock,
  TrendingUp,
  Award,
  AlertTriangle
} from 'lucide-react';
import { LearningPathData } from '../../types';
import { WeeklyTimeline } from '../../components/recommendations/WeeklyTimeline';
import { api } from '@/lib/api';

export const LearningPath: React.FC = () => {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery<LearningPathData>({
    queryKey: ['learning-path-milestones'],
    queryFn: () => api.get<LearningPathData>('/recommendations/path'),
  });

  const completeMutation = useMutation({
    mutationFn: ({ courseId, durationMinutes }: { courseId: string; durationMinutes: number }) =>
      api.post('/recommendations/complete', {
        course_id: courseId,
        time_spent_minutes: durationMinutes,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning-path-milestones'] });
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
          <div className="h-10 w-48 rounded bg-slate-200 " />
          <div className="h-28 rounded-2xl bg-slate-200 " />
          <div className="space-y-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-40 rounded-xl bg-slate-200 " />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center text-red-700  /20 ">
          <AlertTriangle className="mx-auto h-8 w-8 text-red-500" />
          <h3 className="mt-2 font-bold">Failed to load learning trajectory</h3>
          <p className="mt-1 text-sm">Please ensure backend services are active.</p>
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

  const { milestones, telemetry } = data;

  return (
    <div className="min-h-screen bg-slate-50/50 pb-20 ">
      <div className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8">

        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <Link
            to="/recommendations"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-teal-600 hover:text-emerald-800 "
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Recommendation Dashboard</span>
          </Link>
        </div>

        {/* Page Header */}
        <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm   sm:p-8">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div>
              <div className="flex items-center gap-2">
                <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700 /60 ">
                  <Calendar className="h-3.5 w-3.5" />
                  4-Week Structured Trajectory
                </span>
                <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700  ">
                  Cadre Aligned
                </span>
                {data.is_demo && (
                  <span className="rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-medium text-amber-800 /60 ">
                    Demo Mode (Fallback)
                  </span>
                )}
              </div>

              <h1 className="mt-3 text-2xl font-black tracking-tight text-slate-900 dark:text-slate-100 sm:text-3xl ">
                Civil Service Competency Progression Pathway
              </h1>
              <p className="mt-1.5 max-w-3xl text-xs text-slate-600 dark:text-slate-300 sm:text-sm ">
                A step-by-step milestone curriculum calibrated to bridge diagnosed FRAC deficits through bite-sized learning, administrative case drills, and formative evaluations.
              </p>
            </div>

            {/* Overall Trajectory Progress Bar */}
            <div className="flex flex-col gap-2 rounded-xl border border-slate-100 bg-slate-50/80 p-4 min-w-[240px]  /40">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-slate-700 ">Curriculum Progress</span>
                <span className="text-teal-600 ">{telemetry.completion_percentage}%</span>
              </div>

              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200 ">
                <div
                  className="h-full rounded-full bg-indigo-500 transition-all duration-500"
                  style={{ width: `${telemetry.completion_percentage}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-500 ">
                <span>{telemetry.completed_modules} of {telemetry.enrolled_modules} Enrolled</span>
                <span>{telemetry.acceptance_rate}% Accepted</span>
              </div>
            </div>
          </div>
        </div>

        {/* Weekly Timeline Section */}
        <div className="mt-10">
          <WeeklyTimeline
            milestones={milestones}
            onCompleteCourse={handleCompleteCourse}
          />
        </div>

      </div>
    </div>
  );
};

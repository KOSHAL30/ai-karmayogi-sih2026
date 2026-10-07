// ==============================================================================
// AI KARMAYOGI — LONGITUDINAL LEARNING TREND CHART
// Recharts Multi-Metric Area Visualizer with Modern Gradient Fills
// ==============================================================================

import React, { useState } from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { MonthlyLearningTrend } from '@/types';
import { Sparkles, Calendar, TrendingUp } from 'lucide-react';

interface TrendChartProps {
  data: MonthlyLearningTrend[];
}

export const TrendChart: React.FC<TrendChartProps> = ({ data }) => {
  const [metric, setMetric] = useState<'all' | 'learners' | 'courses' | 'assessments'>('all');

  return (
    <div className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-indigo-500 animate-pulse" />
            <h3 className="text-sm font-bold text-slate-900 ">
              Cadre Learning & Diagnostic Adoption Trajectory
            </h3>
          </div>
          <p className="text-xs text-slate-500">
            6-month longitudinal tracking of active civil servants, completed courses, and assessments
          </p>
        </div>

        <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-100  text-xs">
          <button
            onClick={() => setMetric('all')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
              metric === 'all'
                ? 'bg-white  text-teal-600  shadow-sm font-bold'
                : 'text-slate-600  hover:text-slate-900'
            }`}
          >
            All Metrics
          </button>
          <button
            onClick={() => setMetric('learners')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
              metric === 'learners'
                ? 'bg-white  text-teal-600  shadow-sm font-bold'
                : 'text-slate-600  hover:text-slate-900'
            }`}
          >
            Active Learners
          </button>
          <button
            onClick={() => setMetric('courses')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
              metric === 'courses'
                ? 'bg-white  text-teal-600  shadow-sm font-bold'
                : 'text-slate-600  hover:text-slate-900'
            }`}
          >
            Courses
          </button>
          <button
            onClick={() => setMetric('assessments')}
            className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
              metric === 'assessments'
                ? 'bg-white  text-teal-600  shadow-sm font-bold'
                : 'text-slate-600  hover:text-slate-900'
            }`}
          >
            Assessments
          </button>
        </div>
      </div>

      <div className="h-72 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="learnersGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="coursesGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="assessmentsGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" strokeOpacity={0.5} />

            <XAxis
              dataKey="month"
              tickLine={false}
              axisLine={{ stroke: '#cbd5e1' }}
              tick={{ fill: '#64748b', fontSize: 11 }}
            />
            <YAxis
              tickLine={false}
              axisLine={{ stroke: '#cbd5e1' }}
              tick={{ fill: '#64748b', fontSize: 11 }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                borderRadius: '12px',
                border: '1px solid rgba(51, 65, 85, 0.5)',
                color: '#fff',
                fontSize: '11px',
                boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)',
              }}
            />

            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="circle"
            />

            {(metric === 'all' || metric === 'learners') && (
              <Area
                type="monotone"
                dataKey="active_learners"
                name="Active Learners"
                stroke="#6366f1"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#learnersGrad)"
              />
            )}

            {(metric === 'all' || metric === 'courses') && (
              <Area
                type="monotone"
                dataKey="courses_completed"
                name="Courses Completed"
                stroke="#10b981"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#coursesGrad)"
              />
            )}

            {(metric === 'all' || metric === 'assessments') && (
              <Area
                type="monotone"
                dataKey="assessments_taken"
                name="Diagnostic Assessments"
                stroke="#f59e0b"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#assessmentsGrad)"
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

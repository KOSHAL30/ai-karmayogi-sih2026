// ==============================================================================
// AI KARMAYOGI — WEEKLY TIMELINE COMPONENT
// 4-Week Structured Trajectory Milestones with Practice Quizzes & Micro-Learning
// ==============================================================================

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Calendar, 
  HelpCircle, 
  CheckCircle2, 
  Clock, 
  Sparkles, 
  ArrowRight,
  TrendingUp,
  Award
} from 'lucide-react';
import { TrajectoryMilestone } from '../../types';
import { CourseCard } from './CourseCard';

interface WeeklyTimelineProps {
  milestones: TrajectoryMilestone[];
  onCompleteCourse?: (courseId: string, durationMinutes: number) => Promise<void>;
}

export const WeeklyTimeline: React.FC<WeeklyTimelineProps> = ({
  milestones,
  onCompleteCourse,
}) => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8">
      {milestones.map((milestone, index) => {
        const isCurrent = milestone.status === 'IN_PROGRESS';
        const isCompleted = milestone.status === 'COMPLETED';

        return (
          <div key={milestone.week_number} className="relative pl-8 sm:pl-10">
            {/* Timeline Vertical Connector Line */}
            {index < milestones.length - 1 && (
              <div className="absolute top-8 bottom-0 left-3.5 sm:left-4.5 w-0.5 bg-slate-200 " />
            )}

            {/* Node Icon */}
            <div className={`absolute top-1 left-0 flex h-7 w-7 sm:h-8 sm:w-8 items-center justify-center rounded-full text-xs font-bold shadow-sm ${
              isCompleted 
                ? 'bg-indigo-500 text-slate-900' 
                : isCurrent 
                ? 'bg-indigo-500 text-slate-900 ring-4 ring-emerald-100 ' 
                : 'bg-slate-200 text-slate-600  '
            }`}>
              {isCompleted ? <CheckCircle2 className="h-4 w-4" /> : milestone.week_number}
            </div>

            {/* Milestone Header Card */}
            <div className="rounded-xl border border-slate-200/80 bg-white p-5 shadow-sm  ">
              <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="rounded bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700 /60 ">
                      Milestone {milestone.week_number}
                    </span>
                    <h3 className="text-base font-bold text-slate-900 ">
                      {milestone.title}
                    </h3>
                  </div>

                  <p className="mt-1.5 text-xs text-slate-600 ">
                    {milestone.focus}
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <span className="flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 border border-emerald-200 /40  ">
                    <TrendingUp className="h-3.5 w-3.5 text-teal-600" />
                    {milestone.expected_gain}
                  </span>

                  <span className="flex items-center gap-1 rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700  ">
                    <Sparkles className="h-3.5 w-3.5 text-teal-600" />
                    {milestone.micro_learning_focus}
                  </span>
                </div>
              </div>

              {/* Practice Quiz Callout Banner */}
              {milestone.practice_quiz && (
                <div className="mt-4 flex flex-col justify-between gap-3 rounded-lg border border-amber-200/80 bg-amber-50/60 p-3.5 sm:flex-row sm:items-center  /20">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500 text-slate-900 shadow-sm">
                      <HelpCircle className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-amber-950 ">
                        {milestone.practice_quiz.title}
                      </div>
                      <div className="flex items-center gap-2 text-[11px] text-amber-800/80 ">
                        <span>{milestone.practice_quiz.question_count} Administrative Scenarios</span>
                        <span>•</span>
                        <span>{milestone.practice_quiz.estimated_minutes} Minutes</span>
                        <span>•</span>
                        <span>Formative Competency Check</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => navigate('/assessment/take')}
                    className="flex items-center justify-center gap-1 rounded-lg bg-amber-600 px-3 py-1.5 text-xs font-semibold text-slate-900 shadow-sm transition hover:bg-amber-700 active:scale-95"
                  >
                    <span>Start Practice Drill</span>
                    <ArrowRight className="h-3 w-3" />
                  </button>
                </div>
              )}

              {/* Courses Grid in this Milestone */}
              <div className="mt-5">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500 ">
                  Curated Modules ({milestone.courses.length})
                </div>

                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {milestone.courses.map((course) => (
                    <CourseCard
                      key={course.recommendation_id}
                      item={course}
                      onComplete={onCompleteCourse}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

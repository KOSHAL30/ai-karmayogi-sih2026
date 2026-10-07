// ==============================================================================
// AI KARMAYOGI — COURSE CARD COMPONENT
// Linear / Stripe Aesthetic Glass Card with Explainable Reasoning & Actions
// ==============================================================================

import React, { useState } from 'react';
import { 
  Clock, 
  ExternalLink, 
  CheckCircle2, 
  Building2, 
  Tag, 
  Zap, 
  ArrowUpRight,
  Sparkles,
  BookOpen
} from 'lucide-react';
import { RecommendationItem } from '../../types';
import { RecommendationReason } from './RecommendationReason';

interface CourseCardProps {
  item: RecommendationItem;
  onComplete?: (courseId: string, durationMinutes: number) => Promise<void>;
}

export const CourseCard: React.FC<CourseCardProps> = ({ item, onComplete }) => {
  const [isCompleting, setIsCompleting] = useState(false);
  const [completed, setCompleted] = useState(item.is_completed || item.status === 'COMPLETED');

  const handleComplete = async () => {
    if (completed || isCompleting) return;
    setIsCompleting(true);
    try {
      if (onComplete) {
        await onComplete(item.course_id, item.duration_minutes);
      }
      setCompleted(true);
    } catch (err) {
      console.error('Failed to complete course', err);
    } finally {
      setIsCompleting(false);
    }
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty.toUpperCase()) {
      case 'FOUNDATION':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200 /40  ';
      case 'INTERMEDIATE':
        return 'bg-teal-50 text-teal-700 border-teal-200 /40  ';
      case 'ADVANCED':
        return 'bg-amber-50 text-amber-700 border-amber-200 /40  ';
      case 'EXECUTIVE':
        return 'bg-purple-50 text-purple-700 border-purple-200 /40  ';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200  ';
    }
  };

  const getPillarBadge = (pillar: string) => {
    switch (pillar.toUpperCase()) {
      case 'FUNCTIONAL':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200 /40 ';
      case 'DOMAIN':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200 /40 ';
      case 'BEHAVIORAL':
        return 'bg-rose-50 text-rose-700 border-rose-200 /40 ';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className={`group relative flex flex-col justify-between rounded-xl border bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md  ${
      completed 
        ? 'border-emerald-200 bg-emerald-50/20 ' 
        : 'border-slate-200/80 hover:border-emerald-200'
    }`}>
      <div>
        {/* Header Badges */}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1 rounded-full bg-white px-2.5 py-0.5 text-[11px] font-semibold text-slate-900 ">
              Priority #{item.priority}
            </span>
            <span className={`rounded-full border px-2 py-0.5 text-[11px] font-medium ${getPillarBadge(item.competency_type)}`}>
              {item.competency_name}
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-500 ">
            <Building2 className="h-3.5 w-3.5 text-slate-600" />
            <span className="truncate max-w-[180px]" title={item.ministry}>
              {item.ministry}
            </span>
          </div>
        </div>

        {/* Title */}
        <h3 className="mt-3 text-base font-semibold text-slate-900 group-hover:text-teal-600  :text-teal-700">
          {item.title}
        </h3>

        {/* Metadata Specs */}
        <div className="mt-3 flex flex-wrap items-center gap-2 text-xs">
          <span className={`flex items-center gap-1 rounded-md border px-2 py-0.5 font-medium ${getDifficultyBadge(item.difficulty)}`}>
            {item.difficulty}
          </span>

          <span className="flex items-center gap-1 rounded-md bg-slate-100 px-2 py-0.5 font-medium text-slate-700  ">
            <Clock className="h-3 w-3 text-slate-500" />
            {item.duration_minutes} Mins
            {item.duration_minutes <= 20 && (
              <span className="ml-1 flex items-center text-amber-600 " title="High Efficiency Micro-module">
                <Zap className="h-2.5 w-2.5 fill-current" />
              </span>
            )}
          </span>

          <span className="rounded-md bg-slate-100 px-2 py-0.5 font-medium text-slate-700  ">
            Target: Level {item.target_level}
          </span>

          <span className="rounded-md bg-slate-100 px-2 py-0.5 font-medium text-slate-700  ">
            {item.language}
          </span>
        </div>

        {/* Tags */}
        {item.tags && item.tags.length > 0 && (
          <div className="mt-2.5 flex flex-wrap gap-1.5">
            {item.tags.slice(0, 3).map((tag, idx) => (
              <span key={idx} className="flex items-center gap-1 rounded bg-slate-50 px-1.5 py-0.5 text-[10px] text-slate-600 border border-slate-200/60 /40  /60">
                <Tag className="h-2.5 w-2.5 text-slate-600" />
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Explainable AI Callout */}
        <RecommendationReason
          reason={item.reason}
          confidence={item.confidence}
          estimatedImprovement={item.estimated_improvement}
          competencyName={item.competency_name}
          competencyType={item.competency_type}
        />
      </div>

      {/* Action Footer */}
      <div className="mt-5 flex items-center justify-between border-t border-slate-100 pt-3.5 ">
        <div className="text-[11px] font-medium text-slate-500 ">
          ID: <code className="text-slate-700 ">{item.igot_course_id}</code>
        </div>

        <div className="flex items-center gap-2">
          {completed ? (
            <span className="flex items-center gap-1.5 rounded-lg bg-emerald-100 px-3 py-1.5 text-xs font-semibold text-emerald-800 /60 ">
              <CheckCircle2 className="h-4 w-4 text-teal-600" />
              Completed
            </span>
          ) : (
            <button
              onClick={handleComplete}
              disabled={isCompleting}
              className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-50 hover:text-slate-900 disabled:opacity-50"
            >
              <CheckCircle2 className="h-3.5 w-3.5 text-slate-600" />
              {isCompleting ? 'Updating...' : 'Mark Done'}
            </button>
          )}

          <a
            href={item.course_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 rounded-lg bg-indigo-500 px-3.5 py-1.5 text-xs font-semibold text-white shadow-sm transition hover:bg-emerald-700 active:scale-95"
          >
            <span>iGOT Portal</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
};

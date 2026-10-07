// ==============================================================================
// AI KARMAYOGI — ADAPTIVE ASSESSMENT PLAYER
// Live 2PL IRT Execution, Real-Time Countdown Timer, and Scenario Navigation
// ==============================================================================

import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/lib/api';
import {
  StartAssessmentData,
  AssessmentQuestion,
  AnswerSubmitResult,
} from '@/types';
import { ScenarioQuestion } from '@/components/assessment/ScenarioQuestion';
import { Button } from '@/components/ui/button';
import {
  Clock,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ChevronRight,
  Send,
} from 'lucide-react';

export const AssessmentPlayer: React.FC = () => {
  const navigate = useNavigate();

  const [session, setSession] = useState<StartAssessmentData | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<AssessmentQuestion | null>(null);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [currentIndex, setCurrentIndex] = useState(1);
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());

  // Time & Latency Tracking
  const [secondsRemaining, setSecondsRemaining] = useState(1200); // 20 minutes
  const questionStartTimeRef = useRef<number>(Date.now());

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 1. Initialize Assessment Session
  useEffect(() => {
    async function init() {
      setLoading(true);
      setError(null);
      try {
        const data = await api.get<StartAssessmentData>('/assessment/start');
        setSession(data);
        setCurrentQuestion(data.question);
        setCurrentIndex(data.current_question_index || 1);
        questionStartTimeRef.current = Date.now();
      } catch (err: any) {
        setError(err.message || 'Failed to initialize assessment session.');
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  // 2. Countdown Timer
  useEffect(() => {
    if (secondsRemaining <= 0) {
      handleFinalSubmit();
      return;
    }

    const interval = setInterval(() => {
      setSecondsRemaining((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [secondsRemaining]);

  const formatTimer = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const handleToggleBookmark = () => {
    if (!currentQuestion) return;
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (next.has(currentQuestion.id)) {
        next.delete(currentQuestion.id);
      } else {
        next.add(currentQuestion.id);
      }
      return next;
    });
  };

  const handleNextAnswer = async () => {
    if (!session || !currentQuestion || selectedOption === null) return;

    setSubmitting(true);
    setError(null);

    const timeSpent = Math.max(2, Math.round((Date.now() - questionStartTimeRef.current) / 1000));

    try {
      const res = await api.post<AnswerSubmitResult>('/assessment/answer', {
        attempt_id: session.attempt_id,
        question_id: currentQuestion.id,
        selected_option_index: selectedOption,
        time_spent_seconds: timeSpent,
      });

      if (res.is_completed || !res.next_question) {
        // Complete and finalize assessment
        await handleFinalSubmit();
      } else {
        setCurrentQuestion(res.next_question);
        setCurrentIndex(res.current_question_index);
        setSelectedOption(null);
        questionStartTimeRef.current = Date.now();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to record answer.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFinalSubmit = async () => {
    if (!session) return;
    setSubmitting(true);
    try {
      await api.post('/assessment/submit', {
        attempt_id: session.attempt_id,
      });
      navigate(`/assessment/result/${session.attempt_id}`, { replace: true });
    } catch (err: any) {
      setError(err.message || 'Error submitting assessment.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[65vh] items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-600 border-t-transparent" />
          <p className="text-sm font-semibold text-slate-600 ">
            Calibrating psychometric 2PL adaptive item parameters...
          </p>
        </div>
      </div>
    );
  }

  if (error && !currentQuestion) {
    return (
      <div className="mx-auto max-w-lg px-4 py-16 text-center space-y-4">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-100 text-rose-600">
          <AlertCircle className="h-6 w-6" />
        </div>
        <h2 className="text-lg font-bold text-slate-900 ">Assessment Error</h2>
        <p className="text-xs text-slate-500">{error}</p>
        <Button onClick={() => navigate('/assessment')}>Return to Dashboard</Button>
      </div>
    );
  }

  const maxQuestions = session?.max_questions || 15;
  const progressPct = Math.min(100, Math.round(((currentIndex - 1) / maxQuestions) * 100));

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
      {/* Top Fixed Diagnostic Control Bar */}
      <div className="rounded-2xl border border-slate-200  bg-white  p-4 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold text-slate-900  uppercase tracking-wider flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-indigo-500 animate-pulse" />
              FRAC Competency Diagnostic
            </span>
            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-emerald-50 /60 text-emerald-700  border border-emerald-200 ">
              Adaptive 2PL IRT • Scale v2.4
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-slate-500 ">
              Question {currentIndex} of {maxQuestions}
            </span>
            {/* Progress bar */}
            <div className="h-1.5 w-48 sm:w-64 rounded-full bg-slate-100  overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 transition-all duration-300 rounded-full"
                style={{ width: `${progressPct}%` }}
              />
            </div>
            <span className="text-[10px] font-mono text-slate-600 font-semibold">{progressPct}%</span>
          </div>
        </div>

        {/* Right side: Timer & Badges */}
        <div className="flex items-center gap-3">
          <div
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono font-bold ${
              secondsRemaining < 180
                ? 'bg-rose-50 text-rose-700 border-rose-300 animate-pulse'
                : 'bg-slate-50 /80 text-slate-700  border-slate-200 '
            }`}
          >
            <Clock className="h-3.5 w-3.5" />
            <span>{formatTimer(secondsRemaining)}</span>
          </div>

          {currentIndex >= 10 && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleFinalSubmit}
              isLoading={submitting}
              className="text-xs text-slate-600 "
            >
              Complete Early
            </Button>
          )}
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-50 /40 text-rose-700  border border-rose-200  text-xs font-medium">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Question Scenario View */}
      {currentQuestion && (
        <ScenarioQuestion
          question={currentQuestion}
          selectedOption={selectedOption}
          onSelectOption={(idx) => setSelectedOption(idx)}
          isBookmarked={bookmarkedIds.has(currentQuestion.id)}
          onToggleBookmark={handleToggleBookmark}
          questionNumber={currentIndex}
          totalQuestions={maxQuestions}
        />
      )}

      {/* Question Number Tracker Bar (Stitch Design) */}
      <div className="rounded-2xl border border-slate-200/80  bg-white  p-4 shadow-xs">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-600 ">
            <span>Assessment Progress Ledger</span>
            <span className="text-[10px] text-slate-600">({currentIndex} of {maxQuestions} questions reached)</span>
          </div>
          <div className="flex items-center gap-3 text-[11px] text-slate-600">
            <span className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-indigo-500" /> Answered
            </span>
            <span className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-indigo-500" /> Current
            </span>
            <span className="flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-slate-200 " /> Pending
            </span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          {Array.from({ length: maxQuestions }).map((_, i) => {
            const qNum = i + 1;
            const isCurrent = qNum === currentIndex;
            const isCompleted = qNum < currentIndex;
            const isBookmarked = currentQuestion && qNum === currentIndex && bookmarkedIds.has(currentQuestion.id);

            return (
              <div
                key={qNum}
                className={`h-7 w-7 rounded-lg text-[11px] font-mono font-bold flex items-center justify-center transition-all ${
                  isCurrent
                    ? 'bg-indigo-500 text-slate-900 shadow-md shadow-emerald-600/30 ring-2 ring-emerald-400 scale-105'
                    : isCompleted
                    ? 'bg-emerald-50 /60 text-emerald-700  border border-emerald-200 '
                    : 'bg-slate-50  text-slate-600 border border-slate-200 '
                }`}
              >
                {qNum}
              </div>
            );
          })}
        </div>
      </div>

      {/* Bottom Action Footer */}
      <div className="flex items-center justify-between pt-1">
        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-600">
          <HelpCircle className="h-3.5 w-3.5" />
          <span>Formative 2PL IRT Diagnostic • Select best procedural option</span>
        </div>

        <div className="flex items-center gap-3 ml-auto">
          <Button
            size="lg"
            onClick={handleNextAnswer}
            disabled={selectedOption === null || submitting}
            isLoading={submitting}
            className="px-8 bg-indigo-500 hover:bg-emerald-700 text-white shadow-md shadow-emerald-600/20 font-semibold"
          >
            {currentIndex >= maxQuestions ? 'Finalize Assessment' : 'Submit & Next Question'}
            <ChevronRight className="h-4 w-4 ml-1.5" />
          </Button>
        </div>
      </div>
    </div>
  );
};

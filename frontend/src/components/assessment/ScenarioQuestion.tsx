// ==============================================================================
// AI KARMAYOGI — SCENARIO QUESTION COMPONENT
// Sovereign Government Docket Layout for Administrative Dilemma Assessment
// ==============================================================================

import React, { useEffect } from 'react';
import { AssessmentQuestion } from '@/types';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { Bookmark, FileText, Scale, ShieldCheck } from 'lucide-react';

interface ScenarioQuestionProps {
  question: AssessmentQuestion;
  selectedOption: number | null;
  onSelectOption: (index: number) => void;
  isBookmarked: boolean;
  onToggleBookmark: () => void;
  questionNumber: number;
  totalQuestions: number;
}

export const ScenarioQuestion: React.FC<ScenarioQuestionProps> = ({
  question,
  selectedOption,
  onSelectOption,
  isBookmarked,
  onToggleBookmark,
  questionNumber,
  totalQuestions,
}) => {
  // Support keyboard shortcuts (1, 2, 3, 4 or A, B, C, D)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if typing in an input field
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) return;

      const key = e.key.toUpperCase();
      if (key === '1' || key === 'A') onSelectOption(0);
      else if (key === '2' || key === 'B') onSelectOption(1);
      else if (key === '3' || key === 'C') onSelectOption(2);
      else if (key === '4' || key === 'D') onSelectOption(3);
      else if (key === 'B' && e.altKey) onToggleBookmark();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onSelectOption, onToggleBookmark]);

  const getBloomBadge = (level: string) => {
    switch (level.toUpperCase()) {
      case 'ANALYZE':
      case 'EVALUATE':
        return 'bg-amber-100 /60 text-amber-800  border-amber-300 ';
      case 'APPLY':
        return 'bg-emerald-100 /60 text-emerald-800  border-emerald-300 ';
      case 'REMEMBER':
      case 'UNDERSTAND':
      default:
        return 'bg-emerald-100 /60 text-emerald-800  border-emerald-300 ';
    }
  };

  const getPillarBadge = (pillar: string) => {
    switch (pillar.toUpperCase()) {
      case 'BEHAVIORAL':
        return 'bg-purple-100 /60 text-purple-800  border-purple-300 ';
      case 'DOMAIN':
        return 'bg-teal-100 /60 text-teal-800  border-teal-300 ';
      case 'FUNCTIONAL':
      default:
        return 'bg-cyan-100 /60 text-cyan-800  border-cyan-300 ';
    }
  };

  const optionLetters = ['A', 'B', 'C', 'D'];

  return (
    <Card className="border-slate-200  shadow-xl overflow-hidden">
      {/* Top Docket Reference Header */}
      <CardHeader className="bg-slate-50/80 /80 border-b border-slate-200  py-3.5 px-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="flex h-6 w-6 items-center justify-center rounded-md bg-indigo-500 text-white text-xs font-bold">
              Q{questionNumber}
            </span>
            <span className="text-xs font-bold text-slate-700  tracking-wide uppercase">
              {question.competency_name}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getPillarBadge(question.competency_type)}`}>
              {question.competency_type}
            </span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getBloomBadge(question.bloom_level)}`}>
              Bloom: {question.bloom_level}
            </span>
            <button
              onClick={onToggleBookmark}
              title="Bookmark for review"
              className={`p-1.5 rounded-lg border transition-colors ${
                isBookmarked
                  ? 'bg-amber-50 /50 border-amber-300  text-amber-600 '
                  : 'border-slate-200  text-slate-600 hover:text-slate-600'
              }`}
            >
              <Bookmark className="h-4 w-4" fill={isBookmarked ? 'currentColor' : 'none'} />
            </button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-6 space-y-6">
        {/* Government File Scenario Container */}
        <div className="relative rounded-xl border border-slate-200  bg-slate-50/50 /40 p-5 space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 ">
            <FileText className="h-4 w-4" />
            <span>CENTRAL SECRETARIAT DOCKET SCENARIO</span>
          </div>

          <div className="text-sm text-slate-800  leading-relaxed font-normal whitespace-pre-line">
            {question.question_stem}
          </div>
        </div>

        {/* 4 Interactive Options */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-500 ">
            <span>Select the most procedurally and ethically appropriate course of action:</span>
            <span className="hidden sm:inline text-[11px] text-slate-600">Press keys 1-4 or A-D to select</span>
          </div>

          <div className="space-y-2.5" role="radiogroup" aria-label="Assessment Options">
            {question.options.map((opt, idx) => {
              const optText = typeof opt === 'string' ? opt : opt.text;
              const isSelected = selectedOption === idx;

              return (
                <button
                  key={idx}
                  type="button"
                  role="radio"
                  aria-checked={isSelected}
                  onClick={() => onSelectOption(idx)}
                  className={`w-full text-left p-4 rounded-xl border transition-all flex items-start gap-3.5 group focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 ${
                    isSelected
                      ? 'bg-emerald-50/70 /40 border-emerald-500  shadow-sm shadow-emerald-500/10'
                      : 'bg-white  border-slate-200  hover:border-slate-300  hover:bg-slate-50/50'
                  }`}
                >
                  <span
                    className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-lg text-xs font-bold border transition-colors ${
                      isSelected
                        ? 'bg-indigo-500 text-slate-900 border-emerald-600'
                        : 'bg-slate-100  text-slate-600  border-slate-200  group-hover:border-slate-400'
                    }`}
                  >
                    {optionLetters[idx]}
                  </span>
                  <span
                    className={`flex-1 text-sm leading-relaxed transition-colors ${
                      isSelected
                        ? 'font-medium text-emerald-950 '
                        : 'text-slate-700 '
                    }`}
                  >
                    {optText}
                  </span>
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded border transition-colors shrink-0 ${
                    isSelected
                      ? 'border-emerald-300 text-emerald-700   bg-emerald-100/50 /50'
                      : 'border-slate-200  text-slate-600 opacity-60 group-hover:opacity-100'
                  }`}>
                    [{idx + 1}]
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </CardContent>

      {/* Statutory Source Citation Footer */}
      <CardFooter className="bg-slate-50/50 /40 border-t border-slate-200/80 /80 py-3 px-6 flex items-center justify-between text-xs text-slate-500 ">
        <div className="flex items-center gap-1.5">
          <Scale className="h-3.5 w-3.5 text-slate-600" />
          <span>Statutory Authority: <span className="font-semibold text-slate-700 ">{question.source_citation}</span></span>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-slate-600">
          <ShieldCheck className="h-3.5 w-3.5 text-teal-600" />
          <span>FRAC Formative Diagnostic</span>
        </div>
      </CardFooter>
    </Card>
  );
};

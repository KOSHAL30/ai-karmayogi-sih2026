// ==============================================================================
// AI KARMAYOGI — MCQ QUESTION EDITOR (HUMAN REVIEW STUDIO)
// Edit Question Stem, Bloom's Taxonomy, Options, Distractor Rationales & Citations
// ==============================================================================

import React, { useState } from 'react';
import { DraftMCQ, BloomLevel, DifficultyTier, DraftMCQOption } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Edit3,
  CheckCircle2,
  X,
  Save,
  Trash2,
  BookOpen,
  GraduationCap,
  Sparkles,
} from 'lucide-react';

interface QuestionEditorProps {
  question: DraftMCQ;
  onSave: (updated: DraftMCQ) => void;
  onCancel: () => void;
}

const BLOOM_LEVELS: BloomLevel[] = [
  'REMEMBER',
  'UNDERSTAND',
  'APPLY',
  'ANALYZE',
  'EVALUATE',
];

const DIFFICULTY_TIERS: DifficultyTier[] = ['EASY', 'MEDIUM', 'HARD'];

export const QuestionEditor: React.FC<QuestionEditorProps> = ({
  question,
  onSave,
  onCancel,
}) => {
  const [stem, setStem] = useState(question.question_stem);
  const [bloom, setBloom] = useState<BloomLevel>(question.bloom_level);
  const [difficulty, setDifficulty] = useState<DifficultyTier>(question.difficulty);
  const [citation, setCitation] = useState(question.source_citation);
  const [explanation, setExplanation] = useState(question.pedagogical_explanation);
  const [options, setOptions] = useState<DraftMCQOption[]>(
    question.options.map((o) => ({ ...o }))
  );

  const handleOptionTextChange = (id: string, text: string) => {
    setOptions((prev) =>
      prev.map((o) => (o.id === id ? { ...o, option_text: text } : o))
    );
  };

  const handleRationaleChange = (id: string, text: string) => {
    setOptions((prev) =>
      prev.map((o) => (o.id === id ? { ...o, distractor_rationale: text } : o))
    );
  };

  const handleSetCorrectOption = (id: string) => {
    setOptions((prev) =>
      prev.map((o) => ({
        ...o,
        is_correct: o.id === id,
      }))
    );
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...question,
      question_stem: stem.trim(),
      bloom_level: bloom,
      difficulty: difficulty,
      source_citation: citation.trim(),
      pedagogical_explanation: explanation.trim(),
      options: options,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-200  bg-white  p-6 shadow-2xl space-y-5 my-8">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 ">
          <div className="flex items-center gap-2">
            <Edit3 className="h-5 w-5 text-teal-600" />
            <h3 className="text-sm font-bold text-slate-900 ">
              Human Review & Editorial Studio
            </h3>
          </div>
          <button
            onClick={onCancel}
            className="p-1 rounded-lg text-slate-600 hover:text-slate-600"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleFormSubmit} className="space-y-4 text-xs">
          {/* Stem */}
          <div>
            <label className="block font-semibold text-slate-700  mb-1">
              Question Stem / Administrative Scenario
            </label>
            <textarea
              rows={3}
              value={stem}
              onChange={(e) => setStem(e.target.value)}
              required
              className="w-full text-xs px-3 py-2 rounded-xl border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          {/* Classification Tags */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700  mb-1">
                Bloom's Cognitive Level
              </label>
              <select
                value={bloom}
                onChange={(e) => setBloom(e.target.value as BloomLevel)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900 "
              >
                {BLOOM_LEVELS.map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700  mb-1">
                Difficulty Tier
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as DifficultyTier)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900 "
              >
                {DIFFICULTY_TIERS.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Options & Distractors */}
          <div className="space-y-3 pt-2">
            <label className="block font-semibold text-slate-700 ">
              Multiple Choice Options (Select radio for correct answer)
            </label>
            {options.map((opt, idx) => (
              <div
                key={opt.id}
                className={`p-3 rounded-xl border transition-colors space-y-2 ${
                  opt.is_correct
                    ? 'border-emerald-500 bg-emerald-50/30 /20'
                    : 'border-slate-200  bg-slate-50/50 /40'
                }`}
              >
                <div className="flex items-center gap-2">
                  <input
                    type="radio"
                    name="correct_option"
                    checked={opt.is_correct}
                    onChange={() => handleSetCorrectOption(opt.id)}
                    className="text-teal-600 focus:ring-emerald-500"
                  />
                  <span className="font-bold text-slate-600  w-5">
                    {String.fromCharCode(65 + idx)}.
                  </span>
                  <input
                    type="text"
                    value={opt.option_text}
                    onChange={(e) => handleOptionTextChange(opt.id, e.target.value)}
                    required
                    className="flex-1 text-xs px-3 py-1.5 rounded-lg border border-slate-300  bg-white  text-slate-900 "
                  />
                  {opt.is_correct && (
                    <span className="text-[10px] font-bold text-teal-600  bg-emerald-100  px-2 py-0.5 rounded-full border border-emerald-300 ">
                      Correct Key
                    </span>
                  )}
                </div>

                <div className="pl-7">
                  <input
                    type="text"
                    value={opt.distractor_rationale || ''}
                    onChange={(e) => handleRationaleChange(opt.id, e.target.value)}
                    placeholder="Pedagogical distractor rationale..."
                    className="w-full text-[11px] px-2.5 py-1 rounded border border-slate-200  bg-white/80 /60 text-slate-600  italic"
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Explanation */}
          <div>
            <label className="block font-semibold text-slate-700  mb-1">
              Statutory Rationale & Explainable Answer
            </label>
            <textarea
              rows={2}
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-xl border border-slate-300  bg-white  text-slate-900 "
            />
          </div>

          {/* Citation */}
          <div>
            <label className="block font-semibold text-slate-700  mb-1">
              Source Citation & Rule Reference
            </label>
            <input
              type="text"
              value={citation}
              onChange={(e) => setCitation(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  font-mono"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100 ">
            <Button type="button" variant="outline" size="sm" onClick={onCancel} className="text-xs">
              Discard Changes
            </Button>
            <Button
              type="submit"
              size="sm"
              className="text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold flex items-center gap-1.5"
            >
              <Save className="h-3.5 w-3.5" />
              Save Review Changes
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

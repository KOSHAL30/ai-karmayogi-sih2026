// ==============================================================================
// AI KARMAYOGI — BLOOM-CLASSIFIED AI MCQ GENERATION STUDIO
// Human-in-the-Loop Review, Distractor Rationales & Assessment Publishing
// ==============================================================================

import React, { useState } from 'react';
import { api, APIClientError } from '@/lib/api';
import { DocumentItem, DraftMCQ, GenerateMCQResponse, BloomLevel, DifficultyTier } from '@/types';
import { QuestionEditor } from './QuestionEditor';
import { Button } from '@/components/ui/button';
import {
  Sparkles,
  BookOpen,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Sliders,
  Send,
  Loader2,
  Trash2,
  Edit3,
  Award,
  Layers,
  GraduationCap,
  ShieldAlert,
} from 'lucide-react';

interface MCQStudioProps {
  document: DocumentItem;
  onPublished?: (quizId: string) => void;
}

export const MCQStudio: React.FC<MCQStudioProps> = ({ document, onPublished }) => {
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [targetCompetency, setTargetCompetency] = useState<string>('Central Financial Management');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const [quizId, setQuizId] = useState<string | null>(null);
  const [quizTitle, setQuizTitle] = useState<string>('');
  const [questions, setQuestions] = useState<DraftMCQ[]>([]);
  const [editingQuestion, setEditingQuestion] = useState<DraftMCQ | null>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const payload = {
        document_id: document.id,
        num_questions: numQuestions,
        difficulty_distribution: {
          EASY: 0.2,
          MEDIUM: 0.6,
          HARD: 0.2,
        },
        competency_name: targetCompetency,
      };

      const res = await api.post<GenerateMCQResponse>('/mcq/generate', payload);
      setQuizId(res.quiz_id);
      setQuizTitle(res.title || `Assessment: ${document.document_title}`);
      setQuestions(res.questions.map((q) => ({ ...q, is_approved: true })));
      setSuccessMessage(`Successfully generated ${res.questions.length} Bloom-classified questions.`);
    } catch (err: any) {
      setError(err instanceof APIClientError ? err.message : 'Failed to generate MCQs.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveQuestion = (updated: DraftMCQ) => {
    setQuestions((prev) =>
      prev.map((q) => (q.id === updated.id ? { ...updated, is_approved: true } : q))
    );
    setEditingQuestion(null);
  };

  const handleDeleteQuestion = (id: string) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  };

  const toggleApproval = (id: string) => {
    setQuestions((prev) =>
      prev.map((q) => (q.id === id ? { ...q, is_approved: !q.is_approved } : q))
    );
  };

  const handlePublish = async () => {
    if (!quizId || questions.length === 0) return;

    setIsPublishing(true);
    setError(null);

    const approvedOnly = questions.filter((q) => q.is_approved !== false);
    if (approvedOnly.length === 0) {
      setError('Please approve at least one question before publishing.');
      setIsPublishing(false);
      return;
    }

    try {
      const payload = {
        quiz_id: quizId,
        title: quizTitle,
        description: `Official assessment auto-generated and reviewed from ${document.document_title}`,
        document_id: document.id,
        approved_questions: approvedOnly,
      };

      const res = await api.post<any>('/mcq/publish', payload);
      setSuccessMessage(`Assessment published to Mission Karmayogi catalog! Quiz ID: ${res.quiz_id || quizId}`);
      if (onPublished) onPublished(res.quiz_id || quizId);
    } catch (err: any) {
      setError(err instanceof APIClientError ? err.message : 'Failed to publish assessment.');
    } finally {
      setIsPublishing(false);
    }
  };

  const getBloomBadgeColor = (bloom: BloomLevel) => {
    switch (bloom) {
      case 'REMEMBER':
        return 'bg-teal-50  text-teal-700  border-teal-200 ';
      case 'UNDERSTAND':
        return 'bg-teal-50  text-teal-700  border-teal-200 ';
      case 'APPLY':
        return 'bg-amber-50  text-amber-700  border-amber-200 ';
      case 'ANALYZE':
        return 'bg-purple-50  text-purple-700  border-purple-200 ';
      case 'EVALUATE':
        return 'bg-rose-50  text-rose-700  border-rose-200 ';
      default:
        return 'bg-slate-100  text-slate-700  border-slate-200';
    }
  };

  const getDifficultyBadge = (diff: DifficultyTier) => {
    switch (diff) {
      case 'EASY':
        return 'bg-emerald-50  text-emerald-700  border-emerald-200 ';
      case 'MEDIUM':
        return 'bg-amber-50  text-amber-700  border-amber-200 ';
      case 'HARD':
        return 'bg-rose-50  text-rose-700  border-rose-200 ';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="flex flex-col h-full bg-white  rounded-2xl border border-slate-200  overflow-hidden shadow-sm">
      {/* Header */}
      <div className="p-4 border-b border-slate-200  bg-slate-50/60 /60 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-xl bg-emerald-50 /60 text-teal-600  flex items-center justify-center">
            <GraduationCap className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900 ">
              AI MCQ Generation & Review Studio
            </h3>
            <p className="text-[10px] text-slate-500">
              Bloom-Classified Questions with Pedagogical Explanations & Statutory Grounding
            </p>
          </div>
        </div>

        {questions.length > 0 && (
          <Button
            size="sm"
            onClick={handlePublish}
            disabled={isPublishing}
            className="text-xs h-7 px-3 bg-indigo-500 hover:bg-indigo-500 text-white font-semibold flex items-center gap-1.5 shadow-sm"
          >
            {isPublishing ? (
              <Loader2 className="h-3 w-3 animate-spin" />
            ) : (
              <CheckCircle2 className="h-3 w-3" />
            )}
            Publish to Assessment Catalog
          </Button>
        )}
      </div>

      {/* Generator Controls */}
      <div className="p-4 border-b border-slate-100  bg-slate-50/30 /20">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
          <div>
            <label className="block text-[11px] font-semibold text-slate-700  mb-1">
              Batch Size
            </label>
            <div className="flex gap-2">
              {[5, 10, 20].map((count) => (
                <button
                  key={count}
                  type="button"
                  onClick={() => setNumQuestions(count)}
                  className={`flex-1 py-1.5 text-xs font-semibold rounded-lg border transition-all ${
                    numQuestions === count
                      ? 'bg-indigo-500 text-slate-900 border-emerald-600 shadow-sm'
                      : 'bg-white  text-slate-700  border-slate-200  hover:border-emerald-400'
                  }`}
                >
                  {count} Questions
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-700  mb-1">
              FRAC Competency Alignment
            </label>
            <input
              type="text"
              value={targetCompetency}
              onChange={(e) => setTargetCompetency(e.target.value)}
              placeholder="e.g. Procurement & Contract Management"
              className="w-full text-xs px-3 py-1.5 rounded-lg border border-slate-300  bg-white  text-slate-900 "
            />
          </div>

          <div>
            <Button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full text-xs h-8 bg-indigo-500 hover:bg-indigo-500 text-white font-semibold flex items-center justify-center gap-1.5 shadow-md shadow-emerald-600/20"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  Generating Bloom MCQs...
                </>
              ) : (
                <>
                  <Sparkles className="h-3.5 w-3.5" />
                  Generate Sovereign MCQs
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Feedback alerts */}
        {error && (
          <div className="mt-3 p-2.5 rounded-lg bg-rose-50 /40 border border-rose-200  text-xs text-rose-700  flex items-center gap-2">
            <AlertCircle className="h-3.5 w-3.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
        {successMessage && (
          <div className="mt-3 p-2.5 rounded-lg bg-emerald-50 /40 border border-emerald-200  text-xs text-emerald-700  flex items-center gap-2">
            <CheckCircle2 className="h-3.5 w-3.5 shrink-0" />
            <span>{successMessage}</span>
          </div>
        )}
      </div>

      {/* Generated Questions List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {questions.length === 0 ? (
          <div className="text-center py-16 space-y-3">
            <GraduationCap className="h-10 w-10 text-slate-600  mx-auto" />
            <p className="text-xs text-slate-500">
              No questions generated yet. Configure the batch options above to generate Bloom-classified MCQs grounded in "{document.document_title}".
            </p>
          </div>
        ) : (
          questions.map((q, qIndex) => (
            <div
              key={q.id}
              className={`rounded-xl border p-4 transition-all space-y-3 ${
                q.is_approved !== false
                  ? 'border-slate-200  bg-white /80 shadow-sm'
                  : 'border-slate-200  bg-slate-50/60 /40 opacity-60'
              }`}
            >
              {/* Question Header & Classification */}
              <div className="flex items-start justify-between gap-2 pb-2 border-b border-slate-100 ">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-bold text-slate-800 ">
                    Q{qIndex + 1}.
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getBloomBadgeColor(
                      q.bloom_level
                    )}`}
                  >
                    {q.bloom_level}
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getDifficultyBadge(
                      q.difficulty
                    )}`}
                  >
                    {q.difficulty}
                  </span>
                  {q.competency_name && (
                    <span className="text-[10px] font-medium text-slate-500 truncate max-w-[200px]">
                      • {q.competency_name}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setEditingQuestion(q)}
                    title="Edit question & distractors"
                    className="p-1 rounded hover:bg-slate-100  text-slate-600 hover:text-teal-600 transition-colors"
                  >
                    <Edit3 className="h-3.5 w-3.5" />
                  </button>
                  <button
                    onClick={() => handleDeleteQuestion(q.id)}
                    title="Remove question"
                    className="p-1 rounded hover:bg-slate-100  text-slate-600 hover:text-rose-500 transition-colors"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>
              </div>

              {/* Stem */}
              <p className="text-xs font-semibold text-slate-900  leading-relaxed">
                {q.question_stem}
              </p>

              {/* Options */}
              <div className="space-y-1.5">
                {q.options.map((opt, oIndex) => (
                  <div
                    key={opt.id}
                    className={`p-2 rounded-lg text-xs flex items-start gap-2 border transition-colors ${
                      opt.is_correct
                        ? 'border-emerald-300  bg-emerald-50/50 /30 text-emerald-950  font-medium'
                        : 'border-slate-100 /80 bg-slate-50/50 /30 text-slate-700 '
                    }`}
                  >
                    <span className="font-bold text-slate-500 w-4 shrink-0">
                      {String.fromCharCode(65 + oIndex)}.
                    </span>
                    <div className="flex-1">
                      <span>{opt.option_text}</span>
                      {opt.distractor_rationale && (
                        <p className="text-[10px] text-slate-600 italic mt-0.5">
                          Rationale: {opt.distractor_rationale}
                        </p>
                      )}
                    </div>
                    {opt.is_correct && (
                      <span className="text-[9px] font-bold text-teal-600  shrink-0">
                        ✓ Correct
                      </span>
                    )}
                  </div>
                ))}
              </div>

              {/* Footer Citations & Explanation */}
              <div className="pt-2 border-t border-slate-100  text-[11px] space-y-1">
                <p className="text-slate-600 ">
                  <span className="font-bold text-teal-600 ">Explanation: </span>
                  {q.pedagogical_explanation}
                </p>
                <p className="text-slate-500 font-mono text-[10px] flex items-center gap-1">
                  <BookOpen className="h-3 w-3 text-slate-600" />
                  Citation: {q.source_citation}
                </p>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Editing Modal */}
      {editingQuestion && (
        <QuestionEditor
          question={editingQuestion}
          onSave={handleSaveQuestion}
          onCancel={() => setEditingQuestion(null)}
        />
      )}
    </div>
  );
};

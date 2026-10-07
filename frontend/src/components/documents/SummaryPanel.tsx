// ==============================================================================
// AI KARMAYOGI — 6-PART AI POLICY SUMMARY PANEL
// Structured Executive Summary, Policy Changes, Clauses, Checklist, Actions & FAQs
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { DocumentItem, DocumentSummary } from '@/types';
import { Button } from '@/components/ui/button';
import {
  FileText,
  Sparkles,
  CheckSquare,
  AlertTriangle,
  HelpCircle,
  TrendingUp,
  BookOpen,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  Copy,
  Check,
  CheckCircle2,
  Loader2,
} from 'lucide-react';

interface SummaryPanelProps {
  document: DocumentItem;
  onSummaryUpdated?: (summary: DocumentSummary) => void;
}

export const SummaryPanel: React.FC<SummaryPanelProps> = ({ document, onSummaryUpdated }) => {
  const [summary, setSummary] = useState<DocumentSummary | null>(document.summary_json || null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'checklist' | 'faqs'>('overview');
  const [copiedSection, setCopiedSection] = useState<string | null>(null);
  const [expandedFaqIndex, setExpandedFaqIndex] = useState<number | null>(0);
  const [checkedItems, setCheckedItems] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (document.summary_json) {
      setSummary(document.summary_json);
    } else {
      // If not present in doc object, fetch it
      fetchSummary();
    }
  }, [document.id]);

  const fetchSummary = async () => {
    setIsLoading(true);
    try {
      const res = await api.get<any>(`/documents/${document.id}/summary`);
      if (res.summary) {
        setSummary(res.summary);
        if (onSummaryUpdated) onSummaryUpdated(res.summary);
      }
    } catch (err) {
      console.error('Failed to fetch summary:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = async () => {
    setIsLoading(true);
    try {
      const res = await api.post<any>(`/documents/${document.id}/summary`, {});
      if (res.summary) {
        setSummary(res.summary);
        if (onSummaryUpdated) onSummaryUpdated(res.summary);
      }
    } catch (err) {
      console.error('Failed to regenerate summary:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text: string, section: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(section);
    setTimeout(() => setCopiedSection(null), 2000);
  };

  const toggleCheck = (index: number) => {
    setCheckedItems((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="flex flex-col h-full bg-white  rounded-2xl border border-slate-200  overflow-hidden shadow-sm">
      {/* Header */}
      <div className="p-4 border-b border-slate-200  bg-slate-50/60 /60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-xl bg-emerald-50 /60 text-teal-600  flex items-center justify-center">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900 ">
              6-Part Sovereign AI Summary
            </h3>
            <p className="text-[10px] text-slate-500">
              Qwen 3.8 27B Structured Governance Extraction
            </p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleRegenerate}
          disabled={isLoading}
          className="text-xs h-7 px-2.5 flex items-center gap-1.5"
        >
          <RefreshCw className={`h-3 w-3 ${isLoading ? 'animate-spin' : ''}`} />
          <span className="hidden sm:inline">Refresh</span>
        </Button>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex border-b border-slate-100  px-4 pt-2 gap-2 text-xs bg-slate-50/30 /30">
        <button
          onClick={() => setActiveTab('overview')}
          className={`pb-2 font-semibold border-b-2 transition-colors ${
            activeTab === 'overview'
              ? 'border-emerald-600 text-teal-600 '
              : 'border-transparent text-slate-500 hover:text-slate-700'
          }`}
        >
          Summary & Changes
        </button>
        <button
          onClick={() => setActiveTab('checklist')}
          className={`pb-2 font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
            activeTab === 'checklist'
              ? 'border-emerald-600 text-teal-600 '
              : 'border-transparent text-slate-500 hover:text-slate-700'
          }`}
        >
          <span>Checklist & Actions</span>
          {summary?.compliance_checklist && (
            <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 ">
              {summary.compliance_checklist.length}
            </span>
          )}
        </button>
        <button
          onClick={() => setActiveTab('faqs')}
          className={`pb-2 font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
            activeTab === 'faqs'
              ? 'border-emerald-600 text-teal-600 '
              : 'border-transparent text-slate-500 hover:text-slate-700'
          }`}
        >
          <span>Statutory FAQs</span>
          {summary?.faqs && (
            <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 ">
              {summary.faqs.length}
            </span>
          )}
        </button>
      </div>

      {/* Content Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 text-slate-600 gap-2">
            <Loader2 className="h-6 w-6 animate-spin text-teal-600" />
            <span className="text-xs font-medium">Synthesizing 6-part policy summary...</span>
          </div>
        ) : !summary ? (
          <div className="text-center py-12 space-y-3">
            <p className="text-xs text-slate-500">No structured summary generated yet.</p>
            <Button onClick={handleRegenerate} size="sm" className="text-xs bg-indigo-500 text-white">
              Generate AI Summary
            </Button>
          </div>
        ) : activeTab === 'overview' ? (
          <div className="space-y-4">
            {/* 1. Executive Summary */}
            <div className="rounded-xl border border-slate-200  p-3.5 bg-slate-50/40 /30 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
                  <FileText className="h-3.5 w-3.5 text-teal-600" />
                  1. Executive Summary
                </span>
                <button
                  onClick={() => copyToClipboard(summary.executive_summary, 'exec')}
                  className="text-slate-600 hover:text-slate-600"
                >
                  {copiedSection === 'exec' ? (
                    <Check className="h-3 w-3 text-teal-600" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </button>
              </div>
              <p className="text-xs text-slate-700  leading-relaxed">
                {summary.executive_summary}
              </p>
            </div>

            {/* 2. Key Policy Changes */}
            {summary.key_policy_changes && summary.key_policy_changes.length > 0 && (
              <div className="rounded-xl border border-slate-200  p-3.5 space-y-2">
                <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
                  <TrendingUp className="h-3.5 w-3.5 text-teal-600" />
                  2. Key Policy Changes & Reforms
                </span>
                <ul className="space-y-1.5 text-xs text-slate-700 ">
                  {summary.key_policy_changes.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* 3. Important Clauses */}
            {summary.important_clauses && summary.important_clauses.length > 0 && (
              <div className="rounded-xl border border-slate-200  p-3.5 space-y-2">
                <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
                  <BookOpen className="h-3.5 w-3.5 text-teal-600" />
                  3. Important Clauses & Statutory Mandates
                </span>
                <ul className="space-y-1.5 text-xs text-slate-700 ">
                  {summary.important_clauses.map((clause, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                      <span className="font-medium">{clause}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : activeTab === 'checklist' ? (
          <div className="space-y-4">
            {/* 4. Compliance Checklist */}
            <div className="rounded-xl border border-slate-200  p-3.5 space-y-2">
              <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
                <CheckSquare className="h-3.5 w-3.5 text-teal-600" />
                4. Statutory Compliance Checklist
              </span>
              <div className="space-y-2 pt-1">
                {summary.compliance_checklist?.map((item, idx) => (
                  <div
                    key={idx}
                    onClick={() => toggleCheck(idx)}
                    className={`cursor-pointer flex items-start gap-2.5 p-2.5 rounded-lg border text-xs transition-colors ${
                      checkedItems[idx]
                        ? 'border-emerald-300  bg-emerald-50/40 /20 text-emerald-900  line-through opacity-75'
                        : 'border-slate-200  hover:border-slate-300 text-slate-700 '
                    }`}
                  >
                    <div
                      className={`h-4 w-4 rounded flex items-center justify-center shrink-0 mt-0.5 border ${
                        checkedItems[idx]
                          ? 'bg-indigo-500 border-emerald-600 text-slate-900'
                          : 'border-slate-300 '
                      }`}
                    >
                      {checkedItems[idx] && <Check className="h-3 w-3" />}
                    </div>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* 5. Action Points */}
            {summary.action_points && summary.action_points.length > 0 && (
              <div className="rounded-xl border border-slate-200  p-3.5 space-y-2">
                <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
                  <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />
                  5. Action Points for Government Officers
                </span>
                <ul className="space-y-1.5 text-xs text-slate-700 ">
                  {summary.action_points.map((action, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <div className="h-1.5 w-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          /* 6. FAQs Tab */
          <div className="space-y-2">
            <span className="text-xs font-bold text-slate-900  flex items-center gap-1.5 mb-2">
              <HelpCircle className="h-3.5 w-3.5 text-teal-600" />
              6. Frequently Asked Statutory Questions
            </span>
            {summary.faqs?.map((faq, idx) => {
              const isExpanded = expandedFaqIndex === idx;
              return (
                <div
                  key={idx}
                  className="rounded-xl border border-slate-200  overflow-hidden text-xs"
                >
                  <button
                    onClick={() => setExpandedFaqIndex(isExpanded ? null : idx)}
                    className="w-full text-left p-3 font-semibold text-slate-800  bg-slate-50/50 /40 hover:bg-slate-100/50 flex items-center justify-between gap-2"
                  >
                    <span>{faq.question}</span>
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4 shrink-0 text-slate-600" />
                    ) : (
                      <ChevronDown className="h-4 w-4 shrink-0 text-slate-600" />
                    )}
                  </button>
                  {isExpanded && (
                    <div className="p-3 bg-white  text-slate-600  space-y-1.5 border-t border-slate-100 ">
                      <p className="leading-relaxed">{faq.answer}</p>
                      {faq.rule_ref && (
                        <p className="text-[10px] font-mono text-teal-600 ">
                          Reference: {faq.rule_ref}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

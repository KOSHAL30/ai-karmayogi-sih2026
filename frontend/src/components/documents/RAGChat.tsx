// ==============================================================================
// AI KARMAYOGI — SOVEREIGN RAG CHAT ASSISTANT
// Grounded Q&A with Statutory Citations, Confidence Scoring & Verbatim Sources
// ==============================================================================

import React, { useState } from 'react';
import { api, APIClientError } from '@/lib/api';
import { DocumentItem, RAGResponse, CitationItem } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Send,
  Sparkles,
  ShieldCheck,
  BookOpen,
  ChevronRight,
  Loader2,
  Clock,
  CheckCircle2,
  AlertCircle,
  CornerDownRight,
  ExternalLink,
  Bot,
  User,
  Zap,
} from 'lucide-react';

interface RAGChatProps {
  activeDocument?: DocumentItem | null;
  onCitationClick?: (citation: CitationItem) => void;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  ragData?: RAGResponse;
}

export const RAGChat: React.FC<RAGChatProps> = ({ activeDocument, onCitationClick }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: activeDocument
        ? `Namaste. I am your Sovereign Policy Intelligence Assistant. I am grounded in "${activeDocument.document_title}" and Central Government service rules. Ask any statutory question to receive cited, hallucination-free answers.`
        : `Namaste. I am your Sovereign Policy Intelligence Assistant. Ask any question regarding GFR 2017, CCS Conduct Rules, or uploaded government policies to receive verified citations and rule references.`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [scopeToDoc, setScopeToDoc] = useState(true);

  const samplePrompts = [
    'What are the mandatory thresholds for GeM procurement under Rule 149?',
    'What is the procedure if a required item is not available on GeM?',
    'What are the compliance checkpoints before issuing a supply order?',
    'What does Rule 149(i) mandate regarding direct purchase up to ₹25,000?',
  ];

  const handleSend = async (questionText: string) => {
    const cleanQuery = questionText.trim();
    if (!cleanQuery || isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: cleanQuery,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setIsLoading(true);

    try {
      const payload: { query: string; document_id?: string; top_k: number } = {
        query: cleanQuery,
        top_k: 5,
      };

      if (scopeToDoc && activeDocument) {
        payload.document_id = activeDocument.id;
      }

      const res = await api.post<RAGResponse>('/rag/query', payload);

      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        sender: 'assistant',
        text: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        ragData: res,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: 'assistant',
        text: err instanceof APIClientError ? err.message : 'Unable to complete sovereign RAG query.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white  rounded-2xl border border-slate-200  overflow-hidden shadow-sm">
      {/* Header with Scope Toggle & Sovereign Badges */}
      <div className="p-4 border-b border-slate-200  bg-slate-50/60 /60 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-xl bg-indigo-500 text-white flex items-center justify-center shadow-sm">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900  flex items-center gap-1.5">
              Sovereign RAG Copilot
              <span className="rounded bg-emerald-50  px-1.5 py-0.5 text-[9px] font-bold text-emerald-700  border border-emerald-200 ">
                Grounded
              </span>
            </h3>
            <p className="text-[10px] text-slate-500">
              Qwen 3.8 27B • Groq Inference • 768-dim RAG
            </p>
          </div>
        </div>

        {activeDocument && (
          <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-600 ">
            <input
              type="checkbox"
              checked={scopeToDoc}
              onChange={(e) => setScopeToDoc(e.target.checked)}
              className="rounded border-slate-300 text-teal-600 focus:ring-emerald-500"
            />
            <span className="text-[11px] font-medium hidden sm:inline truncate max-w-[160px]">
              Lock to {activeDocument.document_title.slice(0, 18)}...
            </span>
          </label>
        )}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.sender === 'assistant' && (
              <div className="h-7 w-7 rounded-lg bg-emerald-100  text-emerald-700  flex items-center justify-center shrink-0 mt-0.5">
                <Bot className="h-4 w-4" />
              </div>
            )}

            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed space-y-2.5 ${
                msg.sender === 'user'
                  ? 'bg-indigo-500 text-slate-900 rounded-br-none shadow-sm'
                  : 'bg-slate-50 /80 text-slate-800  border border-slate-200 /80 rounded-bl-none shadow-sm'
              }`}
            >
              <div className="whitespace-pre-line font-normal">{msg.text}</div>

              {/* Citations & Metadata for Assistant Messages */}
              {msg.ragData && (
                <div className="pt-2 border-t border-slate-200  space-y-2">
                  <div className="flex flex-wrap items-center justify-between text-[10px] text-slate-500 ">
                    <span className="flex items-center gap-1 font-semibold text-teal-600 ">
                      <ShieldCheck className="h-3 w-3" />
                      Confidence: {(msg.ragData.confidence_score * 100).toFixed(0)}% Grounded
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Clock className="h-2.5 w-2.5" />
                      {msg.ragData.latency_ms}ms • {msg.ragData.model}
                    </span>
                  </div>

                  {msg.ragData.citations && msg.ragData.citations.length > 0 && (
                    <div className="space-y-1.5 pt-1">
                      <p className="text-[10px] font-bold text-slate-600  flex items-center gap-1">
                        <BookOpen className="h-3 w-3 text-teal-600" />
                        Statutory Evidence & Rule Citations ({msg.ragData.citations.length})
                      </p>
                      <div className="space-y-1.5">
                        {msg.ragData.citations.map((cit, idx) => (
                          <div
                            key={idx}
                            onClick={() => onCitationClick && onCitationClick(cit)}
                            className="cursor-pointer p-2 rounded-lg bg-white  border border-slate-200 /80 hover:border-emerald-400  transition-colors text-[11px]"
                          >
                            <div className="flex items-center justify-between font-medium text-teal-600 ">
                              <span className="truncate max-w-[80%]">{cit.breadcrumb}</span>
                              <span className="font-mono text-[10px] text-slate-500">
                                Page {cit.page_number}
                              </span>
                            </div>
                            <p className="mt-1 text-[10px] text-slate-500  line-clamp-2 italic">
                              "{cit.snippet}"
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              <div className="text-[9px] opacity-60 text-right">{msg.timestamp}</div>
            </div>

            {msg.sender === 'user' && (
              <div className="h-7 w-7 rounded-lg bg-slate-200  text-slate-700  flex items-center justify-center shrink-0 mt-0.5">
                <User className="h-4 w-4" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-slate-50 /50 text-slate-500 text-xs w-fit">
            <Loader2 className="h-3.5 w-3.5 animate-spin text-teal-600" />
            <span>Consulting Atlas Vector Search & synthesizing answer via Groq Qwen...</span>
          </div>
        )}
      </div>

      {/* Suggested Chips */}
      {messages.length <= 2 && (
        <div className="p-3 border-t border-slate-100  bg-slate-50/40 /40">
          <p className="text-[10px] font-semibold text-slate-600 uppercase tracking-wider mb-1.5">
            Suggested Statutory Queries
          </p>
          <div className="flex flex-wrap gap-1.5">
            {samplePrompts.map((p, i) => (
              <button
                key={i}
                onClick={() => handleSend(p)}
                className="text-[11px] px-2.5 py-1 rounded-lg bg-white  border border-slate-200  hover:border-emerald-400 text-slate-700  hover:text-teal-600 text-left transition-colors"
              >
                {p}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Query Input */}
      <div className="p-3 border-t border-slate-200  bg-white ">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(query);
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            placeholder={
              activeDocument
                ? `Ask about ${activeDocument.document_title.slice(0, 30)}...`
                : 'Ask a question grounded in government service rules...'
            }
            className="flex-1 text-xs px-3.5 py-2.5 rounded-xl border border-slate-300  bg-slate-50  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <Button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="h-9 w-9 p-0 rounded-xl bg-indigo-500 text-white hover:bg-indigo-500 shrink-0"
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </form>
      </div>
    </div>
  );
};

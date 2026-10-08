// ==============================================================================
// AI KARMAYOGI — DOCUMENT VIEWER & CHUNK EXPLORER
// Sovereign Breadcrumbs, Statutory Citations & PyMuPDF Extracted Content
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { DocumentItem, DocumentChunkItem } from '@/types';
import {
  FileText,
  Search,
  BookOpen,
  Copy,
  Check,
  Tag,
  ExternalLink,
  ChevronRight,
  Layers,
  Calendar,
  Building,
  AlertCircle,
  Loader2,
} from 'lucide-react';

interface DocumentViewerProps {
  document: DocumentItem;
  highlightChunkId?: string | null;
  onSelectCitation?: (chunk: DocumentChunkItem) => void;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({
  document,
  highlightChunkId,
  onSelectCitation,
}) => {
  const [chunks, setChunks] = useState<DocumentChunkItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    async function loadDocumentDetails() {
      setIsLoading(true);
      try {
        const data = await api.get<any>(`/documents/${document.id}`);
        setChunks(data.chunks || []);
      } catch (err) {
        console.error('Failed to load document chunks:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadDocumentDetails();
  }, [document.id]);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredChunks = chunks.filter((c) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      c.content.toLowerCase().includes(q) ||
      c.breadcrumb.toLowerCase().includes(q) ||
      `page ${c.page_number}`.includes(q)
    );
  });

  return (
    <div className="flex flex-col h-full bg-white  rounded-2xl border border-slate-200  overflow-hidden shadow-sm">
      {/* Document Header */}
      <div className="p-5 border-b border-slate-200  bg-slate-50/50 /80">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1.5 flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 /60 px-2.5 py-0.5 text-[10px] font-bold text-emerald-700  border border-emerald-200/60 ">
                <Tag className="h-3 w-3" />
                {document.document_type.replace(/_/g, ' ')}
              </span>
              {document.om_number && (
                <span className="text-[11px] font-mono text-slate-500 ">
                  Ref: {document.om_number}
                </span>
              )}
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                  document.processing_status === 'INDEXED'
                    ? 'bg-emerald-50  text-emerald-700  border-emerald-200 '
                    : 'bg-amber-50  text-amber-700  border-amber-200 '
                }`}
              >
                {document.processing_status}
              </span>
            </div>

            <h2 className="text-base font-extrabold text-slate-900 dark:text-slate-100  truncate">
              {document.document_title}
            </h2>

            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 ">
              <span className="flex items-center gap-1">
                <Building className="h-3.5 w-3.5 text-slate-600 dark:text-slate-300" />
                {document.ministry} ({document.department})
              </span>
              {document.issue_date && (
                <span className="flex items-center gap-1">
                  <Calendar className="h-3.5 w-3.5 text-slate-600 dark:text-slate-300" />
                  {document.issue_date}
                </span>
              )}
              <span className="flex items-center gap-1">
                <Layers className="h-3.5 w-3.5 text-slate-600 dark:text-slate-300" />
                {document.total_pages} Pages • {document.total_chunks} Chunks
              </span>
            </div>
          </div>
        </div>

        {/* Search inside Document */}
        <div className="mt-4 relative">
          <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-600 dark:text-slate-300" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search within extracted statutory sections, rules, or keywords..."
            className="w-full text-xs pl-8 pr-3 py-2 rounded-xl border border-slate-200  bg-white  text-slate-900 dark:text-slate-100  placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
      </div>

      {/* Chunks Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 text-slate-600 dark:text-slate-300 gap-2">
            <Loader2 className="h-6 w-6 animate-spin text-teal-600" />
            <span className="text-xs font-medium">Loading extracted document chunks...</span>
          </div>
        ) : filteredChunks.length === 0 ? (
          <div className="text-center py-12 text-slate-600 dark:text-slate-300 text-xs">
            No matching statutory clauses or chunks found.
          </div>
        ) : (
          filteredChunks.map((chunk) => {
            const isHighlighted = highlightChunkId === chunk.id;
            return (
              <div
                key={chunk.id}
                id={`chunk-${chunk.id}`}
                className={`group rounded-xl border p-4 transition-all ${
                  isHighlighted
                    ? 'border-emerald-500 bg-emerald-50/40 /30 ring-2 ring-emerald-500/20'
                    : 'border-slate-200  hover:border-slate-300  bg-white /60'
                }`}
              >
                {/* Breadcrumb Header */}
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-100 /80">
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-teal-600  truncate max-w-[80%]">
                    <BookOpen className="h-3 w-3 shrink-0" />
                    <span className="truncate">{chunk.breadcrumb}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100  text-slate-600 dark:text-slate-300 ">
                      Page {chunk.page_number}
                    </span>
                    <button
                      onClick={() => handleCopy(chunk.content, chunk.id)}
                      title="Copy statutory snippet"
                      className="p-1 rounded hover:bg-slate-100  text-slate-600 dark:text-slate-300 hover:text-slate-600 dark:text-slate-300  transition-colors"
                    >
                      {copiedId === chunk.id ? (
                        <Check className="h-3 w-3 text-teal-600" />
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Statutory text content */}
                <p className="text-xs text-slate-700  leading-relaxed font-normal whitespace-pre-line">
                  {chunk.content}
                </p>

                {/* Footer action */}
                {onSelectCitation && (
                  <div className="mt-2.5 pt-2 border-t border-slate-100 /60 flex justify-end">
                    <button
                      onClick={() => onSelectCitation(chunk)}
                      className="text-[10px] font-semibold text-teal-600  hover:underline flex items-center gap-1"
                    >
                      <span>Cite in Query / MCQ</span>
                      <ChevronRight className="h-2.5 w-2.5" />
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

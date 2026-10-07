// ==============================================================================
// AI KARMAYOGI — 3-COLUMN SOVEREIGN DOCUMENT & RAG TRAINER STUDIO
// Integrated PDF Intelligence, Grounded Sovereign RAG & Bloom-Classified MCQs
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { DocumentItem, DocumentChunkItem, CitationItem, DocumentSummary } from '@/types';
import { PDFUpload } from '@/components/documents/PDFUpload';
import { DocumentViewer } from '@/components/documents/DocumentViewer';
import { RAGChat } from '@/components/documents/RAGChat';
import { SummaryPanel } from '@/components/documents/SummaryPanel';
import { MCQStudio } from '@/components/documents/MCQStudio';
import { Button } from '@/components/ui/button';
import {
  FileText,
  UploadCloud,
  Search,
  BookOpen,
  Sparkles,
  GraduationCap,
  Layers,
  ChevronRight,
  ShieldCheck,
  Building,
  Calendar,
  Tag,
  Filter,
  RefreshCw,
  Info,
  CheckCircle2,
} from 'lucide-react';

export const DocumentStudio: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [activeDocument, setActiveDocument] = useState<DocumentItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('ALL');

  // Center Tab State
  const [centerTab, setCenterTab] = useState<'viewer' | 'rag' | 'mcq'>('viewer');

  // Modal State for Upload
  const [showUploadModal, setShowUploadModal] = useState(false);

  // Citation highlighting in viewer
  const [highlightChunkId, setHighlightChunkId] = useState<string | null>(null);

  // Load all documents on mount
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setIsLoading(true);
    try {
      const data = await api.get<any>('/documents');
      const docs: DocumentItem[] = Array.isArray(data) ? data : (data.documents || []);
      setDocuments(docs);
      if (docs.length > 0 && !activeDocument) {
        setActiveDocument(docs[0]);
      }
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadSuccess = (newDoc: DocumentItem) => {
    setDocuments((prev) => [newDoc, ...prev]);
    setActiveDocument(newDoc);
    setShowUploadModal(false);
    setCenterTab('viewer');
  };

  const handleCitationClick = (citation: CitationItem) => {
    setHighlightChunkId(citation.chunk_id);
    setCenterTab('viewer');
    setTimeout(() => {
      const el = document.getElementById(`chunk-${citation.chunk_id}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  };

  const filteredDocs = documents.filter((d) => {
    const matchesSearch =
      d.document_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.ministry.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (d.om_number && d.om_number.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesType = selectedType === 'ALL' || d.document_type === selectedType;
    return matchesSearch && matchesType;
  });

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 space-y-6">
      {/* Studio Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-6 text-slate-900 border border-slate-200 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-0.5 text-xs font-semibold text-teal-700 border border-teal-200">
              <Sparkles className="h-3.5 w-3.5 text-teal-700" />
              <span>Sovereign Knowledge Engine • Local Ollama Qwen 3.8 27B + Atlas Vector Search</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight">
              Government PDF Intelligence & AI MCQ Studio
            </h1>
            <p className="text-xs text-slate-600">
              Upload Central/State Acts, Rules, OMs and Manuals. Extract statutory breadcrumbs, run grounded RAG queries, and generate Bloom-classified MCQs for Mission Karmayogi.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <Button
              onClick={() => setShowUploadModal(true)}
              className="bg-indigo-500 hover:bg-indigo-500 text-white font-semibold text-xs shadow-lg shadow-emerald-600/30 flex items-center gap-2"
            >
              <UploadCloud className="h-4 w-4" />
              Ingest New PDF
            </Button>
            <Button
              variant="outline"
              onClick={loadDocuments}
              className="text-slate-900 border-slate-200 hover:bg-white/80 text-xs flex items-center gap-1.5"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              Refresh
            </Button>
          </div>
        </div>
      </div>

      {/* 3-Column Studio Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[720px]">
        {/* COLUMN 1 (Left 3 cols): Sovereign Document Library */}
        <div className="lg:col-span-3 flex flex-col bg-white  rounded-2xl border border-slate-200  overflow-hidden shadow-sm h-[720px]">
          <div className="p-4 border-b border-slate-200  bg-slate-50/60 /60 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BookOpen className="h-4 w-4 text-teal-600" />
                <h2 className="text-xs font-bold text-slate-900  uppercase tracking-wider">
                  Knowledge Base ({filteredDocs.length})
                </h2>
              </div>
            </div>

            {/* Search Input */}
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-600" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search documents, OMs..."
                className="w-full text-xs pl-8 pr-3 py-1.5 rounded-lg border border-slate-200  bg-white  text-slate-900  focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            {/* Filter by Type */}
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full text-xs px-2.5 py-1.5 rounded-lg border border-slate-200  bg-white  text-slate-900  focus:outline-none"
            >
              <option value="ALL">All Document Types</option>
              <option value="ACT">Statutory Acts</option>
              <option value="RULES">Service Rules</option>
              <option value="OFFICE_MEMORANDUM">Office Memorandums</option>
              <option value="CIRCULAR">Circulars / Directives</option>
              <option value="MANUAL">Operating Manuals</option>
            </select>
          </div>

          {/* Document List */}
          <div className="flex-1 overflow-y-auto p-2.5 space-y-2">
            {isLoading ? (
              <div className="py-12 text-center text-xs text-slate-600">Loading catalog...</div>
            ) : filteredDocs.length === 0 ? (
              <div className="py-12 text-center text-xs text-slate-600 space-y-2">
                <p>No documents found.</p>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setShowUploadModal(true)}
                  className="text-xs"
                >
                  Upload First PDF
                </Button>
              </div>
            ) : (
              filteredDocs.map((doc) => {
                const isActive = activeDocument?.id === doc.id;
                return (
                  <div
                    key={doc.id}
                    onClick={() => {
                      setActiveDocument(doc);
                      setHighlightChunkId(null);
                    }}
                    className={`cursor-pointer rounded-xl p-3 border transition-all text-left space-y-1.5 ${
                      isActive
                        ? 'border-emerald-500 bg-emerald-50/50 /40 shadow-sm'
                        : 'border-slate-200  hover:border-slate-300  bg-white /60'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-emerald-700  bg-emerald-50  px-1.5 py-0.5 rounded border border-emerald-200/60  truncate max-w-[140px]">
                        {doc.document_type.replace(/_/g, ' ')}
                      </span>
                      <span
                        className={`h-2 w-2 rounded-full ${
                          doc.processing_status === 'INDEXED' ? 'bg-indigo-500' : 'bg-amber-500'
                        }`}
                      />
                    </div>

                    <h3 className="text-xs font-bold text-slate-900  line-clamp-2">
                      {doc.document_title}
                    </h3>

                    <p className="text-[10px] text-slate-500  truncate">
                      {doc.ministry}
                    </p>

                    <div className="flex items-center justify-between pt-1 text-[9px] text-slate-600 font-mono">
                      <span>{doc.total_chunks} Chunks</span>
                      <span>{doc.total_pages} Pages</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* COLUMN 2 (Center 6 cols): Interactive Workspace (Viewer / RAG / MCQ Studio) */}
        <div className="lg:col-span-6 flex flex-col h-[720px] space-y-3">
          {/* Center Navigation Bar */}
          <div className="flex items-center justify-between bg-white  rounded-xl border border-slate-200  p-1 shadow-sm">
            <div className="flex gap-1">
              <button
                onClick={() => setCenterTab('viewer')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  centerTab === 'viewer'
                    ? 'bg-indigo-500 text-slate-900 shadow-sm'
                    : 'text-slate-600  hover:text-slate-900'
                }`}
              >
                <FileText className="h-3.5 w-3.5" />
                <span>Document & Chunks</span>
              </button>

              <button
                onClick={() => setCenterTab('rag')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  centerTab === 'rag'
                    ? 'bg-indigo-500 text-slate-900 shadow-sm'
                    : 'text-slate-600  hover:text-slate-900'
                }`}
              >
                <Sparkles className="h-3.5 w-3.5" />
                <span>Sovereign RAG Copilot</span>
              </button>

              <button
                onClick={() => setCenterTab('mcq')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  centerTab === 'mcq'
                    ? 'bg-indigo-500 text-slate-900 shadow-sm'
                    : 'text-slate-600  hover:text-slate-900'
                }`}
              >
                <GraduationCap className="h-3.5 w-3.5" />
                <span>AI MCQ Studio</span>
              </button>
            </div>
          </div>

          {/* Active Center Component */}
          <div className="flex-1 min-h-0">
            {activeDocument ? (
              centerTab === 'viewer' ? (
                <DocumentViewer
                  document={activeDocument}
                  highlightChunkId={highlightChunkId}
                  onSelectCitation={() => setCenterTab('rag')}
                />
              ) : centerTab === 'rag' ? (
                <RAGChat
                  activeDocument={activeDocument}
                  onCitationClick={handleCitationClick}
                />
              ) : (
                <MCQStudio
                  document={activeDocument}
                  onPublished={() => loadDocuments()}
                />
              )
            ) : (
              <div className="flex flex-col items-center justify-center h-full bg-white  rounded-2xl border border-slate-200  p-8 text-center text-slate-500 space-y-3">
                <FileText className="h-10 w-10 text-slate-600 " />
                <p className="text-xs">Select or upload a sovereign document to begin.</p>
                <Button
                  onClick={() => setShowUploadModal(true)}
                  className="text-xs bg-indigo-500 text-white"
                >
                  Upload Central Act / OM
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* COLUMN 3 (Right 3 cols): Sovereign Intelligence Summary & Citations */}
        <div className="lg:col-span-3 flex flex-col h-[720px]">
          {activeDocument ? (
            <SummaryPanel
              document={activeDocument}
              onSummaryUpdated={(updatedSummary) => {
                setActiveDocument((prev) => (prev ? { ...prev, summary_json: updatedSummary } : prev));
              }}
            />
          ) : (
            <div className="flex flex-col items-center justify-center h-full bg-white  rounded-2xl border border-slate-200  p-6 text-center text-slate-600 text-xs">
              <Info className="h-6 w-6 text-slate-600  mb-2" />
              <span>Select a document to inspect 6-part AI summary & citations.</span>
            </div>
          )}
        </div>
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="w-full max-w-xl">
            <PDFUpload
              onUploadSuccess={handleUploadSuccess}
              onCancel={() => setShowUploadModal(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

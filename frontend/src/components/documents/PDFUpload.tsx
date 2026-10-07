// ==============================================================================
// AI KARMAYOGI — SOVEREIGN PDF UPLOAD COMPONENT
// Drag-and-Drop Government Policy PDF Upload with Metadata Extraction
// ==============================================================================

import React, { useState, useRef } from 'react';
import { api, APIClientError } from '@/lib/api';
import { DocumentItem } from '@/types';
import { Button } from '@/components/ui/button';
import {
  UploadCloud,
  FileText,
  AlertCircle,
  Loader2,
  X,
  FileCheck,
} from 'lucide-react';

interface PDFUploadProps {
  onUploadSuccess: (doc: DocumentItem) => void;
  onCancel?: () => void;
}

const DOCUMENT_TYPES = [
  { value: 'ACT', label: 'Statutory Act' },
  { value: 'RULES', label: 'Government Rules / Service Rules' },
  { value: 'OFFICE_MEMORANDUM', label: 'Office Memorandum (OM)' },
  { value: 'CIRCULAR', label: 'Official Circular / Directive' },
  { value: 'MANUAL', label: 'Operating Manual / Handbook' },
  { value: 'GAZETTE_NOTIFICATION', label: 'Gazette Notification' },
];

const MINISTRIES = [
  'Ministry of Personnel, Public Grievances and Pensions',
  'Ministry of Finance (Department of Expenditure)',
  'Ministry of Home Affairs',
  'Ministry of Electronics and Information Technology (MeitY)',
  'Ministry of Defence',
  'Ministry of External Affairs',
  'Ministry of Health and Family Welfare',
  'Ministry of Railways',
  'Cabinet Secretariat',
  'NITI Aayog',
];

export const PDFUpload: React.FC<PDFUploadProps> = ({ onUploadSuccess, onCancel }) => {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [docType, setDocType] = useState('OFFICE_MEMORANDUM');
  const [ministry, setMinistry] = useState(MINISTRIES[0]);
  const [department, setDepartment] = useState('DoPT');
  const [omNumber, setOmNumber] = useState('');
  const [issueDate, setIssueDate] = useState('');

  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStep, setUploadStep] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelection = (selectedFile: File) => {
    setError(null);
    if (selectedFile.type !== 'application/pdf' && !selectedFile.name.toLowerCase().endsWith('.pdf')) {
      setError('Only sovereign PDF documents are accepted (.pdf).');
      return;
    }
    const maxBytes = 50 * 1024 * 1024; // 50MB
    if (selectedFile.size > maxBytes) {
      setError('File size exceeds the 50MB sovereign upload limit.');
      return;
    }
    setFile(selectedFile);
    if (!title) {
      const cleanName = selectedFile.name.replace(/\.pdf$/i, '').replace(/[_-]/g, ' ');
      setTitle(cleanName);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF document to upload.');
      return;
    }
    if (!title.trim()) {
      setError('Please provide a document title.');
      return;
    }

    setIsUploading(true);
    setError(null);
    setUploadProgress(20);
    setUploadStep('Validating SHA-256 hash & uploading payload...');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title.trim());
    formData.append('document_type', docType);
    formData.append('ministry', ministry);
    formData.append('department', department.trim());
    if (omNumber) formData.append('om_number', omNumber.trim());
    if (issueDate) formData.append('issue_date', issueDate);

    try {
      setUploadProgress(45);
      setUploadStep('Extracting structure with PyMuPDF & statutory breadcrumbs...');

      const progressTimer = setTimeout(() => {
        setUploadProgress(75);
        setUploadStep('Generating 768-dim dense embeddings via Atlas Vector Search...');
      }, 1200);

      const response = await api.post<DocumentItem>('/documents/upload', formData);
      clearTimeout(progressTimer);

      setUploadProgress(100);
      setUploadStep('Indexing complete! Sovereign RAG is now live.');
      setTimeout(() => {
        onUploadSuccess(response);
      }, 500);
    } catch (err: any) {
      setIsUploading(false);
      if (err instanceof APIClientError) {
        setError(err.message);
      } else {
        setError(err.message || 'Failed to upload and index document.');
      }
    }
  };

  return (
    <div className="bg-white  rounded-2xl border border-slate-200  p-6 shadow-xl">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 ">
        <div className="flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-xl bg-emerald-50 /60 text-teal-600  flex items-center justify-center">
            <UploadCloud className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 ">
              Sovereign Document Ingestion Studio
            </h3>
            <p className="text-xs text-slate-500">
              Upload Central / State Government Acts, Rules, OMs, or Manuals (Max 50MB)
            </p>
          </div>
        </div>
        {onCancel && (
          <button
            onClick={onCancel}
            className="p-1 rounded-lg text-slate-600 hover:text-slate-600  hover:bg-slate-100"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {error && (
        <div className="mt-4 p-3 rounded-xl bg-rose-50 /40 border border-rose-200  text-xs text-rose-700  flex items-start gap-2">
          <AlertCircle className="h-4 w-4 mt-0.5 shrink-0" />
          <div>
            <p className="font-semibold">Upload Error</p>
            <p className="mt-0.5">{error}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-5 space-y-4">
        {!file ? (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition-colors ${
              isDragging
                ? 'border-emerald-500 bg-emerald-50/50 /20'
                : 'border-slate-300  hover:border-emerald-400  bg-slate-50/50 /30'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              className="hidden"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleFileSelection(e.target.files[0]);
                }
              }}
            />
            <FileText className="mx-auto h-10 w-10 text-slate-600  mb-2" />
            <p className="text-xs font-semibold text-slate-700 ">
              Drag and drop sovereign policy PDF here, or <span className="text-teal-600  underline">browse</span>
            </p>
            <p className="text-[11px] text-slate-600 mt-1">
              Supports GFR 2017, CCS Conduct Rules, Procurement Guidelines, OMs up to 50MB
            </p>
          </div>
        ) : (
          <div className="flex items-center justify-between p-3 rounded-xl bg-emerald-50/60 /30 border border-emerald-200 ">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-lg bg-indigo-500 text-white flex items-center justify-center">
                <FileCheck className="h-5 w-5" />
              </div>
              <div className="text-left">
                <p className="text-xs font-bold text-slate-900  truncate max-w-xs sm:max-w-md">
                  {file.name}
                </p>
                <p className="text-[10px] text-slate-500">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB • Ready for PyMuPDF extraction
                </p>
              </div>
            </div>
            <button
              type="button"
              disabled={isUploading}
              onClick={() => setFile(null)}
              className="text-xs text-slate-600 hover:text-rose-500 p-1"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              Document Title <span className="text-rose-500">*</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. General Financial Rules (GFR) 2017 - Rule 149 GeM Mandate"
              required
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              Document Classification <span className="text-rose-500">*</span>
            </label>
            <select
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              {DOCUMENT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              Issuing Ministry / Authority
            </label>
            <select
              value={ministry}
              onChange={(e) => setMinistry(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              {MINISTRIES.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              Department / Wing
            </label>
            <input
              type="text"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              placeholder="e.g. DoPT, Procurement Policy Division"
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              OM / Circular / Gazette Reference
            </label>
            <input
              type="text"
              value={omNumber}
              onChange={(e) => setOmNumber(e.target.value)}
              placeholder="e.g. F.No. 6/1/2023-PPD"
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700  mb-1">
              Issue / Notification Date
            </label>
            <input
              type="date"
              value={issueDate}
              onChange={(e) => setIssueDate(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300  bg-white  text-slate-900  focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
        </div>

        {isUploading && (
          <div className="pt-2 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-teal-600  flex items-center gap-1.5">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                {uploadStep}
              </span>
              <span className="font-mono text-slate-500">{uploadProgress}%</span>
            </div>
            <div className="h-1.5 w-full bg-slate-100  rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-emerald-500 transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100 ">
          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isUploading}
              className="text-xs"
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            disabled={!file || isUploading}
            className="bg-indigo-500 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/20 flex items-center gap-2"
          >
            {isUploading ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Indexing Sovereign Knowledge...
              </>
            ) : (
              <>
                <FileCheck className="h-3.5 w-3.5" />
                Ingest & Index Document
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
};

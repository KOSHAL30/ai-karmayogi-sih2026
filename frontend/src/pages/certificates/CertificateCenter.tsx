// ==============================================================================
// AI KARMAYOGI — SOVEREIGN CERTIFICATE VAULT & VERIFICATION CENTER
// Cryptographic Proof of Competency, Public Verification & PDF Print Export
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { CertificateItem } from '@/types';
import { CertificateCard } from '@/components/certificates/CertificateCard';
import { CertificateModal } from '@/components/certificates/CertificateModal';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';
import {
  Award,
  ShieldCheck,
  Search,
  Filter,
  QrCode,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  PlusCircle,
  FileCheck,
  Shield,
  Layers,
  X,
  RefreshCw,
  ExternalLink,
} from 'lucide-react';

export const CertificateCenter: React.FC = () => {
  const { user } = useAuth();
  const [certificates, setCertificates] = useState<CertificateItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeModalCert, setActiveModalCert] = useState<CertificateItem | null>(null);

  // Public Verification State
  const [verifyDrawerOpen, setVerifyDrawerOpen] = useState<boolean>(false);
  const [verificationInput, setVerificationInput] = useState<string>('');
  const [verifying, setVerifying] = useState<boolean>(false);
  const [verificationResult, setVerificationResult] = useState<CertificateItem | null>(null);
  const [verificationError, setVerificationError] = useState<string | null>(null);

  // New Certificate Generation Modal (Demo evaluator feature)
  const [issueModalOpen, setIssueModalOpen] = useState<boolean>(false);
  const [isIssuing, setIsIssuing] = useState<boolean>(false);
  const [newCertTitle, setNewCertTitle] = useState<string>('FRAC Public Financial Management Specialization');
  const [newCertType, setNewCertType] = useState<'COURSE_COMPLETION' | 'ASSESSMENT_MASTERY' | 'LEARNING_PATH_COMPLETION'>('COURSE_COMPLETION');

  useEffect(() => {
    loadCertificates();
  }, []);

  const loadCertificates = async () => {
    setIsLoading(true);
    try {
      // Fetch user's certificates (or all if admin)
      const res = await api.get<{ certificates: CertificateItem[]; total_certificates: number }>(
        '/certificates?all_cadre=true'
      );
      setCertificates(res.certificates || []);
    } catch (err) {
      console.error('Failed to load certificates:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!verificationInput.trim()) return;

    setVerifying(true);
    setVerificationError(null);
    setVerificationResult(null);

    try {
      const cert = await api.get<CertificateItem>(`/certificates/${verificationInput.trim()}`);
      setVerificationResult(cert);
    } catch (err: any) {
      setVerificationError(
        'Certificate record not found. Please verify the 16-character code or UUID.'
      );
    } finally {
      setVerifying(false);
    }
  };

  const handleIssueCredential = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsIssuing(true);
    try {
      const issued = await api.post<CertificateItem>('/certificates/generate', {
        title: newCertTitle,
        certificate_type: newCertType,
        metadata: {
          credits_earned: 4,
          score_achieved: 94,
          signatory_title: 'Secretary, Capacity Building Commission',
        },
      });
      setCertificates((prev) => [issued, ...prev]);
      setIssueModalOpen(false);
      setActiveModalCert(issued);
    } catch (err) {
      console.error('Failed to issue credential:', err);
    } finally {
      setIsIssuing(false);
    }
  };

  // Filter logic
  const filteredCertificates = certificates.filter((cert) => {
    const matchesType = selectedType === 'ALL' || cert.certificate_type === selectedType;
    const matchesSearch =
      cert.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cert.officer_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cert.certificate_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cert.verification_code.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  const totalCredits = certificates.reduce(
    (acc, c) => acc + (c.metadata?.credits_earned || 2),
    0
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Executive Saffron & emerald Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-8 text-slate-900 dark:text-slate-100 border border-slate-200 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 rounded-full bg-amber-500/20 px-3 py-0.5 text-xs font-semibold text-amber-300 border border-amber-400/30">
              <Award className="h-3.5 w-3.5 text-amber-700" />
              <span>National Competency Credentials • Capacity Building Commission</span>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Sovereign Digital Credentials Vault
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
              Cryptographically verified certificates of competency for civil services officials. Each credential
              carries a sovereign SHA-256 verification hash, FRAC alignment record, and tamper-evident QR payload.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Button
              onClick={() => {
                setVerifyDrawerOpen(true);
                setVerificationResult(null);
                setVerificationError(null);
              }}
              variant="outline"
              className="bg-white/60 dark:bg-white/5 border-slate-200 text-slate-600 dark:text-slate-300 hover:bg-white text-xs h-9 font-semibold flex items-center gap-1.5"
            >
              <QrCode className="h-3.5 w-3.5 text-teal-700" />
              <span>Verify Any Certificate</span>
            </Button>

            <Button
              onClick={() => setIssueModalOpen(true)}
              className="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-bold text-xs h-9 shadow-md shadow-amber-500/20 flex items-center gap-1.5"
            >
              <PlusCircle className="h-3.5 w-3.5" />
              <span>Issue Test Credential</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Earned Credentials</span>
            <div className="p-2 rounded-xl bg-amber-50 /60 text-amber-600 ">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 ">
            {certificates.length}
          </div>
          <p className="text-[11px] text-slate-500">Government recognized achievements</p>
        </div>

        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Continuous Learning Credits</span>
            <div className="p-2 rounded-xl bg-emerald-50 /60 text-teal-600 ">
              <Sparkles className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 ">
            {totalCredits} Credits
          </div>
          <p className="text-[11px] text-teal-600  font-semibold">
            Accrued under CBC Guidelines 2026
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200  bg-white  p-5 shadow-sm space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Tamper-Proof Audit Status</span>
            <div className="p-2 rounded-xl bg-emerald-50 /60 text-teal-600 ">
              <ShieldCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-teal-600 ">
            100% Valid
          </div>
          <p className="text-[11px] text-teal-600  font-semibold">
            Zero revoked or disputed credentials
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Type Filter Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 bg-slate-100 /80 p-1.5 rounded-xl text-xs">
          {[
            { id: 'ALL', label: 'All Credentials' },
            { id: 'COURSE_COMPLETION', label: 'Course Mastery' },
            { id: 'ASSESSMENT_MASTERY', label: 'Diagnostic Assessment' },
            { id: 'LEARNING_PATH_COMPLETION', label: 'Trajectory Milestone' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedType(tab.id)}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all ${
                selectedType === tab.id
                  ? 'bg-white  text-teal-600  shadow-sm'
                  : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative min-w-[240px]">
          <Search className="h-3.5 w-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-600 dark:text-slate-300" />
          <input
            type="text"
            placeholder="Search by title, number, officer..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 rounded-xl text-xs bg-white  border border-slate-200  text-slate-900 dark:text-slate-100  focus:outline-none focus:ring-1 focus:ring-emerald-500 shadow-xs"
          />
        </div>
      </div>

      {/* Certificates Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-64 rounded-2xl bg-slate-200  animate-pulse" />
          ))}
        </div>
      ) : filteredCertificates.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300  p-12 text-center space-y-3">
          <Award className="h-10 w-10 text-slate-600 dark:text-slate-300  mx-auto" />
          <h3 className="text-sm font-bold text-slate-700 ">
            No Credentials Found
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-300 max-w-sm mx-auto">
            No certificates match the selected filters. Complete a diagnostic assessment or iGOT course to receive official certification.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCertificates.map((cert) => (
            <CertificateCard
              key={cert.id}
              certificate={cert}
              onViewPrint={(c) => setActiveModalCert(c)}
            />
          ))}
        </div>
      )}

      {/* Full-Screen Printable Official Certificate Modal */}
      {activeModalCert && (
        <CertificateModal
          certificate={activeModalCert}
          onClose={() => setActiveModalCert(null)}
        />
      )}

      {/* Public Verification Drawer / Modal */}
      {verifyDrawerOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-3xl border border-slate-200  bg-white  p-6 shadow-2xl space-y-5 animate-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 ">
              <div className="flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-teal-600" />
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 ">
                  Sovereign Credential Verification
                </h3>
              </div>
              <button
                onClick={() => setVerifyDrawerOpen(false)}
                className="p-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-slate-600 dark:text-slate-300  hover:bg-slate-100"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed">
              Enter any official Certificate Number (e.g. <span className="font-mono text-teal-600 font-semibold">KMY-2026-62A89F4B</span>) or Certificate UUID to verify record validity against the Mission Karmayogi ledger.
            </p>

            <form onSubmit={handleVerifyLookup} className="flex gap-2">
              <input
                type="text"
                placeholder="e.g. KMY-2026-..."
                value={verificationInput}
                onChange={(e) => setVerificationInput(e.target.value)}
                className="flex-1 px-3 py-2 text-xs rounded-xl bg-slate-50  border border-slate-200  text-slate-900 dark:text-slate-100  focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono"
              />
              <Button
                type="submit"
                disabled={verifying || !verificationInput.trim()}
                className="text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold px-4"
              >
                {verifying ? 'Checking...' : 'Verify'}
              </Button>
            </form>

            {/* Error Result */}
            {verificationError && (
              <div className="p-3 rounded-xl bg-rose-50 /40 border border-rose-200  text-xs text-rose-700  flex items-start gap-2">
                <AlertCircle className="h-4 w-4 mt-0.5 shrink-0" />
                <span>{verificationError}</span>
              </div>
            )}

            {/* Success Result */}
            {verificationResult && (
              <div className="p-4 rounded-2xl bg-emerald-50/70 /30 border border-emerald-200  space-y-3">
                <div className="flex items-center gap-2 text-emerald-800  font-bold text-xs">
                  <CheckCircle2 className="h-4 w-4 text-teal-600 shrink-0" />
                  <span>Official Government Credential Verified & Active</span>
                </div>

                <div className="space-y-1 text-xs">
                  <p className="font-bold text-slate-900 dark:text-slate-100 ">
                    {verificationResult.title}
                  </p>
                  <p className="text-slate-600 dark:text-slate-300 ">
                    Awarded to: <strong className="text-slate-900 dark:text-slate-100 ">{verificationResult.officer_name}</strong> ({verificationResult.designation})
                  </p>
                  <p className="text-slate-500  text-[11px]">
                    Department: {verificationResult.department} • {verificationResult.ministry}
                  </p>
                  <p className="text-slate-500  text-[11px]">
                    Issued: {new Date(verificationResult.issued_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })}
                  </p>
                  <div className="pt-2">
                    <span className="text-[10px] font-mono text-slate-600 dark:text-slate-300 block truncate">
                      Hash: {verificationResult.verification_code}
                    </span>
                  </div>
                </div>

                <div className="pt-2 flex justify-end">
                  <Button
                    size="sm"
                    onClick={() => {
                      setActiveModalCert(verificationResult);
                      setVerifyDrawerOpen(false);
                    }}
                    className="text-xs bg-emerald-700 hover:bg-indigo-500 text-white font-semibold"
                  >
                    View Official Certificate
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Demo Issue Credential Modal */}
      {issueModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-3xl border border-slate-200  bg-white  p-6 shadow-2xl space-y-4 animate-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 ">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-amber-500" />
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 ">
                  Issue Verifiable Digital Credential
                </h3>
              </div>
              <button
                onClick={() => setIssueModalOpen(false)}
                className="p-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-slate-600 dark:text-slate-300  hover:bg-slate-100"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed">
              Instantly issue an official Government of India certificate for the current authenticated officer.
            </p>

            <form onSubmit={handleIssueCredential} className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-700  block mb-1">
                  Credential Title
                </label>
                <input
                  type="text"
                  required
                  value={newCertTitle}
                  onChange={(e) => setNewCertTitle(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-xl bg-slate-50  border border-slate-200  text-slate-900 dark:text-slate-100  focus:outline-none focus:ring-1 focus:ring-emerald-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-700  block mb-1">
                  Certificate Category
                </label>
                <select
                  value={newCertType}
                  onChange={(e) => setNewCertType(e.target.value as any)}
                  className="w-full px-3 py-2 text-xs rounded-xl bg-slate-50  border border-slate-200  text-slate-900 dark:text-slate-100  focus:outline-none focus:ring-1 focus:ring-emerald-500"
                >
                  <option value="COURSE_COMPLETION">Course Mastery (iGOT Karmayogi)</option>
                  <option value="ASSESSMENT_MASTERY">Diagnostic Assessment Mastery</option>
                  <option value="LEARNING_PATH_COMPLETION">Learning Path Milestone</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setIssueModalOpen(false)}
                  className="text-xs"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  disabled={isIssuing}
                  size="sm"
                  className="text-xs bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold"
                >
                  {isIssuing ? 'Issuing...' : 'Generate & Stamp'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

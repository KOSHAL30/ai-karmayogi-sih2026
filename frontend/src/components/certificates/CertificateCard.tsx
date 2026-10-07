// ==============================================================================
// AI KARMAYOGI — VERIFIABLE CERTIFICATE CARD
// Sovereign Credential Display with Gold Accents, QR Verification & Print Actions
// ==============================================================================

import React, { useState } from 'react';
import { CertificateItem } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Award,
  ShieldCheck,
  Calendar,
  ExternalLink,
  Printer,
  Copy,
  Check,
  Building,
  QrCode,
} from 'lucide-react';

interface CertificateCardProps {
  certificate: CertificateItem;
  onViewPrint: (cert: CertificateItem) => void;
}

export const CertificateCard: React.FC<CertificateCardProps> = ({
  certificate,
  onViewPrint,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopyLink = () => {
    navigator.clipboard.writeText(certificate.verification_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getBadgeType = (type: string) => {
    switch (type) {
      case 'COURSE_COMPLETION':
        return { label: 'Course Mastery', bg: 'bg-emerald-50 text-emerald-700   border-emerald-200 ' };
      case 'ASSESSMENT_MASTERY':
        return { label: 'Diagnostic Assessment', bg: 'bg-emerald-50 text-emerald-700   border-emerald-200 ' };
      case 'LEARNING_PATH_COMPLETION':
      default:
        return { label: 'Trajectory Milestone', bg: 'bg-amber-50 text-amber-700   border-amber-200 ' };
    }
  };

  const badge = getBadgeType(certificate.certificate_type);

  return (
    <div className="relative overflow-hidden rounded-2xl border-2 border-slate-200  bg-white  p-6 shadow-md hover:shadow-xl transition-all duration-200 flex flex-col justify-between group">
      {/* Top Sovereign Indian Tricolor Accent */}
      <div className="absolute top-0 left-0 right-0 h-1.5 bg-indigo-600 shadow-xs" />

      <div className="space-y-4">
        {/* Header Badges & Emblem */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="h-10 w-10 rounded-xl bg-amber-50 /60 text-amber-600  border border-amber-200  flex items-center justify-center shadow-sm">
              <Award className="h-5 w-5" />
            </div>
            <div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${badge.bg}`}>
                {badge.label}
              </span>
              <p className="text-[10px] font-mono text-slate-600 mt-1">
                {certificate.certificate_number}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1 text-[10px] font-semibold text-teal-600  bg-emerald-50 /60 px-2 py-0.5 rounded-full border border-emerald-200 ">
            <ShieldCheck className="h-3 w-3" />
            <span>Verified</span>
          </div>
        </div>

        {/* Certificate Title */}
        <div>
          <h4 className="text-sm font-extrabold text-slate-900  line-clamp-2 leading-snug group-hover:text-teal-600 :text-teal-700 transition-colors">
            {certificate.title}
          </h4>
          <p className="text-xs text-slate-500  mt-1">
            Awarded to <span className="font-semibold text-slate-800 ">{certificate.officer_name}</span> ({certificate.designation})
          </p>
        </div>

        {/* Authority & Ministry */}
        <div className="p-2.5 rounded-xl bg-slate-50 /50 border border-slate-100  text-[11px] text-slate-600  space-y-1">
          <div className="flex items-center gap-1.5 truncate">
            <Building className="h-3.5 w-3.5 text-slate-600 shrink-0" />
            <span className="truncate">{certificate.department} • {certificate.ministry}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar className="h-3.5 w-3.5 text-slate-600 shrink-0" />
            <span>Issued: {new Date(certificate.issued_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
        </div>

        {/* Verification Code */}
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 bg-slate-100  px-3 py-1.5 rounded-lg">
          <span>Code: {certificate.verification_code}</span>
          <button
            onClick={handleCopyLink}
            title="Copy Public Verification Link"
            className="text-slate-600 hover:text-teal-600  transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-teal-600" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
        </div>
      </div>

      {/* Card Footer Actions */}
      <div className="pt-4 mt-4 border-t border-slate-100  flex items-center justify-between gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={handleCopyLink}
          className="text-xs text-slate-600  flex items-center gap-1 flex-1"
        >
          <ExternalLink className="h-3 w-3" />
          <span>Verify</span>
        </Button>

        <Button
          size="sm"
          onClick={() => onViewPrint(certificate)}
          className="text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold flex items-center gap-1.5 shadow-sm flex-1"
        >
          <Printer className="h-3 w-3" />
          <span>View / Print PDF</span>
        </Button>
      </div>
    </div>
  );
};

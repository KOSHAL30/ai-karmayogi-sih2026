// ==============================================================================
// AI KARMAYOGI — GAP SUMMARY CARD COMPONENT
// Executive Metric Summary Across Core FRAC Pillars
// ==============================================================================

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Award, BookOpen, Scale, Shield, CheckCircle2 } from 'lucide-react';

interface GapSummaryCardProps {
  overallScore: number;
  overallStatus: string;
  behavioralScore: number;
  functionalScore: number;
  domainScore: number;
  compositeDeficitPct: number;
}

export const GapSummaryCard: React.FC<GapSummaryCardProps> = ({
  overallScore,
  overallStatus,
  behavioralScore,
  functionalScore,
  domainScore,
  compositeDeficitPct,
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'EXEMPLARY':
        return {
          label: 'Exemplary Mastery',
          classes: 'bg-emerald-100 /60 text-emerald-800  border-emerald-300',
        };
      case 'COMPETENT':
        return {
          label: 'Mandate Competent',
          classes: 'bg-emerald-100 /60 text-emerald-800  border-emerald-300',
        };
      case 'MODERATE_DEFICIT':
        return {
          label: 'Moderate Gaps Detected',
          classes: 'bg-amber-100 /60 text-amber-800  border-amber-300',
        };
      case 'ACUTE_DEFICIT':
      default:
        return {
          label: 'Acute Deficit (Priority ACBP)',
          classes: 'bg-rose-100 /60 text-rose-800  border-rose-300',
        };
    }
  };

  const statusInfo = getStatusBadge(overallStatus);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Overall Score */}
      <Card className="border-emerald-200  bg-gradient-to-br from-emerald-50/50 to-white   shadow-sm">
        <CardContent className="p-5 flex flex-col justify-between h-full space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-700  uppercase tracking-wider">
              Overall Score
            </span>
            <div className="h-8 w-8 rounded-lg bg-indigo-500 text-white flex items-center justify-center shadow-sm shadow-emerald-600/20">
              <Award className="h-4 w-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-slate-900  tracking-tight">
              {overallScore.toFixed(1)}%
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Composite Deficit: {compositeDeficitPct.toFixed(1)}%
            </p>
          </div>
          <div className="pt-2 border-t border-emerald-100 ">
            <span className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full border ${statusInfo.classes}`}>
              {statusInfo.label}
            </span>
          </div>
        </CardContent>
      </Card>

      {/* 2. Functional Score */}
      <Card className="border-slate-200  shadow-sm">
        <CardContent className="p-5 flex flex-col justify-between h-full space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Functional Pillar
            </span>
            <div className="h-8 w-8 rounded-lg bg-cyan-100 /60 text-cyan-700  flex items-center justify-center">
              <BookOpen className="h-4 w-4" />
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-slate-900 ">
              {functionalScore.toFixed(1)}%
            </div>
            <p className="text-[11px] text-slate-500 mt-1">GFR 2017, CSMOP, GeM</p>
          </div>
          <div className="w-full bg-slate-100  h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-cyan-600 h-full rounded-full transition-all"
              style={{ width: `${functionalScore}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* 3. Domain Score */}
      <Card className="border-slate-200  shadow-sm">
        <CardContent className="p-5 flex flex-col justify-between h-full space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Domain Pillar
            </span>
            <div className="h-8 w-8 rounded-lg bg-teal-100 /60 text-teal-700  flex items-center justify-center">
              <Scale className="h-4 w-4" />
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-slate-900 ">
              {domainScore.toFixed(1)}%
            </div>
            <p className="text-[11px] text-slate-500 mt-1">RTI Act, Establishment Rules</p>
          </div>
          <div className="w-full bg-slate-100  h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-teal-600 h-full rounded-full transition-all"
              style={{ width: `${domainScore}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* 4. Behavioral Score */}
      <Card className="border-slate-200  shadow-sm">
        <CardContent className="p-5 flex flex-col justify-between h-full space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Behavioral Pillar
            </span>
            <div className="h-8 w-8 rounded-lg bg-purple-100 /60 text-purple-700  flex items-center justify-center">
              <Shield className="h-4 w-4" />
            </div>
          </div>
          <div>
            <div className="text-2xl font-extrabold text-slate-900 ">
              {behavioralScore.toFixed(1)}%
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Ethics, Citizen Empathy</p>
          </div>
          <div className="w-full bg-slate-100  h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-purple-600 h-full rounded-full transition-all"
              style={{ width: `${behavioralScore}%` }}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

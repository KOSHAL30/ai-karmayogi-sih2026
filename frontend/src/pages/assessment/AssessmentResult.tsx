// ==============================================================================
// AI KARMAYOGI — COMPETENCY DIAGNOSTIC RESULT DOSSIER
// Radar Profile, Multi-Pillar Heatmap, and Explainable AI (XAI) Gap Analysis
// ==============================================================================

import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '@/lib/api';
import { AssessmentResultData } from '@/types';
import { GapSummaryCard } from '@/components/assessment/GapSummaryCard';
import { RadarChartCard } from '@/components/assessment/RadarChartCard';
import { CompetencyHeatmap } from '@/components/assessment/CompetencyHeatmap';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Compass,
  Award,
  Shield,
  Printer,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  HelpCircle,
  FileCheck,
  Scale,
  Sparkles,
} from 'lucide-react';

export const AssessmentResult: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  const [dossier, setDossier] = useState<AssessmentResultData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadResult() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await api.get<AssessmentResultData>(`/assessment/result/${id}`);
        setDossier(data);
      } catch (err: any) {
        setError(err.message || 'Failed to retrieve assessment results.');
      } finally {
        setLoading(false);
      }
    }
    loadResult();
  }, [id]);

  if (loading) {
    return (
      <div className="flex min-h-[65vh] items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-600 border-t-transparent" />
          <p className="text-sm font-semibold text-slate-600 ">
            Compiling FRAC competency gap matrix & XAI diagnostic rationale...
          </p>
        </div>
      </div>
    );
  }

  if (error || !dossier) {
    return (
      <div className="mx-auto max-w-lg px-4 py-16 text-center space-y-4">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-100 text-rose-600">
          <AlertTriangle className="h-6 w-6" />
        </div>
        <h2 className="text-lg font-bold text-slate-900 ">Dossier Unavailable</h2>
        <p className="text-xs text-slate-500">{error || 'Could not find the requested assessment record.'}</p>
        <Link to="/assessment">
          <Button>Return to Assessment Dashboard</Button>
        </Link>
      </div>
    );
  }

  const formatMinutes = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m}m ${s}s`;
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8 print:p-2 print:space-y-4">
      {/* 1. Official Government Header Dossier */}
      <div className="rounded-2xl border border-slate-200  bg-white  p-6 shadow-sm flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-indigo-500" />
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              National Programme for Civil Services Capacity Building (NPCSCB)
            </span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-slate-900  flex items-center gap-2">
            Competency Diagnostic Dossier
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50  text-emerald-700  border border-emerald-200 ">
              FRAC Certified
            </span>
          </h1>
          <p className="text-xs text-slate-500 ">
            Evaluated Officer: <strong className="text-slate-800 ">{dossier.officer_name}</strong> ({dossier.designation}) • {dossier.department}
          </p>
          <p className="text-[11px] text-slate-600">
            Work-Based Role: <span className="font-semibold text-slate-600 ">{dossier.work_role}</span> • Evaluated in {formatMinutes(dossier.time_taken_seconds)} ({dossier.score_achieved}/{dossier.total_questions} scenarios mastered)
          </p>
        </div>

        <div className="flex items-center gap-3 self-start md:self-auto print:hidden">
          <Button
            variant="outline"
            size="sm"
            onClick={() => window.print()}
            className="text-xs text-slate-700  flex items-center gap-1.5"
          >
            <Printer className="h-3.5 w-3.5" />
            Print Official Dossier
          </Button>
          <Link to="/assessment">
            <Button size="sm" className="text-xs">
              Dashboard
            </Button>
          </Link>
        </div>
      </div>

      {/* 2. Executive Metric Cards */}
      <GapSummaryCard
        overallScore={dossier.overall_score}
        overallStatus={dossier.overall_status}
        behavioralScore={dossier.behavioral_score}
        functionalScore={dossier.functional_score}
        domainScore={dossier.domain_score}
        compositeDeficitPct={dossier.composite_deficit_pct}
      />

      {/* 3. Deep Analytical Visualizations (Radar Chart & Severity Heatmap) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <RadarChartCard competencies={dossier.competency_results} />
        <CompetencyHeatmap competencies={dossier.competency_results} />
      </div>

      {/* 4. Strengths & Development Areas Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-emerald-200  bg-emerald-50/30 /10 shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2 text-emerald-800 ">
              <CheckCircle2 className="h-4 w-4 text-teal-600" />
              Demonstrated Cadre Strengths
            </CardTitle>
          </CardHeader>
          <CardContent>
            {dossier.strengths.length === 0 ? (
              <p className="text-xs text-slate-500">Baseline established across all competency nodes.</p>
            ) : (
              <ul className="space-y-1.5 text-xs text-slate-700 ">
                {dossier.strengths.map((str, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-teal-600 font-bold">✓</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card className="border-amber-200  bg-amber-50/30 /10 shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2 text-amber-800 ">
              <AlertTriangle className="h-4 w-4 text-amber-600" />
              Priority Capacity Building Focus
            </CardTitle>
          </CardHeader>
          <CardContent>
            {dossier.weaknesses.length === 0 ? (
              <p className="text-xs text-slate-500">No acute competency deficits identified.</p>
            ) : (
              <ul className="space-y-1.5 text-xs text-slate-700 ">
                {dossier.weaknesses.map((wk, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-amber-600 font-bold">•</span>
                    <span>{wk}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      </div>

      {/* 5. Granular Competency Breakdown with Deterministic XAI Explanations */}
      <Card className="border-slate-200  shadow-sm">
        <CardHeader className="pb-3 border-b border-slate-100 ">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <CardTitle className="text-base flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-teal-600" />
                Explainable AI (XAI) Diagnostic Rationale
              </CardTitle>
              <CardDescription className="text-xs">
                Transparent, rule-grounded administrative explanations for all evaluated competency vectors.
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="divide-y divide-slate-100  p-0">
          {dossier.competency_results.map((comp) => (
            <div key={comp.competency_id} className="p-5 space-y-2.5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900 ">
                    {comp.competency_name}
                  </span>
                  <span className="text-[10px] font-mono text-slate-600">
                    ({comp.competency_code})
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-slate-500">
                    Mandated: <strong className="text-slate-800 ">L{comp.mandated_level}</strong>
                  </span>
                  <span className="text-[11px] text-slate-500">•</span>
                  <span className="text-[11px] text-slate-500">
                    Demonstrated: <strong className="text-slate-800 ">L{comp.demonstrated_level}</strong>
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      comp.deficit_pct >= 40
                        ? 'bg-rose-100 /60 text-rose-800 '
                        : comp.deficit_pct > 0
                        ? 'bg-amber-100 /60 text-amber-800 '
                        : 'bg-emerald-100 /60 text-emerald-800 '
                    }`}
                  >
                    {comp.deficit_pct > 0 ? `${comp.deficit_pct.toFixed(0)}% Gap` : 'Proficient'}
                  </span>
                </div>
              </div>

              {/* XAI Explanation Narrative Box */}
              <div className="rounded-xl bg-slate-50 /40 p-3.5 border border-slate-200/80  text-xs text-slate-700  leading-relaxed font-normal">
                {comp.xai_explanation}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* 6. Administrative Recommendation & Continuous Learning Path */}
      <Card className="rounded-2xl border-emerald-200  bg-gradient-to-br from-emerald-50/50 to-white   shadow-md">
        <CardContent className="p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          <div className="space-y-1 max-w-2xl">
            <span className="text-xs font-bold text-emerald-700  uppercase tracking-wider">
              Official Directive & Next Steps
            </span>
            <p className="text-sm font-semibold text-slate-900  leading-relaxed">
              {dossier.recommended_action}
            </p>
            <p className="text-xs text-slate-500">
              Personalized micro-learning modules on iGOT Karmayogi have been mapped to resolve identified gaps.
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-3">
            <Link to="/recommendations">
              <Button className="bg-indigo-500 hover:bg-indigo-500 text-white font-bold shadow-md shadow-emerald-600/20">
                Proceed to Recommendations
                <ArrowRight className="h-4 w-4 ml-1.5" />
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

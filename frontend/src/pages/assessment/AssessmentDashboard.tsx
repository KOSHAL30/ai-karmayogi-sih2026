// ==============================================================================
// AI KARMAYOGI — COMPETENCY ASSESSMENT DASHBOARD
// Officer Orientation, Assigned FRAC Competencies, and Diagnostic Launchpad
// ==============================================================================

import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { AssessmentHistoryItemData, FRACCompetency } from '@/types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Compass,
  BookOpen,
  Award,
  Shield,
  Clock,
  Layers,
  ArrowRight,
  FileCheck,
  AlertCircle,
  HelpCircle,
} from 'lucide-react';

export const AssessmentDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [history, setHistory] = useState<AssessmentHistoryItemData[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await api.get<AssessmentHistoryItemData[]>('/assessment/history');
        setHistory(data);
      } catch (err) {
        console.warn('Could not load assessment history:', err);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  const handleStartAssessment = async () => {
    setStarting(true);
    try {
      navigate('/assessment/take');
    } catch (err) {
      console.error(err);
      setStarting(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* 1. Welcome & Work Role Header */}
      <div className="rounded-2xl border border-slate-200  bg-gradient-to-r from-indigo-50 via-white to-teal-50 p-8 text-slate-900 shadow-xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-teal-700 border border-teal-200">
            <Compass className="h-3.5 w-3.5 text-teal-700" />
            <span>Mission Karmayogi Competency Diagnostic</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome, {user?.full_name || 'Officer'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-600">
            {user?.designation} • {user?.department}
          </p>
          <div className="flex flex-wrap items-center gap-2 pt-1 text-xs text-teal-700">
            <span className="font-semibold text-slate-900">Designated Work Role:</span>
            <span className="px-2.5 py-0.5 rounded-md bg-emerald-800/60 border border-emerald-700/60 text-slate-900 font-medium">
              {user?.work_role || 'Desk Officer (Administration)'}
            </span>
          </div>
        </div>

        <div className="shrink-0 flex flex-col sm:flex-row gap-3">
          <Button
            size="lg"
            onClick={handleStartAssessment}
            isLoading={starting}
            className="bg-indigo-500 hover:bg-indigo-500 text-white font-bold shadow-lg shadow-emerald-600/30 px-6"
          >
            Start Diagnostic Assessment
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 2. Left 2 Columns: Assessment tealprint & Assigned FRAC Competencies */}
        <div className="lg:col-span-2 space-y-6">
          {/* Assessment Protocol Card */}
          <Card className="border-slate-200  shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Layers className="h-4 w-4 text-teal-600" />
                Adaptive Assessment Framework Protocol
              </CardTitle>
              <CardDescription className="text-xs">
                Two-Parameter Logistic (2PL) Item Response Theory calibrated to evaluate latent civil service ability.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-xs text-slate-600 ">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="rounded-xl border border-slate-200  p-3.5 bg-slate-50/50 /40 space-y-1">
                  <span className="text-[10px] font-bold text-slate-600 uppercase">Duration</span>
                  <div className="text-base font-extrabold text-slate-900  flex items-center gap-1.5">
                    <Clock className="h-4 w-4 text-teal-600" />
                    20 Minutes
                  </div>
                  <p className="text-[11px] text-slate-500">Self-timed countdown</p>
                </div>

                <div className="rounded-xl border border-slate-200  p-3.5 bg-slate-50/50 /40 space-y-1">
                  <span className="text-[10px] font-bold text-slate-600 uppercase">Item Volume</span>
                  <div className="text-base font-extrabold text-slate-900  flex items-center gap-1.5">
                    <BookOpen className="h-4 w-4 text-teal-600" />
                    10 - 15 Items
                  </div>
                  <p className="text-[11px] text-slate-500">Adaptive stopping criteria</p>
                </div>

                <div className="rounded-xl border border-slate-200  p-3.5 bg-slate-50/50 /40 space-y-1">
                  <span className="text-[10px] font-bold text-slate-600 uppercase">Ethos</span>
                  <div className="text-base font-extrabold text-teal-600  flex items-center gap-1.5">
                    <Shield className="h-4 w-4" />
                    Formative
                  </div>
                  <p className="text-[11px] text-slate-500">Non-punitive diagnostic</p>
                </div>
              </div>

              <div className="rounded-xl bg-emerald-50/60 /30 border border-emerald-200/80  p-3.5 text-xs text-emerald-900  space-y-1">
                <p className="font-bold flex items-center gap-1.5">
                  <HelpCircle className="h-4 w-4 text-teal-600 " />
                  How the Adaptive Diagnostic Works:
                </p>
                <p className="text-[11px] leading-relaxed text-emerald-800/90 ">
                  You will be presented with official file dilemmas and Office Memorandums. Correct responses adaptively introduce higher-level administrative analysis questions, while incorrect responses stabilize difficulty to pinpoint exact training needs without penalty.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Assigned FRAC Competencies Card */}
          <Card className="border-slate-200  shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Award className="h-4 w-4 text-teal-600" />
                Mandated FRAC Competency Baseline
              </CardTitle>
              <CardDescription className="text-xs">
                Statutory proficiency levels required for your designated cadre role.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="divide-y divide-slate-100  text-xs">
                <div className="py-2.5 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-900 ">Public Procurement & GFR 2017</p>
                    <p className="text-[11px] text-slate-500">Rule 149 (GeM), Rule 166 (PAC), Financial delegations</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-100 /60 text-cyan-800  border border-cyan-300">
                    Mandated: Level 4
                  </span>
                </div>

                <div className="py-2.5 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-900 ">Central Secretariat File Management & CSMOP</p>
                    <p className="text-[11px] text-slate-500">Noting, drafting, cabinet notes, e-Office audit compliance</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-100 /60 text-cyan-800  border border-cyan-300">
                    Mandated: Level 4
                  </span>
                </div>

                <div className="py-2.5 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-900 ">Ethical Governance & Conflict of Interest</p>
                    <p className="text-[11px] text-slate-500">CCS Conduct Rules 1964, recusal, zero corruption tolerance</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-100 /60 text-purple-800  border border-purple-300">
                    Mandated: Level 4
                  </span>
                </div>

                <div className="py-2.5 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-900 ">Right to Information & Statutory Appeals</p>
                    <p className="text-[11px] text-slate-500">RTI Act Section 8 exemptions, life/liberty timelines, CPIO norms</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-100 /60 text-teal-800  border border-teal-300">
                    Mandated: Level 3
                  </span>
                </div>

                <div className="py-2.5 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-900 ">Citizen-Centric Grievance Redressal</p>
                    <p className="text-[11px] text-slate-500">CPGRAMS disposal timelines, speaking orders, qualitative resolution</p>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-100 /60 text-purple-800  border border-purple-300">
                    Mandated: Level 3
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 3. Right 1 Column: Previous Assessment History */}
        <div className="space-y-6">
          <Card className="border-slate-200  shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <FileCheck className="h-4 w-4 text-teal-600" />
                Assessment Dossier History
              </CardTitle>
              <CardDescription className="text-xs">
                Your past completed diagnostic evaluations.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-3">
              {loading ? (
                <div className="py-8 text-center text-xs text-slate-600">Loading evaluation history...</div>
              ) : history.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200  p-6 text-center space-y-2">
                  <Compass className="h-8 w-8 text-slate-600  mx-auto" />
                  <p className="text-xs font-semibold text-slate-700 ">
                    No assessments taken yet
                  </p>
                  <p className="text-[11px] text-slate-600">
                    Take your baseline diagnostic assessment to generate your FRAC capability heatmap.
                  </p>
                  <Button size="sm" onClick={handleStartAssessment} className="mt-2">
                    Begin Assessment
                  </Button>
                </div>
              ) : (
                <div className="space-y-2.5">
                  {history.map((item) => (
                    <div
                      key={item.attempt_id}
                      className="rounded-xl border border-slate-200  p-3.5 space-y-2 hover:border-emerald-400 transition-colors bg-white "
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-900 ">
                          Role Diagnostic
                        </span>
                        {item.overall_score !== null && (
                          <span className="text-xs font-extrabold text-teal-600 ">
                            {item.overall_score.toFixed(1)}%
                          </span>
                        )}
                      </div>

                      <div className="flex items-center justify-between text-[11px] text-slate-500">
                        <span>{item.attempted_at ? new Date(item.attempted_at).toLocaleDateString() : 'Recent'}</span>
                        <span>{item.score_achieved} / {item.total_questions} Correct</span>
                      </div>

                      <Link to={`/assessment/result/${item.attempt_id}`}>
                        <Button variant="outline" size="sm" className="w-full text-xs mt-1">
                          View Diagnostic Dossier
                        </Button>
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

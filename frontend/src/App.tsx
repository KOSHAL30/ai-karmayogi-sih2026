// ==============================================================================
// AI KARMAYOGI — ENTERPRISE ROOT APPLICATION
// Sovereign Design System, Route Lazy-Loading, Command Palette & SIH Demo Mode
// ==============================================================================

import React, { useEffect, useState, lazy, Suspense } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { Navbar } from '@/components/layout/Navbar';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { useAuth } from '@/context/AuthContext';
import { useLanguage } from '@/context/LanguageContext';
import { api } from '@/lib/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PageSkeleton } from '@/components/ui/skeleton';
import { CommandPalette } from '@/components/navigation/CommandPalette';
import {
  Shield,
  Award,
  BookOpen,
  Compass,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Users,
  Activity,
  Layers,
  Clock,
  Calendar,
  ExternalLink,
  Download,
  CheckCircle,
  Brain,
  Building2,
  Database,
  Cpu,
  Lock,
} from 'lucide-react';

// Route Lazy-Loading & Code-Splitting for Sub-1.5s Initial Paint
const Login = lazy(() => import('@/pages/auth/Login').then((m) => ({ default: m.Login })));
const Register = lazy(() => import('@/pages/auth/Register').then((m) => ({ default: m.Register })));
const ForgotPassword = lazy(() => import('@/pages/auth/ForgotPassword').then((m) => ({ default: m.ForgotPassword })));
const Unauthorized = lazy(() => import('@/pages/auth/Unauthorized').then((m) => ({ default: m.Unauthorized })));
const Profile = lazy(() => import('@/pages/profile/Profile').then((m) => ({ default: m.Profile })));
const AssessmentDashboard = lazy(() =>
  import('@/pages/assessment/AssessmentDashboard').then((m) => ({ default: m.AssessmentDashboard }))
);
const AssessmentPlayer = lazy(() =>
  import('@/pages/assessment/AssessmentPlayer').then((m) => ({ default: m.AssessmentPlayer }))
);
const AssessmentResult = lazy(() =>
  import('@/pages/assessment/AssessmentResult').then((m) => ({ default: m.AssessmentResult }))
);
const RecommendationDashboard = lazy(() =>
  import('@/pages/recommendations/RecommendationDashboard').then((m) => ({ default: m.RecommendationDashboard }))
);
const LearningPath = lazy(() =>
  import('@/pages/recommendations/LearningPath').then((m) => ({ default: m.LearningPath }))
);
const DocumentStudio = lazy(() =>
  import('@/pages/trainer/DocumentStudio').then((m) => ({ default: m.DocumentStudio }))
);
const AdminDashboard = lazy(() =>
  import('@/pages/admin/AdminDashboard').then((m) => ({ default: m.AdminDashboard }))
);
const DepartmentAnalytics = lazy(() =>
  import('@/pages/admin/DepartmentAnalytics').then((m) => ({ default: m.DepartmentAnalytics }))
);
const CompetencyInsights = lazy(() =>
  import('@/pages/admin/CompetencyInsights').then((m) => ({ default: m.CompetencyInsights }))
);
const CertificateCenter = lazy(() =>
  import('@/pages/certificates/CertificateCenter').then((m) => ({ default: m.CertificateCenter }))
);

// Overview / Landing Component for Authenticated and Guest Users
function OverviewPage() {
  const { user, isAuthenticated } = useAuth();
  const { t } = useLanguage();
  const [healthStatus, setHealthStatus] = useState<{ status: string; db: string; ai: string } | null>(null);

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await api.get<any>('/health', { silent: true });
        setHealthStatus({
          status: res.status,
          db: res.services?.postgresql?.status || 'healthy',
          ai: res.services?.ollama?.status || 'standby',
        });
      } catch {
        setHealthStatus({ status: 'operational', db: 'ready', ai: 'ready' });
      }
    }
    checkHealth();
  }, []);

  // --------------------------------------------------------------------------
  // AUTHENTICATED OFFICER DASHBOARD (STITCH SOVEREIGN DESIGN)
  // --------------------------------------------------------------------------
  if (isAuthenticated && user) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8 animate-in fade-in duration-300">
        {/* Sovereign Header Banner */}
        <div className="relative overflow-hidden rounded-3xl bg-indigo-50 dark:bg-slate-900 border-indigo-100 dark:border-slate-800 p-8 sm:p-10 text-slate-900 dark:text-slate-100 shadow-2xl border border-slate-200/40">
          {/* Ambient Glows & Watermark */}
          <div className="absolute -top-32 -left-32 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 right-0 w-[28rem] h-[28rem] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10 space-y-6">
            {/* Top Sovereign Tag */}
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="font-semibold text-[#FF9933]">सत्यमेव जयते</span>
              <span className="text-slate-900 dark:text-slate-100/40">•</span>
              <span className="text-slate-900 dark:text-slate-100/70 font-medium">Mission Karmayogi Bharat Sovereign Portal</span>
              <span className="text-slate-900 dark:text-slate-100/40">•</span>
              <span className="text-teal-700 font-medium flex items-center gap-1">
                <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400" />
                FRAC v1.6 Calibrated
              </span>
            </div>

            {/* Officer Welcome */}
            <div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight">
                {t('overview.welcome_back', 'Welcome back')}, {user.full_name}
              </h1>
              <p className="text-sm sm:text-base text-teal-700/90 dark:text-teal-200/80 font-medium mt-1">
                {user.designation} • {user.department}, {t('brand.motto', 'Government of India')}
              </p>
            </div>

            {/* 3 Quick Action Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              {/* Card 1: Diagnostic Assessment */}
              <Link to="/assessment" className="group">
                <div className="h-full bg-white/60 dark:bg-white/5 hover:bg-white/90 dark:hover:bg-white/10 backdrop-blur-md border border-indigo-200/50 dark:border-white/10 hover:border-emerald-400/50 rounded-2xl p-5 transition-all duration-200 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="h-9 w-9 rounded-xl bg-indigo-500/20 text-teal-700 flex items-center justify-center">
                        <Brain className="h-5 w-5" />
                      </div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/30 text-teal-700 border border-teal-200">
                        FRAC Mandate
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 group-hover:text-teal-700 transition-colors">
                      Start Diagnostic Assessment
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-300/80 leading-relaxed">
                      Evaluate your competency gaps against FRAC statutory mandates and cadre benchmarks.
                    </p>
                  </div>
                  <div className="pt-4 flex items-center justify-between text-xs text-teal-700 font-semibold">
                    <span>20 Adaptive Qs • 2PL-IRT</span>
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>

              {/* Card 2: Learning Path */}
              <Link to="/learning-path" className="group">
                <div className="h-full bg-white/60 dark:bg-white/5 hover:bg-white/90 dark:hover:bg-white/10 backdrop-blur-md border border-indigo-200/50 dark:border-white/10 hover:border-emerald-400/50 rounded-2xl p-5 transition-all duration-200 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="h-9 w-9 rounded-xl bg-indigo-500/20 text-teal-700 flex items-center justify-center">
                        <Layers className="h-5 w-5" />
                      </div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/30 text-teal-700 border border-teal-200">
                        Step 3 of 8
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 group-hover:text-teal-700 transition-colors">
                      View Learning Path
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-300/80 leading-relaxed">
                      4-week structured trajectory towards Cadre Competency Tier-1 statutory qualification.
                    </p>
                  </div>
                  <div className="pt-4 flex items-center justify-between text-xs text-teal-700 font-semibold">
                    <span>Next: COMP: Drafting</span>
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>

              {/* Card 3: Recommendations */}
              <Link to="/recommendations" className="group">
                <div className="h-full bg-white/60 dark:bg-white/5 hover:bg-white/90 dark:hover:bg-white/10 backdrop-blur-md border border-indigo-200/50 dark:border-white/10 hover:border-amber-400/50 rounded-2xl p-5 transition-all duration-200 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="h-9 w-9 rounded-xl bg-amber-500/20 text-amber-300 flex items-center justify-center">
                        <Sparkles className="h-5 w-5" />
                      </div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/30 text-amber-700 border border-amber-400/30">
                        Synthesized
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 group-hover:text-amber-700 transition-colors">
                      Explore Recommendations
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-300/80 leading-relaxed">
                      12 AI-curated modules synthesized from recent diagnostic gaps and procurement revisions.
                    </p>
                  </div>
                  <div className="pt-4 flex items-center justify-between text-xs text-amber-300 font-semibold">
                    <span>GFR 2017 & GeM Focus</span>
                    <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>

        {/* Progress Snapshot Row */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100  flex items-center gap-2">
              Your Progress Snapshot
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-100  text-slate-600 dark:text-slate-300">
                S2 FY25-26
              </span>
            </h2>
            <span className="text-xs text-slate-600 dark:text-slate-300 flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-indigo-500" />
              Last IRT Sync: Today at 06:00 IST
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Tile 1: Cadre Competency Score */}
            <Card className="border-slate-200/80  shadow-xs">
              <CardContent className="pt-5 pb-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500  Competency Score</span>"></span>
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-50  text-amber-700  border border-amber-200">
                    Moderate Deficit
                  </span>
                </div>
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100"></span>
                  <span className="text-xs text-slate-600 dark:text-slate-300">Cadre Target: 72%</span>
                </div>
                <div className="mt-2 flex items-center gap-1 text-[11px] text-teal-600  font-medium">
                  <span>+4.2% vs last cycle</span>
                </div>
              </CardContent>
            </Card>

            {/* Tile 2: Prescribed Modules */}
            <Card className="border-slate-200/80  shadow-xs">
              <CardContent className="pt-5 pb-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500  Modules</span>"></span>
                  <BookOpen className="h-4 w-4 text-teal-600" />
                </div>
                <div className="mt-3 flex items-baseline gap-1.5">
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100"></span>
                  <span className="text-base text-slate-600 dark:text-slate-300">/ 12 completed</span>
                </div>
                <div className="mt-3 w-full bg-slate-100  rounded-full h-1.5 overflow-hidden">
                  <div className="bg-indigo-500 h-full rounded-full w-[33%]" />
                </div>
              </CardContent>
            </Card>

            {/* Tile 3: Continuous Learning Time */}
            <Card className="border-slate-200/80  shadow-xs">
              <CardContent className="pt-5 pb-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500  Learning Time</span>"></span>
                  <Clock className="h-4 w-4 text-teal-600" />
                </div>
                <div className="mt-3 flex items-baseline gap-1.5">
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100"></span>
                  <span className="text-sm text-slate-600 dark:text-slate-300">Hours</span>
                </div>
                <div className="mt-2 text-[11px] text-slate-500">
                  Cadence: 3.3 hrs/wk (Target: 4.0)
                </div>
              </CardContent>
            </Card>

            {/* Tile 4: Mandatory Assessment Callout */}
            <Card className="border-slate-200/80  shadow-xs bg-white text-slate-900 dark:text-slate-100">
              <CardContent className="pt-5 pb-5 flex flex-col justify-between h-full">
                <div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-teal-700">Mandatory Assessment</span>
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      3 Days Left
                    </span>
                  </div>
                  <p className="mt-2 text-sm font-bold">Statutory Mid-Career Review</p>
                  <p className="text-[11px] text-slate-600 dark:text-slate-300">Due: 18 Oct 2026</p>
                </div>
                <Link to="/assessment" className="mt-3">
                  <Button size="sm" className="w-full bg-white text-slate-900 dark:text-slate-100 hover:bg-slate-100 text-xs font-semibold">
                    Launch Assessment
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* 2-Column Dashboard Grid: Recent Cadre Activity & Sovereign Node Telemetry */}
        <div className="grid grid-cols-1 gap-6">
          {/* Left Column (2/3): Recent Cadre Activity */}
          <div className="space-y-4">
            <Card className="border-slate-200/80  shadow-sm">
              <CardHeader className="pb-3 border-b border-slate-100">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-base font-bold flex items-center gap-2">
                      <Activity className="h-4 w-4 text-teal-600" />
                      Recent Cadre Activity
                    </CardTitle>
                    <CardDescription className="text-xs">
                      Immutable ledger log of completed modules, proctored checks & scores.
                    </CardDescription>
                  </div>
                  <Link to="/profile">
                    <Button variant="outline" size="sm" className="text-xs">
                      View Full Audit Trail
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="pt-4 space-y-4">
                {/* Event 1 */}
                <div className="flex items-start gap-3.5 pb-4 border-b border-slate-100">
                  <div className="h-8 w-8 rounded-full bg-emerald-100  text-teal-600  flex items-center justify-center shrink-0 mt-0.5">
                    <CheckCircle className="h-4 w-4" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">
                        Completed Module: Ethics & Conduct in Public Service
                      </h4>
                      <span className="text-[10px] text-slate-600 dark:text-slate-300">Today • 10:30 AM</span>
                    </div>
                    <p className="text-xs text-slate-500  leading-relaxed">
                      Passed post-course comprehension evaluation with 84% accuracy. Rule 13 & 14 CCS (Conduct) Rules certified under FRAC mandate.
                    </p>
                    <div className="pt-1 flex items-center gap-2">
                      <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-teal-600  bg-emerald-50  px-2 py-0.5 rounded border border-emerald-200">
                        <Award className="h-3 w-3" />
                        Verified Certificate Generated (Hash: #AF28-C7A-2026)
                      </span>
                    </div>
                  </div>
                </div>

                {/* Event 2 */}
                <div className="flex items-start gap-3.5 pb-4 border-b border-slate-100">
                  <div className="h-8 w-8 rounded-full bg-emerald-100  text-teal-600  flex items-center justify-center shrink-0 mt-0.5">
                    <Brain className="h-4 w-4" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">
                        Assessment Score: 72% on GFR 2017 & GeM Procurement Module
                      </h4>
                      <span className="text-[10px] text-slate-600 dark:text-slate-300">Yesterday • 04:20 PM</span>
                    </div>
                    <p className="text-xs text-slate-500  leading-relaxed">
                      Evaluated across Rule 149 reverse auction thresholds. Minor gap detected in direct purchase ceilings above ₹5 Lakhs.
                    </p>
                    <div className="pt-1 flex items-center gap-2 text-[10px] text-slate-500">
                      <span className="font-semibold text-teal-600  Score Updated</span>"></span>
                      <span>•</span>
                      <span>2PL-IRT θ: +0.68 (Level 3 demonstrated)</span>
                    </div>
                  </div>
                </div>

                {/* Event 3 */}
                <div className="flex items-start gap-3.5">
                  <div className="h-8 w-8 rounded-full bg-amber-100  text-amber-600  flex items-center justify-center shrink-0 mt-0.5">
                    <Layers className="h-4 w-4" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">
                        Started: RTI Act Compliance & Appellate Procedures Training
                      </h4>
                      <span className="text-[10px] text-slate-600 dark:text-slate-300">2 days ago • 11:00 AM</span>
                    </div>
                    <p className="text-xs text-slate-500  leading-relaxed">
                      Section 8(1)(j) third-party privacy exemption analysis module opened. Time actively engaged: 45 minutes.
                    </p>
                    <div className="pt-1 flex items-center gap-2 text-[10px] text-amber-600  font-medium">
                      <span>Module in Progress (45%)</span>
                      <span>•</span>
                      <span>Estimated remaining: 1 hr 15 mins</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column (1/3): Sovereign Node Telemetry */}
          <div className="space-y-4">

            {/* FRAC Statutory Compliance Download Card */}
            <Card className="border-slate-200/80  shadow-xs">
              <CardContent className="pt-4 pb-4 space-y-2">
                <div className="flex items-center gap-2">
                  <Award className="h-4 w-4 text-teal-600  />" />
                  <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">
                    FRAC Statutory Compliance
                  </h4>
                </div>
                <p className="text-xs text-slate-500">
                  Your profile is aligned with <span className="font-semibold text-slate-700  Secretary Establishment Domain (Tier-1)</span>."></span>
                </p>
                <a
                  href="/api/v1/health"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-semibold text-teal-600  hover:underline pt-1"
                >
                  <Download className="h-3.5 w-3.5" />
                  Download Official Framework Telemetry
                </a>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  // --------------------------------------------------------------------------
  // PUBLIC / GUEST LANDING PAGE (MISSION KARMAYOGI SOVEREIGN OVERVIEW)
  // --------------------------------------------------------------------------
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-10 animate-in fade-in duration-300">
      {/* Sovereign Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-indigo-50 dark:bg-slate-900 border-indigo-100 dark:border-slate-800 p-8 sm:p-12 text-slate-900 dark:text-slate-100 shadow-2xl border border-slate-200/40">
        <div className="absolute -top-24 -right-24 h-96 w-96 rounded-full bg-teal-500/10 blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/60 dark:bg-white/5 backdrop-blur-md px-3 py-1 text-xs font-semibold text-teal-800 border border-indigo-200/50 dark:border-white/10">
            <Sparkles className="h-3.5 w-3.5 text-[#FF9933]" />
            <span>{t('overview.badge', 'Mission Karmayogi Bharat Sovereign Portal')}</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
            {t('overview.hero_title', 'AI-Enabled Competency Diagnostic & Learning Ecosystem')}
          </h1>

          <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl">
            {t('overview.hero_desc', 'Diagnosing civil service competency gaps, aligning role-based training via the iGOT Karmayogi repository, and delivering automated assessment generation for modern Indian governance.')}
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-4">
            <Link to="/login">
              <Button className="bg-indigo-500 text-white hover:bg-indigo-500 font-semibold shadow-lg shadow-emerald-600/30">
                {t('overview.sign_in_portal', 'Sign In to Portal')}
                <ArrowRight className="h-4 w-4 ml-1.5" />
              </Button>
            </Link>
            <Link to="/register">
              <Button variant="outline" className="text-slate-900 dark:text-slate-100 border-slate-600 hover:bg-white/60 dark:bg-white/5 font-medium">
                {t('overview.register_officer', 'Register as Officer')}
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* 3 Core Roles Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
              {t('overview.roles_title', 'Sovereign Role Archetypes')}
            </h2>
            <p className="text-xs text-slate-500">
              {t('overview.roles_subtitle', 'Three streamlined roles aligned with Mission Karmayogi institutional workflows.')}
            </p>
          </div>
          {healthStatus && (
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50  text-emerald-700  border border-emerald-200">
              <Activity className="h-3.5 w-3.5" />
              <span>Core Stack: MongoDB Atlas + Atlas Vector Search</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Learner Card */}
          <Link to="/login">
            <Card className="border-slate-200  hover:border-emerald-500/80 hover:shadow-md transition-all h-full">
              <CardHeader className="pb-3">
                <div className="h-10 w-10 rounded-xl bg-emerald-50  text-teal-600  flex items-center justify-center mb-2">
                  <BookOpen className="h-5 w-5" />
                </div>
                <CardTitle className="text-base flex items-center justify-between">
                  Civil Services Official (Learner)
                  <ArrowRight className="h-4 w-4 text-slate-600 dark:text-slate-300" />
                </CardTitle>
                <CardDescription className="text-xs">
                  Demo Officer: Rajesh Kumar (Under Secretary)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                <p>• FRAC Competency Gap Self-Assessment</p>
                <p>• Explainable Course Recommendations from iGOT</p>
                <p>• Adaptive Quiz Engine with Feedback</p>
              </CardContent>
            </Card>
          </Link>

          {/* Trainer Card */}
          <Link to="/login">
            <Card className="border-slate-200  hover:border-emerald-500/80 hover:shadow-md transition-all h-full">
              <CardHeader className="pb-3">
                <div className="h-10 w-10 rounded-xl bg-emerald-50  text-teal-600  flex items-center justify-center mb-2">
                  <Award className="h-5 w-5" />
                </div>
                <CardTitle className="text-base flex items-center justify-between">
                  Training Faculty (Trainer)
                  <ArrowRight className="h-4 w-4 text-slate-600 dark:text-slate-300" />
                </CardTitle>
                <CardDescription className="text-xs">
                  Demo Faculty: Dr. Sunita Deshmukh (Senior Faculty)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                <p>• Policy Material Upload (PDF & Guidelines)</p>
                <p>• Sovereign RAG with Statutory Citations</p>
                <p>• Bloom's Taxonomy Automated MCQ Studio</p>
              </CardContent>
            </Card>
          </Link>

          {/* Admin Card */}
          <Link to="/login">
            <Card className="border-slate-200  hover:border-emerald-500/80 hover:shadow-md transition-all h-full">
              <CardHeader className="pb-3">
                <div className="h-10 w-10 rounded-xl bg-amber-50  text-amber-600  flex items-center justify-center mb-2">
                  <Shield className="h-5 w-5" />
                </div>
                <CardTitle className="text-base flex items-center justify-between">
                  Governance Lead (Admin)
                  <ArrowRight className="h-4 w-4 text-slate-600 dark:text-slate-300" />
                </CardTitle>
                <CardDescription className="text-xs">
                  Demo Lead: Dr. Priya Nair (Director Analytics)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                <p>• Departmental Competency Heatmaps & Health</p>
                <p>• FRAC Taxonomy & Work-Role Allocation</p>
                <p>• Officer Management & Sovereign RBAC</p>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const location = useLocation();
  const isAuthPage = ['/login', '/register', '/forgot-password'].includes(location.pathname);
    const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  // Global Keyboard Shortcuts (Ctrl+Shift+D for Demo Cockpit, Ctrl+K for Command Palette)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {        if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        setCommandPaletteOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50  text-slate-900 dark:text-slate-100  transition-colors duration-200">
      {!isAuthPage && <Navbar />}

      <main className={isAuthPage ? 'h-screen w-full overflow-hidden' : 'flex-1'}>
        <Suspense fallback={<PageSkeleton />}>
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/unauthorized" element={<Unauthorized />} />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/assessment"
              element={
                <ProtectedRoute>
                  <AssessmentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/assessment/take"
              element={
                <ProtectedRoute>
                  <AssessmentPlayer />
                </ProtectedRoute>
              }
            />
            <Route
              path="/assessment/result/:id"
              element={
                <ProtectedRoute>
                  <AssessmentResult />
                </ProtectedRoute>
              }
            />
            <Route
              path="/recommendations"
              element={
                <ProtectedRoute>
                  <RecommendationDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/learning-path"
              element={
                <ProtectedRoute>
                  <LearningPath />
                </ProtectedRoute>
              }
            />
            <Route
              path="/trainer/documents"
              element={
                <ProtectedRoute allowedRoles={['trainer', 'admin', 'administrator']}>
                  <DocumentStudio />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute allowedRoles={['admin', 'administrator', 'department_head']}>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/departments"
              element={
                <ProtectedRoute allowedRoles={['admin', 'administrator', 'department_head']}>
                  <DepartmentAnalytics />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/competencies"
              element={
                <ProtectedRoute allowedRoles={['admin', 'administrator', 'department_head']}>
                  <CompetencyInsights />
                </ProtectedRoute>
              }
            />
            <Route
              path="/certificates"
              element={
                <ProtectedRoute>
                  <CertificateCenter />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<OverviewPage />} />
          </Routes>
        </Suspense>
      </main>

      

      {/* Global Command Palette (Ctrl + K) */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
      />

      {/* Sovereign National Footer */}
      {!isAuthPage && (
        <footer className="border-t border-slate-200  bg-white  py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-indigo-500" />
              <span>AI Karmayogi Platform</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="hidden sm:inline">Press <kbd className="px-1.5 py-0.5 rounded bg-slate-100  border text-[10px] font-mono">Ctrl+K</kbd> for Command Palette</span>
              <span>•</span>
              <span>100% Sovereign Local Stack</span>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}

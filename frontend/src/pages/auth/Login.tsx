// ==============================================================================
// AI KARMAYOGI — SOVEREIGN LOGIN PORTAL (STITCH SPLIT-HERO DESIGN)
// Pixel-Perfect Split-Screen Layout: 60% Sovereign Hero + 40% Glassmorphic Auth
// ==============================================================================

import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { useLanguage } from '@/context/LanguageContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { LanguageSelector } from '@/components/layout/LanguageSelector';
import {
  Compass,
  ShieldCheck,
  AlertCircle,
  Sparkles,
  Mail,
  Lock,
  Eye,
  EyeOff,
  Users,
  Building2,
  Brain,
  Sun,
  Moon,
  ArrowRight,
  Globe,
  HelpCircle,
} from 'lucide-react';

export const Login: React.FC = () => {
  const { login, switchPersona, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // If already authenticated, redirect
  React.useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email, password);
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (role: any) => {
    setError(null);
    setLoading(true);
    try {
      await switchPersona(role);
      navigate('/', { replace: true });
    } catch (err: any) {
      setError(err.message || 'Demo authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen w-full flex flex-col overflow-hidden bg-slate-50  select-none">
      {/* 1. Top Sovereign Indian Tricolor Accent Ribbon (4px) */}
      <div className="w-full h-1 bg-indigo-600 shrink-0 z-50 shadow-xs" />

      {/* 2. Main Edge-to-Edge Split Layout Container */}
      <div className="flex-1 w-full h-[calc(100vh-4px)] flex flex-col lg:flex-row overflow-hidden">
        {/* =========================================================================
            LEFT HERO PANEL (60% Desktop) — SOVEREIGN IDENTITY & STATS
            ========================================================================= */}
        <div className="relative hidden lg:flex lg:w-[58%] xl:w-[60%] h-full bg-indigo-50 border-indigo-100 text-slate-900 p-10 xl:p-14 flex-col justify-between overflow-hidden shadow-2xl z-10 border-r border-slate-200/40">
          {/* Ambient Glows */}
          <div className="absolute -top-32 -left-32 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 right-0 w-[30rem] h-[30rem] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          {/* Ashoka Chakra 24-Spoke Watermark (Clean SVG with subtle 7% opacity) */}
          <div className="absolute right-[-8%] top-[18%] w-[540px] h-[540px] pointer-events-none opacity-[0.06] text-slate-900 select-none">
            <svg className="w-full h-full animate-[spin_180s_linear_infinite]" fill="none" stroke="currentColor" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="92" strokeWidth="2.5" />
              <circle cx="100" cy="100" r="22" strokeWidth="2.5" />
              <circle cx="100" cy="100" fill="currentColor" r="6" />
              {/* 24 Radial Spokes */}
              {Array.from({ length: 24 }).map((_, i) => {
                const angle = (i * 15 * Math.PI) / 180;
                return (
                  <line
                    key={i}
                    x1={100 + 22 * Math.cos(angle)}
                    y1={100 + 22 * Math.sin(angle)}
                    x2={100 + 92 * Math.cos(angle)}
                    y2={100 + 92 * Math.sin(angle)}
                    strokeWidth="1.5"
                  />
                );
              })}
            </svg>
          </div>

          {/* Top Sovereign Badge Cluster */}
          <div className="relative z-10 space-y-3">
            <div className="flex items-center gap-3">
              <div className="px-3 py-1 rounded bg-white/10 backdrop-blur-md border border-white/15 text-[11px] font-semibold tracking-wider uppercase text-[#FF9933] flex items-center gap-1.5 shadow-xs">
                <span>{t('brand.motto', 'सत्यमेव जयते • Government of India')}</span>
              </div>
              <span className="text-xs text-slate-600">|</span>
              <span className="text-xs text-slate-600 font-medium">
                {t('brand.ministry', 'Ministry of Personnel, Public Grievances and Pensions')}
              </span>
            </div>
            <div className="inline-flex items-center gap-2 text-xs font-semibold text-teal-700 bg-emerald-950/40 border border-emerald-500/30 px-3 py-1 rounded-full backdrop-blur-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              {t('brand.portal_badge', 'Mission Karmayogi Bharat Sovereign Portal')}
            </div>
          </div>

          {/* Central Hero Statement */}
          <div className="relative z-10 max-w-2xl my-auto space-y-5 pt-4">
            <div className="space-y-2">
              <h1 className="text-4xl xl:text-5xl font-extrabold tracking-tight leading-[1.15] text-slate-900">
                {t('brand.name', 'AI Karmayogi')}
              </h1>
              <p className="text-sm xl:text-base font-semibold text-[#FF9933] uppercase tracking-wider">
                {t('brand.sub', 'National Programme for Civil Services Capacity Building')}
              </p>
            </div>
            <p className="text-slate-600/90 text-sm xl:text-base leading-relaxed max-w-xl">
              {t('brand.hero_desc', 'Accelerating competency diagnostic frameworks, personalized learning pathways, and adaptive civil service readiness powered by sovereign AI intelligence.')}
            </p>

            {/* 3 Glassmorphic Key Metrics Bento Cards */}
            <div className="grid grid-cols-3 gap-3.5 pt-3">
              {/* Metric 1 */}
              <div className="bg-white/[0.06] backdrop-blur-md border border-white/10 rounded-xl p-4 transition-all duration-200 hover:bg-white/[0.09] hover:border-white/20">
                <div className="flex items-center gap-1.5 text-amber-300 mb-1">
                  <Users className="h-4 w-4" />
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-600 font-mono">
                    {t('brand.reach', 'Reach')}
                  </span>
                </div>
                <div className="text-2xl xl:text-3xl font-extrabold text-slate-900 tracking-tight">2M+</div>
                <div className="text-[11px] text-slate-600 font-normal leading-tight mt-0.5">
                  {t('brand.officers_assessed', 'Officers Onboarded & Assessed')}
                </div>
              </div>

              {/* Metric 2 */}
              <div className="bg-white/[0.06] backdrop-blur-md border border-white/10 rounded-xl p-4 transition-all duration-200 hover:bg-white/[0.09] hover:border-white/20">
                <div className="flex items-center gap-1.5 text-teal-700 mb-1">
                  <Building2 className="h-4 w-4" />
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-600 font-mono">
                    {t('brand.federal', 'Federal')}
                  </span>
                </div>
                <div className="text-2xl xl:text-3xl font-extrabold text-slate-900 tracking-tight">93</div>
                <div className="text-[11px] text-slate-600 font-normal leading-tight mt-0.5">
                  {t('brand.ministries_count', 'Ministries & State Departments')}
                </div>
              </div>

              {/* Metric 3 */}
              <div className="bg-white/[0.06] backdrop-blur-md border border-white/10 rounded-xl p-4 transition-all duration-200 hover:bg-white/[0.09] hover:border-white/20">
                <div className="flex items-center gap-1.5 text-sky-300 mb-1">
                  <Brain className="h-4 w-4" />
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-600 font-mono">
                    {t('brand.models', 'Models')}
                  </span>
                </div>
                <div className="text-2xl xl:text-3xl font-extrabold text-slate-900 tracking-tight">45+</div>
                <div className="text-[11px] text-slate-600 font-normal leading-tight mt-0.5">
                  {t('brand.frameworks_count', 'Core Competency Frameworks')}
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Sovereignty & Security Notice */}
          <div className="relative z-10 pt-4 border-t border-white/10 flex items-center justify-between text-xs text-slate-600">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-teal-700" />
              <span className="font-medium text-slate-600">
                {t('login.nic_powered', 'Powered by National Informatics Centre (NIC) Sovereign Compute Cluster')}
              </span>
            </div>
            <div className="flex items-center gap-1.5 text-[11px] text-slate-600 font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              <span>{t('login.tier_iv', 'TIER-IV DATA CENTRE')}</span>
            </div>
          </div>
        </div>

        {/* =========================================================================
            RIGHT AUTH PANEL (40% Desktop, 100% Mobile) — SIGN IN CARD
            ========================================================================= */}
        <div className="w-full lg:w-[42%] xl:w-[40%] h-full bg-slate-50  flex flex-col justify-between overflow-y-auto p-6 sm:p-8 xl:p-12 relative">
          {/* Top Bar inside Auth Panel */}
          <div className="w-full flex items-center justify-between text-xs text-slate-500 pb-2">
            <div className="flex items-center gap-1.5 font-semibold text-slate-700 ">
              <span className="text-[11px] text-slate-600">{t('login.portal_tag', 'Civil Services Portal')}</span>
            </div>
            <div className="flex items-center gap-2 sm:gap-3">
              {/* Language Selection near Theme Toggle */}
              <LanguageSelector variant="compact" />

              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                aria-label="Toggle theme"
                className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900  hover:bg-slate-200/60  transition-colors"
              >
                {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>
              <Link
                to="/"
                className="text-xs font-semibold text-teal-600  hover:underline flex items-center gap-1 ml-1"
              >
                <span>{t('nav.overview', 'Overview')}</span>
                <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
          </div>

          {/* Centered Authentication Form */}
          <div className="w-full max-w-md mx-auto my-auto py-4 space-y-6">
            {/* Compass Emblem & Title */}
            <div className="text-center space-y-2">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-lg shadow-indigo-500/25">
                <Compass className="h-7 w-7" />
              </div>
              <h2 className="text-2xl font-extrabold tracking-tight text-slate-900 ">
                {t('login.title', 'Sign in to your account')}
              </h2>
              <p className="text-xs text-slate-500 ">
                {t('login.subtitle', 'Enter your official government email to access competency diagnostics')}
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-50 /40 text-rose-700  border border-rose-200  text-xs font-medium">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <Label htmlFor="email" required>
                    {t('login.email_label', 'Official Government Email')}
                  </Label>
                  <span className="text-[10px] font-medium text-emerald-700  bg-emerald-50 /50 border border-emerald-200/60  px-1.5 py-0.5 rounded">
                    {t('login.email_verified', '.gov.in / .nic.in verified')}
                  </span>
                </div>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-600" />
                  <Input
                    id="email"
                    type="email"
                    placeholder={t('login.email_placeholder', 'rajesh.kumar@gov.in')}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="pl-10 text-sm h-11 rounded-xl bg-white  border-slate-300 "
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password" required>
                    {t('login.password_label', 'Password')}
                  </Label>
                  <Link
                    to="/forgot-password"
                    className="text-xs font-medium text-teal-600  hover:underline"
                  >
                    {t('login.forgot_password', 'Forgot password?')}
                  </Link>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-600" />
                  <Input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder={t('login.password_placeholder', '••••••••••••')}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="pl-10 pr-10 text-sm h-11 rounded-xl bg-white  border-slate-300 "
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-600  transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full h-11 rounded-xl bg-[#F97316] hover:bg-[#EA580C] text-slate-900 shadow-md font-semibold text-sm transition-all"
                isLoading={loading}
              >
                {t('login.submit_btn', 'Sign In to Karmayogi →')}
              </Button>
            </form>

            {/* Registration Link */}
            <div className="text-center text-xs text-slate-500 ">
              {t('login.no_account', "Don't have an official account?")}{' '}
              <Link to="/register" className="font-semibold text-teal-600  hover:underline">
                {t('login.register_officer', 'Register as Officer')}
              </Link>
            </div>

            {/* SIH 2026 Evaluation Quick Logins */}
            <div className="w-full rounded-2xl bg-white  p-4 border border-slate-200  shadow-xs space-y-2.5">
              <div className="flex items-center justify-between text-[11px] font-bold text-slate-600 ">
                <span className="flex items-center gap-1.5">
                  <Sparkles className="h-3.5 w-3.5 text-teal-600" />
                  {t('login.sih_quick_logins', 'SIH 2026 Quick Logins:')}
                </span>
                <span className="text-[10px] text-slate-600 font-normal">{t('login.one_click', '1-Click Auth')}</span>
              </div>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleQuickDemo('learner')}
                  disabled={loading}
                  className="group px-3 py-2 text-xs font-semibold rounded-xl bg-slate-50 /60 border border-emerald-200  text-emerald-700  hover:border-emerald-500 hover:bg-emerald-50  transition-all duration-200 disabled:opacity-50 text-center"
                >
                  <span className="block text-[10px] text-slate-600  mb-0.5">
                    {t('login.civil_officer', 'Civil Officer')}
                  </span>
                  {t('login.learner', 'Learner')}
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickDemo('trainer')}
                  disabled={loading}
                  className="group px-3 py-2 text-xs font-semibold rounded-xl bg-slate-50 /60 border border-emerald-200  text-emerald-700  hover:border-emerald-500 hover:bg-emerald-50  transition-all duration-200 disabled:opacity-50 text-center"
                >
                  <span className="block text-[10px] text-slate-600  mb-0.5">
                    {t('login.faculty', 'Faculty')}
                  </span>
                  {t('login.trainer', 'Trainer')}
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickDemo('admin')}
                  disabled={loading}
                  className="group px-3 py-2 text-xs font-semibold rounded-xl bg-slate-50 /60 border border-amber-200  text-amber-700  hover:border-amber-500 hover:bg-amber-50  transition-all duration-200 disabled:opacity-50 text-center"
                >
                  <span className="block text-[10px] text-slate-600  mb-0.5">
                    {t('login.director', 'Director')}
                  </span>
                  {t('login.admin', 'Admin')}
                </button>
              </div>
            </div>
          </div>

          {/* Footer Security Badge */}
          <div className="pt-2 text-center text-[11px] text-slate-600 flex items-center justify-center gap-2">
            <ShieldCheck className="h-3.5 w-3.5 text-teal-600" />
            <span>{t('login.sovereign_footer', 'Sovereign Local Self-Hosted Infrastructure • MeitY & Digital India Certified')}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

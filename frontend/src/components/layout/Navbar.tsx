// ==============================================================================
// AI KARMAYOGI — ENTERPRISE NAVIGATION BAR
// Sovereign Government of India Design System (Linear / Apple / Slate + emerald)
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth, DEMO_PERSONAS } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { UserRole, NotificationListData } from '@/types';
import { api } from '@/lib/api';
import { NotificationCenter } from '@/components/notifications/NotificationCenter';
import { LanguageSelector } from '@/components/layout/LanguageSelector';
import { useLanguage } from '@/context/LanguageContext';
import {
  Sun,
  Moon,
  User as UserIcon,
  LogOut,
  Shield,
  BookOpen,
  Award,
  Sparkles,
  ChevronDown,
  Compass,
  Bell,
  BarChart3,
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout, switchPersona } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [demoModalOpen, setDemoModalOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (isAuthenticated) {
      api.get<NotificationListData>('/notifications')
        .then((res) => setUnreadCount(res.unread_count || 0))
        .catch(() => {});
    }
  }, [isAuthenticated]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'admin':
      case 'administrator':
        return {
          label: 'Admin',
          classes: 'bg-amber-100 /40 text-amber-800  border-amber-200 ',
        };
      case 'trainer':
        return {
          label: 'Trainer',
          classes: 'bg-emerald-100 /40 text-emerald-800  border-emerald-200 ',
        };
      case 'learner':
      default:
        return {
          label: 'Learner',
          classes: 'bg-emerald-100 /40 text-emerald-800  border-emerald-200 ',
        };
    }
  };

  return (
    <>
      <header className="sticky top-0 z-40 w-full border-b border-slate-200  bg-white/90 /90 backdrop-blur-md">
        {/* Tricolor sovereignty banner */}
        <div className="h-1 w-full bg-indigo-600    shadow-sm" />

        <div className="mx-auto flex h-16 w-full items-center justify-between px-4 sm:px-6">
          {/* Left Brand Identity */}
          <div className="flex items-center gap-2 lg:gap-4 min-w-0 flex-1">
            <Link to="/" className="flex items-center gap-3 group shrink-0">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-lg shadow-indigo-500/25 group-hover:shadow-indigo-500/40 transition-all duration-200">
                <Compass className="h-5 w-5" />
              </div>
              <div className="flex flex-col shrink-0">
                <span className="text-base font-extrabold tracking-tight text-slate-900 dark:text-slate-100  flex items-center gap-1.5 whitespace-nowrap">
                  AI Karmayogi
                  <span className="rounded-md bg-emerald-50  px-1.5 py-0.5 text-[10px] font-semibold text-emerald-700  border border-emerald-200/60 ">
                    FRAC
                  </span>
                </span>
                <span className="text-[11px] font-medium text-slate-500  -mt-0.5 flex items-center gap-1 whitespace-nowrap">
                  <span className="inline-block h-1.5 w-1.5 rounded-full bg-indigo-500 animate-pulse shrink-0" />
                  {t('brand.sub', 'Mission Karmayogi Bharat')}
                </span>
              </div>
            </Link>

            {/* Navigation items for authenticated session */}
            {isAuthenticated && user && (
              <nav aria-label="Main Navigation" role="navigation" className="hidden lg:flex items-center space-x-0.5 pl-2 lg:pl-4 border-l border-slate-200  overflow-x-auto scrollbar-hide flex-1">
                <Link
                  to="/"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname === '/'
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.overview', 'Overview')}
                </Link>
                <Link
                  to="/assessment"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname.startsWith('/assessment')
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.assessments', 'Assessments')}
                </Link>
                <Link
                  to="/recommendations"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname === '/recommendations'
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.recommendations', 'Recommendations')}
                </Link>
                <Link
                  to="/learning-path"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname === '/learning-path'
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.learning_path', 'Learning Path')}
                </Link>
                <Link
                  to="/trainer/documents"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname.startsWith('/trainer/documents')
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.trainer_studio', 'Trainer Studio')}
                </Link>
                <Link
                  to="/certificates"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname.startsWith('/certificates')
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.certificates', 'Certificates')}
                </Link>
                <Link
                  to="/admin"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname.startsWith('/admin')
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.admin_analytics', 'Admin Analytics')}
                </Link>
                <Link
                  to="/profile"
                  className={`px-2 py-1 rounded-md text-[13px] font-medium whitespace-nowrap shrink-0 transition-colors ${
                    location.pathname === '/profile'
                      ? 'bg-slate-100  text-slate-900 dark:text-slate-100 '
                      : 'text-slate-600 dark:text-slate-300  hover:text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {t('nav.profile', 'Profile')}
                </Link>
              </nav>
            )}
          </div>

          {/* Right Action Icons & User Menu */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            {/* Multilingual Selector (Eighth Schedule Indic Languages) */}
            <LanguageSelector variant="compact" />

            {/* Notification Bell with Dropdown Popover */}
            {isAuthenticated && (
              <div className="relative">
                <button
                  onClick={() => setNotificationsOpen(!notificationsOpen)}
                  title="Administrative Alerts & Notifications"
                  className="p-2 rounded-lg text-slate-600 dark:text-slate-300  hover:bg-slate-100  transition-colors relative"
                >
                  <Bell className="h-4 w-4" />
                  {unreadCount > 0 && (
                    <span className="absolute top-1 right-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[9px] font-bold text-white shadow-xs">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
                </button>

                {/* Popover drawer */}
                {notificationsOpen && (
                  <div className="absolute right-0 mt-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                    <NotificationCenter
                      onClose={() => setNotificationsOpen(false)}
                      onCountChange={(count) => setUnreadCount(count)}
                    />
                  </div>
                )}
              </div>
            )}

            

            {/* Authenticated user pill / dropdown */}
            {isAuthenticated && user ? (
              <div className="relative">
                <button
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                  className="flex items-center gap-2.5 p-1.5 rounded-lg hover:bg-slate-100  transition-colors"
                >
                  <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center text-slate-900 dark:text-slate-100 text-xs font-bold shadow-sm">
                    {user.full_name
                      .split(' ')
                      .map((n) => n[0])
                      .slice(0, 2)
                      .join('')
                      .toUpperCase()}
                  </div>
                  <div className="hidden lg:flex flex-col text-left">
                    <span className="text-xs font-semibold text-slate-900 dark:text-slate-100  max-w-[130px] truncate">
                      {user.full_name}
                    </span>
                    <span className="text-[10px] text-slate-500  max-w-[130px] truncate">
                      {user.designation}
                    </span>
                  </div>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full border whitespace-nowrap shrink-0 ${
                      getRoleBadge(user.role).classes
                    }`}
                  >
                    {getRoleBadge(user.role).label}
                  </span>
                  <ChevronDown className="h-3.5 w-3.5 text-slate-600 dark:text-slate-300 shrink-0 ml-1" />
                </button>

                {/* Dropdown menu */}
                {userDropdownOpen && (
                  <div
                    onMouseLeave={() => setUserDropdownOpen(false)}
                    className="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200  bg-white  py-1.5 shadow-xl z-50 animate-in fade-in slide-in-from-top-2 duration-150"
                  >
                    <div className="px-4 py-2 border-b border-slate-100 ">
                      <p className="text-xs font-bold text-slate-900 dark:text-slate-100 ">{user.full_name}</p>
                      <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                      <p className="text-[10px] text-teal-600  mt-1 font-medium truncate">
                        {user.department}
                      </p>
                    </div>

                    <Link
                      to="/certificates"
                      onClick={() => setUserDropdownOpen(false)}
                      className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700  hover:bg-slate-50  transition-colors"
                    >
                      <Award className="h-3.5 w-3.5 text-amber-500" />
                      {t('nav.my_certificates', 'My Verifiable Certificates')}
                    </Link>

                    <Link
                      to="/admin"
                      onClick={() => setUserDropdownOpen(false)}
                      className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700  hover:bg-slate-50  transition-colors"
                    >
                      <BarChart3 className="h-3.5 w-3.5 text-teal-600" />
                      {t('nav.cadre_analytics', 'Cadre Analytics Dashboard')}
                    </Link>

                    <Link
                      to="/profile"
                      onClick={() => setUserDropdownOpen(false)}
                      className="flex items-center gap-2 px-4 py-2 text-xs text-slate-700  hover:bg-slate-50  transition-colors"
                    >
                      <UserIcon className="h-3.5 w-3.5" />
                      {t('nav.officer_profile', 'Officer Profile & Security')}
                    </Link>

                    <button
                      onClick={() => {
                        setUserDropdownOpen(false);
                        handleLogout();
                      }}
                      className="flex w-full items-center gap-2 px-4 py-2 text-xs text-rose-600  hover:bg-rose-50  transition-colors text-left"
                    >
                      <LogOut className="h-3.5 w-3.5" />
                      {t('nav.sign_out', 'Sign Out')}
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-700  hover:bg-slate-100  transition-colors"
                >
                  {t('nav.sign_in', 'Sign In')}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-indigo-500 text-white hover:bg-emerald-700 transition-colors shadow-sm shadow-emerald-600/20"
                >
                  {t('nav.register', 'Register')}
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Navigation (Scrollable) */}
        {isAuthenticated && user && (
          <nav
            aria-label="Mobile Navigation"
            role="navigation"
            className="lg:hidden flex items-center space-x-2 px-4 py-2 border-t border-slate-200 overflow-x-auto scrollbar-hide bg-slate-50/50 backdrop-blur-sm"
          >
            <Link to="/" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname === '/' ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.overview', 'Overview')}</Link>
            <Link to="/assessment" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname.startsWith('/assessment') ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.assessments', 'Assessments')}</Link>
            <Link to="/recommendations" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname === '/recommendations' ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.recommendations', 'Recommendations')}</Link>
            <Link to="/learning-path" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname === '/learning-path' ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.learning_path', 'Learning Path')}</Link>
            
            {/* Conditional Roles for Mobile */}
            {(user.role === 'trainer' || user.role === 'admin' || user.role === 'administrator') && (
              <Link to="/trainer/documents" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname.startsWith('/trainer/documents') ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.trainer_studio', 'Trainer Studio')}</Link>
            )}
            {(user.role === 'admin' || user.role === 'administrator' || user.role === 'department_head') && (
              <>
                <Link to="/admin" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname === '/admin' ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.admin_dashboard', 'Admin')}</Link>
                <Link to="/certificates" className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${location.pathname === '/certificates' ? 'bg-indigo-100 text-indigo-700' : 'bg-white text-slate-600 border border-slate-200'}`}>{t('nav.certificates', 'Certificates')}</Link>
              </>
            )}
          </nav>
        )}
      </header>

      
    </>
  );
};

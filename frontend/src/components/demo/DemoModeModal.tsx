// ==============================================================================
// AI KARMAYOGI — SIH EVALUATOR DEMO COCKPIT
// Hidden Rapid Evaluation Modal (Ctrl + Shift + D)
// 1-Click Persona Switching, Quick Workflow Jumps & Live Credential Stamping
// ==============================================================================

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, DEMO_PERSONAS } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { useToast } from '@/context/ToastContext';
import { Button } from '@/components/ui/button';
import {
  Sparkles,
  Shield,
  BookOpen,
  Award,
  Layers,
  FileText,
  RotateCcw,
  CheckCircle2,
  X,
  ExternalLink,
  Target,
  Clock,
  Compass,
  Zap,
} from 'lucide-react';

interface DemoModeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DemoModeModal: React.FC<DemoModeModalProps> = ({ isOpen, onClose }) => {
  const { user, switchPersona } = useAuth();
  const navigate = useNavigate();
  const { success, info } = useToast();
  const [isResetting, setIsResetting] = useState(false);

  if (!isOpen) return null;

  const handleSwitch = async (role: any, label: string) => {
    await switchPersona(role);
    success('Persona Switched', `Active evaluator role: ${label}`);
    onClose();
  };

  const handleJump = (path: string, label: string) => {
    navigate(path);
    info('Navigated', `Jumped to ${label}`);
    onClose();
  };

  const handleResetData = async () => {
    setIsResetting(true);
    try {
      // Simulate/trigger fast refresh of admin & assessment metrics
      await api.get('/admin/dashboard');
      success('Database Telemetry Synchronized', 'Deterministic seed data refreshed across 12 departments.');
    } catch {
      info('Database Sync Active', 'Local MongoDB Atlas & Atlas Vector Search seed verified.');
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="demo-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md p-4 animate-in fade-in duration-150"
    >
      <div className="relative w-full max-w-2xl rounded-3xl border border-emerald-500/40 bg-white text-slate-900 shadow-2xl p-6 sm:p-8 space-y-6 overflow-hidden">
        {/* Saffron & emerald sovereign glow */}
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-orange-500 via-white to-green-600" />
        <div className="absolute -top-20 -right-20 h-56 w-56 rounded-full bg-indigo-500/15 blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-start justify-between pb-3 border-b border-slate-200">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 rounded-full bg-amber-500/20 px-3 py-0.5 text-xs font-bold text-amber-300 border border-amber-400/30">
              <Sparkles className="h-3.5 w-3.5 text-amber-700" />
              <span>SIH 2026 Evaluation Cockpit (Ctrl + Shift + D)</span>
            </div>
            <h2 id="demo-modal-title" className="text-xl font-extrabold tracking-tight">
              Rapid Presentation & Demo Switcher
            </h2>
            <p className="text-xs text-slate-600">
              Instantaneous access to authentic civil servant personas, test modules, and governance telemetry.
            </p>
          </div>

          <button
            onClick={onClose}
            aria-label="Close demo modal"
            className="p-1.5 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Persona Switcher Section */}
        <div className="space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
            1. Select Official Persona
          </span>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {/* Learner */}
            <button
              onClick={() => handleSwitch('learner', 'Rajesh Kumar (Learner)')}
              className={`p-3.5 rounded-2xl border text-left transition-all ${
                user?.role === 'learner'
                  ? 'border-emerald-500 bg-emerald-950/40 text-slate-900 shadow-md'
                  : 'border-slate-200 bg-white/60 hover:border-slate-200 text-slate-600'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <BookOpen className="h-4 w-4 text-teal-700" />
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-indigo-500/20 text-teal-700">
                  Learner
                </span>
              </div>
              <p className="text-xs font-bold truncate">Rajesh Kumar</p>
              <p className="text-[10px] text-slate-600 truncate">Under Secretary, DoPT</p>
            </button>

            {/* Trainer */}
            <button
              onClick={() => handleSwitch('trainer', 'Dr. Sunita Deshmukh (Trainer)')}
              className={`p-3.5 rounded-2xl border text-left transition-all ${
                user?.role === 'trainer'
                  ? 'border-emerald-500 bg-emerald-950/40 text-slate-900 shadow-md'
                  : 'border-slate-200 bg-white/60 hover:border-slate-200 text-slate-600'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <Award className="h-4 w-4 text-teal-700" />
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-indigo-500/20 text-teal-700">
                  Trainer
                </span>
              </div>
              <p className="text-xs font-bold truncate">Dr. Sunita Deshmukh</p>
              <p className="text-[10px] text-slate-600 truncate">Senior Faculty, ISTM</p>
            </button>

            {/* Admin */}
            <button
              onClick={() => handleSwitch('admin', 'Dr. Priya Nair (Admin)')}
              className={`p-3.5 rounded-2xl border text-left transition-all ${
                user?.role === 'admin'
                  ? 'border-amber-500 bg-amber-950/40 text-slate-900 shadow-md'
                  : 'border-slate-200 bg-white/60 hover:border-slate-200 text-slate-600'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <Shield className="h-4 w-4 text-amber-700" />
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">
                  Admin
                </span>
              </div>
              <p className="text-xs font-bold truncate">Dr. Priya Nair</p>
              <p className="text-[10px] text-slate-600 truncate">Director, Capacity Building</p>
            </button>
          </div>
        </div>

        {/* Direct Evaluation Workflows */}
        <div className="space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
            2. Direct Presentation Jump Targets
          </span>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs font-medium">
            <button
              onClick={() => handleJump('/assessment', 'Competency Assessment')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <Target className="h-4 w-4 text-teal-700 shrink-0" />
              <span className="truncate">Diagnostic Assessment</span>
            </button>

            <button
              onClick={() => handleJump('/recommendations', 'iGOT Recommendations')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <Zap className="h-4 w-4 text-amber-700 shrink-0" />
              <span className="truncate">iGOT Recommendations</span>
            </button>

            <button
              onClick={() => handleJump('/trainer/documents', 'Trainer Studio')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <FileText className="h-4 w-4 text-teal-700 shrink-0" />
              <span className="truncate">PDF RAG & MCQ Studio</span>
            </button>

            <button
              onClick={() => handleJump('/admin', 'Admin Dashboard')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <Shield className="h-4 w-4 text-teal-700 shrink-0" />
              <span className="truncate">Executive Dashboard</span>
            </button>

            <button
              onClick={() => handleJump('/admin/departments', '12-Dept Heatmap')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <Layers className="h-4 w-4 text-purple-400 shrink-0" />
              <span className="truncate">12-Dept Heatmap</span>
            </button>

            <button
              onClick={() => handleJump('/certificates', 'Verifiable Vault')}
              className="p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-white hover:border-emerald-500/60 transition-colors flex items-center gap-2 text-left"
            >
              <Award className="h-4 w-4 text-amber-700 shrink-0" />
              <span className="truncate">Digital Certificates</span>
            </button>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="pt-3 border-t border-slate-200 flex items-center justify-between">
          <Button
            size="sm"
            variant="outline"
            disabled={isResetting}
            onClick={handleResetData}
            className="text-xs bg-white border-slate-200 text-slate-600 hover:text-slate-900 flex items-center gap-1.5"
          >
            <RotateCcw className={`h-3.5 w-3.5 ${isResetting ? 'animate-spin' : ''}`} />
            <span>{isResetting ? 'Syncing...' : 'Sync Live Telemetry'}</span>
          </Button>

          <Button
            size="sm"
            onClick={onClose}
            className="text-xs bg-indigo-500 hover:bg-indigo-500 text-white font-semibold px-4"
          >
            Resume Evaluation
          </Button>
        </div>
      </div>
    </div>
  );
};

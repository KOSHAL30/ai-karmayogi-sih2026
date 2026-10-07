// ==============================================================================
// AI KARMAYOGI — SPOTLIGHT COMMAND PALETTE (Ctrl + K)
// Instant Global Search, Keyboard Navigation & Universal Action Dispatcher
// ==============================================================================

import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { useToast } from '@/context/ToastContext';
import {
  Search,
  BookOpen,
  Target,
  Zap,
  Layers,
  Award,
  Shield,
  User,
  Moon,
  Sun,
  Sparkles,
  Compass,
  ArrowRight,
  FileText,
  Clock,
  Check,
} from 'lucide-react';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenDemo: () => void;
}

interface CommandItem {
  id: string;
  category: 'Navigation' | 'Actions' | 'Personas';
  label: string;
  sublabel?: string;
  icon: React.ReactNode;
  shortcut?: string;
  perform: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose, onOpenDemo }) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { switchPersona } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { info, success } = useToast();

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const commands: CommandItem[] = [
    // Navigation
    {
      id: 'nav-overview',
      category: 'Navigation',
      label: 'Mission Overview & Portal',
      sublabel: 'Home landing page',
      icon: <Compass className="h-4 w-4 text-teal-700" />,
      perform: () => {
        navigate('/');
        onClose();
      },
    },
    {
      id: 'nav-assessment',
      category: 'Navigation',
      label: 'Competency Assessment Dashboard',
      sublabel: 'FRAC diagnostic launchpad',
      icon: <Target className="h-4 w-4 text-teal-700" />,
      perform: () => {
        navigate('/assessment');
        onClose();
      },
    },
    {
      id: 'nav-recommendations',
      category: 'Navigation',
      label: 'Personalized Recommendations',
      sublabel: 'Explainable iGOT course recommendations',
      icon: <Zap className="h-4 w-4 text-amber-700" />,
      perform: () => {
        navigate('/recommendations');
        onClose();
      },
    },
    {
      id: 'nav-learning-path',
      category: 'Navigation',
      label: '4-Week Learning Roadmap',
      sublabel: 'Weekly milestone progression',
      icon: <Clock className="h-4 w-4 text-teal-700" />,
      perform: () => {
        navigate('/learning-path');
        onClose();
      },
    },
    {
      id: 'nav-trainer',
      category: 'Navigation',
      label: 'Document Studio & Sovereign RAG',
      sublabel: 'Ingest policy PDFs and generate Bloom MCQs',
      icon: <FileText className="h-4 w-4 text-teal-700" />,
      perform: () => {
        navigate('/trainer/documents');
        onClose();
      },
    },
    {
      id: 'nav-admin',
      category: 'Navigation',
      label: 'Executive Cadre Dashboard',
      sublabel: 'CBC national governance telemetry',
      icon: <Shield className="h-4 w-4 text-teal-700" />,
      perform: () => {
        navigate('/admin');
        onClose();
      },
    },
    {
      id: 'nav-departments',
      category: 'Navigation',
      label: '12-Department Competency Heatmap',
      sublabel: 'Cross-pillar matrix & cadre rankings',
      icon: <Layers className="h-4 w-4 text-purple-400" />,
      perform: () => {
        navigate('/admin/departments');
        onClose();
      },
    },
    {
      id: 'nav-competencies',
      category: 'Navigation',
      label: '10-Axis Competency Radar',
      sublabel: 'Mandated vs Demonstrated deficit audit',
      icon: <Target className="h-4 w-4 text-rose-400" />,
      perform: () => {
        navigate('/admin/competencies');
        onClose();
      },
    },
    {
      id: 'nav-certificates',
      category: 'Navigation',
      label: 'Sovereign Certificates Vault',
      sublabel: 'Verifiable credentials and PDF printing',
      icon: <Award className="h-4 w-4 text-amber-700" />,
      perform: () => {
        navigate('/certificates');
        onClose();
      },
    },
    {
      id: 'nav-profile',
      category: 'Navigation',
      label: 'Officer Profile & Security Settings',
      sublabel: 'Manage credentials & password',
      icon: <User className="h-4 w-4 text-slate-600" />,
      perform: () => {
        navigate('/profile');
        onClose();
      },
    },

    // Actions
    {
      id: 'action-theme',
      category: 'Actions',
      label: `Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`,
      sublabel: 'Toggle application color scheme',
      icon: theme === 'dark' ? <Sun className="h-4 w-4 text-amber-700" /> : <Moon className="h-4 w-4 text-teal-700" />,
      perform: () => {
        toggleTheme();
        info('Theme Updated', `Switched to ${theme === 'dark' ? 'light' : 'dark'} mode.`);
        onClose();
      },
    },
    {
      id: 'action-demo-cockpit',
      category: 'Actions',
      label: 'Open SIH Evaluation Cockpit',
      sublabel: 'Instant demo switcher & database sync',
      icon: <Sparkles className="h-4 w-4 text-amber-700" />,
      shortcut: 'Ctrl+Shift+D',
      perform: () => {
        onClose();
        onOpenDemo();
      },
    },

    // Personas
    {
      id: 'persona-learner',
      category: 'Personas',
      label: 'Switch to Rajesh Kumar (Learner)',
      sublabel: 'Under Secretary, DoPT',
      icon: <BookOpen className="h-4 w-4 text-teal-700" />,
      perform: async () => {
        await switchPersona('learner');
        success('Persona Switched', 'Active: Rajesh Kumar (Learner)');
        onClose();
      },
    },
    {
      id: 'persona-trainer',
      category: 'Personas',
      label: 'Switch to Dr. Sunita Deshmukh (Trainer)',
      sublabel: 'Senior Faculty, ISTM',
      icon: <Award className="h-4 w-4 text-teal-700" />,
      perform: async () => {
        await switchPersona('trainer');
        success('Persona Switched', 'Active: Dr. Sunita Deshmukh (Trainer)');
        onClose();
      },
    },
    {
      id: 'persona-admin',
      category: 'Personas',
      label: 'Switch to Dr. Priya Nair (Admin)',
      sublabel: 'Director, Capacity Building Commission',
      icon: <Shield className="h-4 w-4 text-amber-700" />,
      perform: async () => {
        await switchPersona('admin');
        success('Persona Switched', 'Active: Dr. Priya Nair (Admin)');
        onClose();
      },
    },
  ];

  // Filter commands
  const filtered = commands.filter((c) => {
    const text = `${c.label} ${c.sublabel || ''} ${c.category}`.toLowerCase();
    return text.includes(query.toLowerCase());
  });

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (filtered.length || 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + filtered.length) % (filtered.length || 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filtered[selectedIndex]) {
        filtered[selectedIndex].perform();
      }
    } else if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-start justify-center pt-20 sm:pt-28 bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-100"
    >
      <div className="relative w-full max-w-xl rounded-2xl border border-slate-200 bg-white/95 text-slate-900 shadow-2xl overflow-hidden flex flex-col backdrop-blur-xl">
        {/* Search Header */}
        <div className="flex items-center gap-3 px-4 py-3.5 border-b border-slate-200">
          <Search className="h-5 w-5 text-teal-700 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Type a command, page name, or persona..."
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            onKeyDown={handleKeyDown}
            className="flex-1 bg-transparent text-sm text-slate-900 placeholder:text-slate-500 focus:outline-none"
          />
          <kbd className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-mono font-semibold rounded bg-white text-slate-600 border border-slate-200">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-80 overflow-y-auto p-2 divide-y divide-slate-800/40">
          {filtered.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-500">
              No matching commands found for "{query}".
            </div>
          ) : (
            filtered.map((item, index) => (
              <div
                key={item.id}
                onClick={item.perform}
                onMouseEnter={() => setSelectedIndex(index)}
                className={`flex items-center justify-between p-2.5 rounded-xl cursor-pointer transition-colors ${
                  selectedIndex === index
                    ? 'bg-indigo-500/30 text-slate-900 border border-emerald-500/40'
                    : 'text-slate-600 hover:bg-white/60 border border-transparent'
                }`}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="p-1.5 rounded-lg bg-white/80 shrink-0">
                    {item.icon}
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs font-bold truncate">{item.label}</p>
                    {item.sublabel && (
                      <p className="text-[10px] text-slate-600 truncate">{item.sublabel}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  {item.shortcut && (
                    <kbd className="px-1.5 py-0.5 text-[9px] font-mono rounded bg-white text-slate-600 border border-slate-200">
                      {item.shortcut}
                    </kbd>
                  )}
                  <span className="text-[10px] uppercase tracking-wider font-semibold text-slate-500">
                    {item.category}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer Navigation Hints */}
        <div className="px-4 py-2 bg-white/60 border-t border-slate-200/80 flex items-center justify-between text-[11px] text-slate-500">
          <div className="flex items-center gap-3">
            <span>↑↓ Navigate</span>
            <span>↵ Select</span>
            <span>ESC Close</span>
          </div>
          <span className="font-semibold text-teal-700">AI Karmayogi Spotlight</span>
        </div>
      </div>
    </div>
  );
};

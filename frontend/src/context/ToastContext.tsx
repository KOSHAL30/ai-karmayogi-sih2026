// ==============================================================================
// AI KARMAYOGI — SOVEREIGN TOAST NOTIFICATION SYSTEM
// Accessible In-App Alert Banners with Auto-Dismiss & Custom Event Dispatch
// ==============================================================================

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Info,
  X,
} from 'lucide-react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastItem {
  id: string;
  type: ToastType;
  title: string;
  description?: string;
  duration?: number;
}

interface ToastContextType {
  toast: (opts: Omit<ToastItem, 'id'>) => void;
  success: (title: string, description?: string) => void;
  error: (title: string, description?: string) => void;
  warning: (title: string, description?: string) => void;
  info: (title: string, description?: string) => void;
  removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback(
    ({ type = 'info', title, description, duration = 4000 }: Omit<ToastItem, 'id'>) => {
      const id = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
      setToasts((prev) => [...prev, { id, type, title, description, duration }]);

      if (duration > 0) {
        setTimeout(() => {
          removeToast(id);
        }, duration);
      }
    },
    [removeToast]
  );

  const success = useCallback((title: string, description?: string) => toast({ type: 'success', title, description }), [toast]);
  const error = useCallback((title: string, description?: string) => toast({ type: 'error', title, description }), [toast]);
  const warning = useCallback((title: string, description?: string) => toast({ type: 'warning', title, description }), [toast]);
  const info = useCallback((title: string, description?: string) => toast({ type: 'info', title, description }), [toast]);

  // Support global window event dispatch for calls from non-React modules (like api.ts)
  useEffect(() => {
    const handleGlobalToast = (e: Event) => {
      const customEvent = e as CustomEvent<Omit<ToastItem, 'id'>>;
      if (customEvent.detail) {
        toast(customEvent.detail);
      }
    };

    window.addEventListener('karmayogi:toast', handleGlobalToast);
    return () => window.removeEventListener('karmayogi:toast', handleGlobalToast);
  }, [toast]);

  const getIcon = (type: ToastType) => {
    switch (type) {
      case 'success':
        return <CheckCircle2 className="h-4 w-4 text-teal-600 shrink-0" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-rose-500 shrink-0" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-amber-500 shrink-0" />;
      case 'info':
      default:
        return <Info className="h-4 w-4 text-teal-600 shrink-0" />;
    }
  };

  const getBorderColor = (type: ToastType) => {
    switch (type) {
      case 'success':
        return 'border-emerald-500/30 bg-emerald-50/90 /80';
      case 'error':
        return 'border-rose-500/30 bg-rose-50/90 /80';
      case 'warning':
        return 'border-amber-500/30 bg-amber-50/90 /80';
      case 'info':
      default:
        return 'border-emerald-500/30 bg-emerald-50/90 /80';
    }
  };

  return (
    <ToastContext.Provider value={{ toast, success, error, warning, info, removeToast }}>
      {children}

      {/* Floating Toast Notification Container */}
      <aside
        aria-live="polite"
        aria-label="Notifications"
        className="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm w-full pointer-events-none"
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            role="status"
            className={`pointer-events-auto flex items-start gap-3 p-3.5 rounded-2xl border backdrop-blur-md shadow-xl text-slate-900  transition-all animate-in slide-in-from-bottom-3 duration-200 ${getBorderColor(
              t.type
            )}`}
          >
            <div className="mt-0.5">{getIcon(t.type)}</div>
            <div className="flex-1 space-y-0.5 text-xs">
              <p className="font-bold leading-tight">{t.title}</p>
              {t.description && (
                <p className="text-[11px] text-slate-600  leading-relaxed">
                  {t.description}
                </p>
              )}
            </div>
            <button
              onClick={() => removeToast(t.id)}
              className="p-1 rounded-lg text-slate-600 hover:text-slate-700  transition-colors shrink-0">
              aria-label="Dismiss notification"
            
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        ))}
      </aside>
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// Utility function to dispatch toast from anywhere (even outside React components)
export const notify = (opts: Omit<ToastItem, 'id'>) => {
  window.dispatchEvent(new CustomEvent('karmayogi:toast', { detail: opts }));
};

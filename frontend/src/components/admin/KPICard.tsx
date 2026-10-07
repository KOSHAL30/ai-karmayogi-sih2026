// ==============================================================================
// AI KARMAYOGI — EXECUTIVE KPI METRIC CARD
// Stripe / Linear Aesthetic with Sovereign Accent & Trend Indicators
// ==============================================================================

import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  label: string;
  value: string | number;
  changePct?: number;
  trend?: 'up' | 'down' | 'neutral';
  period?: string;
  description?: string;
  icon: React.ReactNode;
  variant?: 'emerald' | 'emerald' | 'amber' | 'teal' | 'purple' | 'slate';
}

export const KPICard: React.FC<KPICardProps> = ({
  label,
  value,
  changePct,
  trend = 'up',
  period = 'vs last month',
  description,
  icon,
  variant = 'emerald',
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'emerald':
        return {
          iconBg: 'bg-emerald-50 /60 text-teal-600  border-emerald-200/60 ',
          accent: 'border-l-emerald-500',
        };
      case 'amber':
        return {
          iconBg: 'bg-amber-50 /60 text-amber-600  border-amber-200/60 ',
          accent: 'border-l-amber-500',
        };
      case 'teal':
        return {
          iconBg: 'bg-teal-50 /60 text-teal-600  border-teal-200/60 ',
          accent: 'border-l-teal-500',
        };
      case 'purple':
        return {
          iconBg: 'bg-purple-50 /60 text-purple-600  border-purple-200/60 ',
          accent: 'border-l-purple-500',
        };
      case 'emerald':
      default:
        return {
          iconBg: 'bg-emerald-50 /60 text-teal-600  border-emerald-200/60 ',
          accent: 'border-l-emerald-500',
        };
    }
  };

  const styles = getVariantStyles();

  return (
    <div className={`relative overflow-hidden rounded-2xl border border-slate-200  bg-white/90 /90 backdrop-blur-sm p-5 shadow-sm hover:shadow-md hover:border-slate-300  transition-all group`}>
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1 min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500  truncate">
            {label}
          </p>
          <div className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 ">
            {value}
          </div>
        </div>

        <div className={`h-11 w-11 rounded-xl border flex items-center justify-center shrink-0 ${styles.iconBg} shadow-sm group-hover:scale-105 transition-transform duration-200`}>
          {icon}
        </div>
      </div>

      <div className="mt-3.5 pt-3 border-t border-slate-100 /80 flex items-center justify-between text-xs">
        {changePct !== undefined ? (
          <div className="flex items-center gap-1">
            <span
              className={`inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded-full text-[10px] font-bold ${
                trend === 'up'
                  ? 'bg-emerald-50 /60 text-emerald-700 '
                  : trend === 'down'
                  ? 'bg-rose-50 /60 text-rose-700 '
                  : 'bg-slate-100  text-slate-600 '
              }`}
            >
              {trend === 'up' && <TrendingUp className="h-2.5 w-2.5" />}
              {trend === 'down' && <TrendingDown className="h-2.5 w-2.5" />}
              {trend === 'neutral' && <Minus className="h-2.5 w-2.5" />}
              {trend === 'up' ? '+' : ''}{changePct}%
            </span>
            <span className="text-[11px] text-slate-600">{period}</span>
          </div>
        ) : (
          <span className="text-[11px] text-slate-600 truncate">{description || 'Executive metric'}</span>
        )}

        {description && changePct !== undefined && (
          <span className="hidden sm:inline text-[10px] text-slate-600 truncate max-w-[160px]">
            {description}
          </span>
        )}
      </div>
    </div>
  );
};

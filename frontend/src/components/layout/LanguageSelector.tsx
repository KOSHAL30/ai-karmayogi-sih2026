// ==============================================================================
// AI KARMAYOGI — SOVEREIGN MULTILINGUAL SELECTOR
// Supports Official Eighth Schedule Indian Languages for Scalable Civil Services Access
// ==============================================================================

import React, { useState, useRef, useEffect } from 'react';
import { Globe, Check, ChevronDown } from 'lucide-react';

import { useLanguage, SupportedLanguage } from '@/context/LanguageContext';

export interface LanguageOption {
  code: string;
  name: string;
  nativeName: string;
  region: string;
}

export const SUPPORTED_LANGUAGES: LanguageOption[] = [
  { code: 'en', name: 'English', nativeName: 'English (India)', region: 'Official' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', region: 'Official / Union' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', region: 'Eighth Schedule' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', region: 'Eighth Schedule' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', region: 'Eighth Schedule' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', region: 'Eighth Schedule' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', region: 'Eighth Schedule' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', region: 'Eighth Schedule' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം', region: 'Eighth Schedule' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', region: 'Eighth Schedule' },
  { code: 'or', name: 'Odia', nativeName: 'ଓଡ଼ିଆ', region: 'Eighth Schedule' },
  { code: 'as', name: 'Assamese', nativeName: 'অসমীয়া', region: 'Eighth Schedule' },
];

interface LanguageSelectorProps {
  variant?: 'compact' | 'expanded';
  className?: string;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  variant = 'compact',
  className = '',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const { language, setLanguage } = useLanguage();

  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleSelectLanguage = (code: string) => {
    setLanguage(code as SupportedLanguage);
    setIsOpen(false);
  };

  const activeOption =
    SUPPORTED_LANGUAGES.find((lang) => lang.code === language) || SUPPORTED_LANGUAGES[0];

  return (
    <div className={`relative inline-block text-left ${className}`} ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-haspopup="true"
        title={`Change Language (Current: ${activeOption.nativeName})`}
        className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-150 ${
          isOpen
            ? 'bg-slate-200  text-slate-900  ring-2 ring-emerald-500/20'
            : 'text-slate-600  hover:bg-slate-100  hover:text-slate-900'
        }`}
      >
        <Globe className="h-4 w-4 text-teal-600  shrink-0" />
        {variant === 'expanded' ? (
          <span className="hidden sm:inline-block truncate max-w-[90px]">
            {activeOption.nativeName}
          </span>
        ) : (
          <span className="uppercase text-[11px] font-bold tracking-wider font-mono">
            {activeOption.code}
          </span>
        )}
        <ChevronDown
          className={`h-3 w-3 text-slate-600 transition-transform duration-150 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {/* Popover Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 rounded-2xl border border-slate-200  bg-white  shadow-2xl z-50 animate-in fade-in zoom-in-95 duration-150 overflow-hidden">
          {/* Header */}
          <div className="px-3.5 py-2.5 bg-slate-50 /60 border-b border-slate-100  flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Globe className="h-3.5 w-3.5 text-teal-600" />
              <span className="text-xs font-bold text-slate-900 ">
                Select Language
              </span>
            </div>
            <span className="text-[10px] font-mono text-slate-600">
              8th Schedule
            </span>
          </div>

          {/* Language Options List */}
          <div className="max-h-64 overflow-y-auto py-1.5 divide-y divide-slate-100/60 ">
            {SUPPORTED_LANGUAGES.map((lang) => {
              const isSelected = lang.code === language;
              return (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => handleSelectLanguage(lang.code)}
                  className={`w-full text-left px-3.5 py-2 flex items-center justify-between text-xs transition-colors group ${
                    isSelected
                      ? 'bg-emerald-50/80 /40 text-emerald-700  font-semibold'
                      : 'text-slate-700  hover:bg-slate-50'
                  }`}
                >
                  <div className="flex flex-col">
                    <span className="text-xs font-medium group-hover:text-teal-600 :text-teal-700">
                      {lang.nativeName}
                    </span>
                    <span className="text-[10px] text-slate-600 ">
                      {lang.name} • {lang.region}
                    </span>
                  </div>

                  {isSelected && (
                    <div className="h-5 w-5 rounded-full bg-indigo-500 text-white flex items-center justify-center shrink-0">
                      <Check className="h-3 w-3 stroke-[3]" />
                    </div>
                  )}
                </button>
              );
            })}
          </div>

          {/* Footer Note */}
          <div className="px-3.5 py-2 bg-slate-50/70 /40 border-t border-slate-100  text-[10px] text-slate-600">
            Bhashini Indic AI translation integration ready
          </div>
        </div>
      )}
    </div>
  );
};

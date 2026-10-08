import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", error, helperText, disabled, ...props }, ref) => {
    return (
      <div className="w-full space-y-1">
        <input
          type={type}
          disabled={disabled}
          ref={ref}
          className={cn(
            "flex h-10 w-full rounded-lg border border-slate-300  bg-white  px-3 py-2 text-sm text-slate-900 dark:text-slate-100  placeholder:text-slate-600 dark:text-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:border-transparent disabled:cursor-not-allowed disabled:opacity-50 transition-all",
            error && "border-rose-500 focus-visible:ring-rose-500",
            className
          )}
          {...props}
        />
        {error ? (
          <p className="text-xs text-rose-500 font-medium">{error}</p>
        ) : helperText ? (
          <p className="text-xs text-slate-500 ">{helperText}</p>
        ) : null}
      </div>
    );
  }
);

Input.displayName = "Input";

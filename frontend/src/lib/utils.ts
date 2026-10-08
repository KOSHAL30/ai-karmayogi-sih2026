import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines multiple conditional class names and merges Tailwind conflicts.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formats a decimal percentage for dashboard display.
 */
export function formatPercentage(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`;
}

/**
 * Maps FRAC proficiency level (1 to 5) to human-readable label.
 */
export function getProficiencyLabel(level: number): string {
  switch (level) {
    case 1: return "Level 1 (Basic Awareness)";
    case 2: return "Level 2 (Novice Practitioner)";
    case 3: return "Level 3 (Working Proficiency)";
    case 4: return "Level 4 (Advanced Authority)";
    case 5: return "Level 5 (Mastery / Expert)";
    default: return `Level ${level}`;
  }
}

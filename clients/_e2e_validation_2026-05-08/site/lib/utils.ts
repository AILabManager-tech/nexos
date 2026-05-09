import clsx, { type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind class names safely.
 *
 * Combines `clsx` (conditionals, arrays, objects) with `tailwind-merge`
 * so that conflicting utilities (e.g. `px-2` + `px-4`) collapse to the last one.
 *
 * @param inputs - Any clsx-compatible class values.
 * @returns Deduplicated, conflict-aware Tailwind class string.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

import type { ReactNode } from 'react';
import { cn } from '@/lib/cn';

interface BadgeProps {
  children: ReactNode;
  variant?: 'accent' | 'primary' | 'info' | 'warning';
  className?: string;
}

const styles: Record<NonNullable<BadgeProps['variant']>, string> = {
  accent: 'bg-accent text-accent-foreground',
  primary: 'bg-primary text-primary-foreground',
  info: 'bg-info text-white',
  warning: 'bg-warning text-white',
};

export function Badge({ children, variant = 'accent', className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full px-3 py-1 text-small font-semibold',
        styles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}

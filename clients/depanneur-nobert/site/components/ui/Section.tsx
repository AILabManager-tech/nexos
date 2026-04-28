import type { ComponentPropsWithoutRef, ReactNode } from 'react';
import { cn } from '@/lib/cn';

interface SectionProps extends ComponentPropsWithoutRef<'section'> {
  variant?: 'background' | 'background-alt' | 'surface' | 'primary';
  children?: ReactNode;
}

const bgStyles: Record<NonNullable<SectionProps['variant']>, string> = {
  background: 'bg-background',
  'background-alt': 'bg-background-alt',
  surface: 'bg-surface',
  primary: 'bg-primary text-primary-foreground',
};

export function Section({
  className,
  variant = 'background',
  children,
  ...props
}: SectionProps) {
  return (
    <section
      className={cn(
        'py-12 sm:py-16 lg:py-20',
        bgStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </section>
  );
}

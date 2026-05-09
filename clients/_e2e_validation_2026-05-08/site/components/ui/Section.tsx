import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface SectionProps extends HTMLAttributes<HTMLElement> {
  alt?: boolean;
}

export function Section({ alt, className, children, ...rest }: SectionProps) {
  return (
    <section
      className={cn(
        'py-12 sm:py-16 lg:py-24',
        alt ? 'bg-surface' : 'bg-background',
        className,
      )}
      {...rest}
    >
      {children}
    </section>
  );
}

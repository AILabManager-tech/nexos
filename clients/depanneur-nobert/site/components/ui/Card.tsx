import type { ComponentPropsWithoutRef } from 'react';
import { cn } from '@/lib/cn';

export function Card({
  className,
  ...props
}: ComponentPropsWithoutRef<'article'>) {
  return (
    <article
      className={cn(
        'bg-surface border border-border rounded-lg p-6 shadow-sm',
        'transition-shadow duration-200 hover:shadow-card-hover',
        className
      )}
      {...props}
    />
  );
}

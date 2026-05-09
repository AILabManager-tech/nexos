import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export function Card({
  className,
  children,
  ...rest
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        'rounded-lg border border-border bg-surface p-4 shadow-sm transition-shadow duration-300 ease-enter hover:shadow-card-hover sm:p-6',
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

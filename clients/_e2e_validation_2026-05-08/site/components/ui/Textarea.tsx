import { forwardRef, type TextareaHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  invalid?: boolean;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  function Textarea({ invalid, className, ...rest }, ref) {
    return (
      <textarea
        ref={ref}
        aria-invalid={invalid || undefined}
        className={cn(
          'block w-full rounded border bg-surface px-3 py-2.5 text-base text-text',
          'placeholder:text-text-muted',
          'focus:outline-none focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2',
          invalid ? 'border-error' : 'border-border-strong',
          'min-h-[140px]',
          className,
        )}
        {...rest}
      />
    );
  },
);

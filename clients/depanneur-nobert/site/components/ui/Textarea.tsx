import { type ComponentPropsWithoutRef, forwardRef, useId } from 'react';
import { cn } from '@/lib/cn';

interface TextareaProps extends ComponentPropsWithoutRef<'textarea'> {
  label: string;
  error?: string;
  hint?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, hint, className, id: providedId, required, ...props }, ref) => {
    const reactId = useId();
    const id = providedId ?? reactId;
    const errorId = `${id}-error`;
    const hintId = `${id}-hint`;
    const describedBy =
      [error ? errorId : null, hint ? hintId : null].filter(Boolean).join(' ') || undefined;

    return (
      <div className="space-y-2">
        <label
          htmlFor={id}
          className="block text-small font-semibold text-text"
        >
          {label}
          {required && (
            <span aria-hidden="true" className="ml-1 text-error">
              *
            </span>
          )}
        </label>
        {hint && (
          <p id={hintId} className="text-small text-text-muted">
            {hint}
          </p>
        )}
        <textarea
          ref={ref}
          id={id}
          required={required}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy}
          className={cn(
            'block w-full rounded border border-border bg-surface px-4 py-3 text-base min-h-[140px]',
            'placeholder:text-text-muted/70',
            'focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:border-primary',
            error && 'border-error focus-visible:ring-error',
            className
          )}
          {...props}
        />
        {error && (
          <p id={errorId} role="alert" className="text-small text-error">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Textarea.displayName = 'Textarea';

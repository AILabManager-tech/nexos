import { type ComponentPropsWithoutRef, forwardRef, useId, type ReactNode } from 'react';
import { cn } from '@/lib/cn';

interface CheckboxProps extends ComponentPropsWithoutRef<'input'> {
  label: ReactNode;
  description?: ReactNode;
  error?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, description, error, id: providedId, className, required, ...props }, ref) => {
    const reactId = useId();
    const id = providedId ?? reactId;
    const errorId = `${id}-error`;
    const descId = `${id}-desc`;
    const describedBy =
      [error ? errorId : null, description ? descId : null].filter(Boolean).join(' ') || undefined;

    return (
      <div className="space-y-2">
        <label htmlFor={id} className="flex items-start gap-3 cursor-pointer">
          <input
            ref={ref}
            id={id}
            type="checkbox"
            required={required}
            aria-invalid={error ? true : undefined}
            aria-describedby={describedBy}
            className={cn(
              'mt-1 h-5 w-5 shrink-0 rounded border border-border bg-surface accent-primary',
              'focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2',
              error && 'border-error',
              className
            )}
            {...props}
          />
          <span className="text-small leading-relaxed text-text">
            {label}
            {required && (
              <span aria-hidden="true" className="ml-1 text-error">
                *
              </span>
            )}
          </span>
        </label>
        {description && (
          <p id={descId} className="ml-8 text-small text-text-muted">
            {description}
          </p>
        )}
        {error && (
          <p id={errorId} role="alert" className="ml-8 text-small text-error">
            {error}
          </p>
        )}
      </div>
    );
  }
);
Checkbox.displayName = 'Checkbox';

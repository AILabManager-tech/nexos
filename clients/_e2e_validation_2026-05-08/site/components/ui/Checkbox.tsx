import { forwardRef, type InputHTMLAttributes, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {
  label: ReactNode;
  invalid?: boolean;
  detail?: ReactNode;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  function Checkbox({ label, detail, invalid, className, id, ...rest }, ref) {
    const checkboxId = id ?? `cb-${Math.random().toString(36).slice(2, 9)}`;
    return (
      <label
        htmlFor={checkboxId}
        className={cn('flex gap-3 cursor-pointer items-start', className)}
      >
        <input
          ref={ref}
          id={checkboxId}
          type="checkbox"
          aria-invalid={invalid || undefined}
          className={cn(
            'mt-0.5 h-5 w-5 shrink-0 rounded border border-border-strong text-primary',
            'focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2',
            invalid && 'border-error',
          )}
          {...rest}
        />
        <span className="flex flex-col gap-1 text-sm leading-relaxed text-text">
          <span>{label}</span>
          {detail && <span className="text-xs text-text-muted">{detail}</span>}
        </span>
      </label>
    );
  },
);

import { cloneElement, isValidElement, type ReactElement, type ReactNode } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

type Props = {
  variant?: Variant;
  size?: Size;
  asChild?: boolean;
  className?: string;
  children: ReactNode;
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

const VARIANTS: Record<Variant, string> = {
  primary: 'bg-primary text-surface hover:bg-primary-600 focus-visible:ring-primary-300',
  secondary: 'bg-surface-alt text-ink hover:bg-accent-soft focus-visible:ring-primary-300',
  ghost: 'bg-transparent text-ink hover:bg-surface-alt focus-visible:ring-primary-300'
};

const SIZES: Record<Size, string> = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-6 py-3 text-base',
  lg: 'px-8 py-4 text-lg'
};

const BASE =
  'inline-flex items-center justify-center gap-2 rounded-full font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-surface disabled:opacity-60 disabled:cursor-not-allowed';

export function Button({
  variant = 'primary',
  size = 'md',
  asChild = false,
  className = '',
  children,
  ...rest
}: Props) {
  const classes = `${BASE} ${VARIANTS[variant]} ${SIZES[size]} ${className}`.trim();

  if (asChild && isValidElement(children)) {
    const child = children as ReactElement<{ className?: string }>;
    return cloneElement(child, {
      className: `${classes} ${child.props.className ?? ''}`.trim()
    });
  }

  return (
    <button className={classes} {...rest}>
      {children}
    </button>
  );
}

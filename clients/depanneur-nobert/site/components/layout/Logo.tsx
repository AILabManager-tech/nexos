import { cn } from '@/lib/cn';

interface LogoProps {
  variant?: 'full' | 'short';
  color?: 'primary' | 'inverse';
  className?: string;
}

export function Logo({ variant = 'full', color = 'primary', className }: LogoProps) {
  const text = variant === 'full' ? 'Dépanneur Nobert' : 'Nobert';
  const colorClass = color === 'inverse' ? 'text-primary-foreground' : 'text-primary';

  return (
    <span
      className={cn(
        'font-heading font-bold tracking-tight text-2xl',
        colorClass,
        className
      )}
    >
      {text}
    </span>
  );
}

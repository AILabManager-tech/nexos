import { describe, it, expect } from 'vitest';
import { cn } from '@/lib/utils';

describe('cn', () => {
  it('joins class names', () => {
    expect(cn('a', 'b')).toBe('a b');
  });

  it('handles falsy values', () => {
    expect(cn('a', false && 'b', undefined, null, 'c')).toBe('a c');
  });

  it('merges conflicting Tailwind classes (twMerge wins on the last one)', () => {
    expect(cn('px-2', 'px-4')).toBe('px-4');
    expect(cn('text-red-500', 'text-blue-500')).toBe('text-blue-500');
  });

  it('keeps non-conflicting classes', () => {
    expect(cn('px-2', 'py-4')).toBe('px-2 py-4');
  });

  it('accepts arrays and objects (clsx behavior)', () => {
    expect(cn(['a', 'b'], { c: true, d: false })).toBe('a b c');
  });
});

import { describe, expect, it } from 'vitest';
import { cn } from '../lib/cn';

describe('cn() — class name merger', () => {
  it('concatène plusieurs strings sans doublons', () => {
    expect(cn('px-4', 'py-2')).toBe('px-4 py-2');
  });

  it('merge les classes Tailwind conflictuelles (dernière gagne)', () => {
    // tailwind-merge : px-4 puis px-8 → seul px-8 reste
    expect(cn('px-4', 'px-8')).toBe('px-8');
  });

  it('ignore les valeurs falsy', () => {
    expect(cn('a', false, null, undefined, '', 'b')).toBe('a b');
  });

  it('accepte un tableau de classes', () => {
    expect(cn(['px-2', 'py-1'])).toBe('px-2 py-1');
  });

  it('résout les conditions clsx', () => {
    expect(cn('base', { active: true, hidden: false })).toBe('base active');
  });
});

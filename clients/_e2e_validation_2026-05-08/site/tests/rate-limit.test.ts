import { describe, it, expect } from 'vitest';
import { rateLimit } from '@/lib/rate-limit';

describe('rateLimit', () => {
  it('allows the first request and decrements remaining', () => {
    const r = rateLimit('test:first', 3, 60_000);
    expect(r.allowed).toBe(true);
    expect(r.remaining).toBe(2);
    expect(r.resetAt).toBeGreaterThan(Date.now());
  });

  it('blocks once the limit is exhausted in the same window', () => {
    const key = 'test:exhaust';
    expect(rateLimit(key, 2, 60_000).allowed).toBe(true);
    expect(rateLimit(key, 2, 60_000).allowed).toBe(true);
    const blocked = rateLimit(key, 2, 60_000);
    expect(blocked.allowed).toBe(false);
    expect(blocked.remaining).toBe(0);
  });

  it('resets after the window expires', async () => {
    const key = 'test:window';
    expect(rateLimit(key, 1, 5).allowed).toBe(true);
    expect(rateLimit(key, 1, 5).allowed).toBe(false);
    await new Promise((resolve) => setTimeout(resolve, 15));
    const after = rateLimit(key, 1, 5);
    expect(after.allowed).toBe(true);
  });

  it('isolates state per key', () => {
    const a = rateLimit('test:keyA', 1, 60_000);
    const b = rateLimit('test:keyB', 1, 60_000);
    expect(a.allowed).toBe(true);
    expect(b.allowed).toBe(true);
  });
});

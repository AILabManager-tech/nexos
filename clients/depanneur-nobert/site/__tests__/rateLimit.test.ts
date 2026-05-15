import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { rateLimit } from '../lib/rateLimit';

describe('rateLimit() — token bucket per key', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-05-15T00:00:00Z'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('autorise la première requête et décrémente le remaining', () => {
    const r = rateLimit('test-key-fresh', 5, 60_000);
    expect(r.allowed).toBe(true);
    expect(r.remaining).toBe(4);
    expect(r.resetIn).toBe(60_000);
  });

  it('bloque après dépassement de la limite', () => {
    const key = 'test-key-burst';
    for (let i = 0; i < 3; i++) rateLimit(key, 3, 60_000);
    const blocked = rateLimit(key, 3, 60_000);
    expect(blocked.allowed).toBe(false);
    expect(blocked.remaining).toBe(0);
  });

  it('reset le bucket après expiration de la window', () => {
    const key = 'test-key-reset';
    for (let i = 0; i < 5; i++) rateLimit(key, 5, 1_000);
    expect(rateLimit(key, 5, 1_000).allowed).toBe(false);

    vi.advanceTimersByTime(1_500);
    const after = rateLimit(key, 5, 1_000);
    expect(after.allowed).toBe(true);
    expect(after.remaining).toBe(4);
  });

  it('isole les clés indépendantes', () => {
    rateLimit('alice', 2, 60_000);
    rateLimit('alice', 2, 60_000);
    expect(rateLimit('alice', 2, 60_000).allowed).toBe(false);
    expect(rateLimit('bob', 2, 60_000).allowed).toBe(true);
  });
});

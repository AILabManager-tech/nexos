// Tests promotions — filtrage actif, top, dernière mise à jour (P4c).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  getActivePromotions,
  getLastUpdate,
  getTopPromotions,
} from '../lib/promotions';

describe('promotions — filtre temporel + tri', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  it('getActivePromotions retourne un tableau', () => {
    const result = getActivePromotions();
    expect(Array.isArray(result)).toBe(true);
  });

  it('getActivePromotions filtre les promotions actives au 1er juin 2026', () => {
    // À cette date, les promos Q1/Q2 doivent être visibles (validUntil > juin).
    vi.setSystemTime(new Date('2026-06-01T12:00:00Z'));
    const active = getActivePromotions();
    for (const promo of active) {
      const start = new Date(promo.validFrom);
      const end = new Date(promo.validUntil);
      const now = new Date('2026-06-01T12:00:00Z');
      expect(start.getTime()).toBeLessThanOrEqual(now.getTime());
      expect(end.getTime()).toBeGreaterThanOrEqual(now.getTime());
    }
  });

  it('getActivePromotions retourne 0 promo en 2030 (toutes expirées)', () => {
    vi.setSystemTime(new Date('2030-01-01T00:00:00Z'));
    const active = getActivePromotions();
    expect(active.length).toBe(0);
  });

  it('getActivePromotions trie par validUntil ascendant (les plus urgentes en premier)', () => {
    vi.setSystemTime(new Date('2026-06-01T00:00:00Z'));
    const active = getActivePromotions();
    if (active.length < 2) return;
    for (let i = 1; i < active.length; i++) {
      const prev = new Date(active[i - 1]!.validUntil).getTime();
      const cur = new Date(active[i]!.validUntil).getTime();
      expect(prev).toBeLessThanOrEqual(cur);
    }
  });

  it('getTopPromotions limite à 3 par défaut', () => {
    vi.setSystemTime(new Date('2026-06-01T00:00:00Z'));
    const top = getTopPromotions();
    expect(top.length).toBeLessThanOrEqual(3);
  });

  it('getTopPromotions limite custom respecté', () => {
    vi.setSystemTime(new Date('2026-06-01T00:00:00Z'));
    const top = getTopPromotions(1);
    expect(top.length).toBeLessThanOrEqual(1);
  });

  it('getLastUpdate retourne une string YYYY-MM-DD valide', () => {
    const result = getLastUpdate();
    expect(result).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });
});

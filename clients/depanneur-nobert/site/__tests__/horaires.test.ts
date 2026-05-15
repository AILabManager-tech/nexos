// Tests horaires — getHoraires / getRegularHoraires (P4c).
import { describe, expect, it } from 'vitest';
import { getHoraires, getRegularHoraires } from '../lib/horaires';

describe('horaires', () => {
  it('getHoraires retourne un objet avec regular[]', () => {
    const result = getHoraires();
    expect(result).toBeDefined();
    expect(Array.isArray(result.regular)).toBe(true);
  });

  it('getRegularHoraires retourne 7 jours (lun-dim) ou la liste configurée', () => {
    const regular = getRegularHoraires();
    expect(Array.isArray(regular)).toBe(true);
    // Sanity : chaque entrée a au moins { day } (structure HoraireJour)
    for (const horaire of regular) {
      expect(horaire).toHaveProperty('day');
    }
  });
});

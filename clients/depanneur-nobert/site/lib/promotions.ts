import promotionsData from '@/data/promotions.json';
import type { Promotion } from '@/types';

export function getActivePromotions(): Promotion[] {
  const now = new Date();
  return (promotionsData as Promotion[])
    .filter((promo) => {
      const start = new Date(promo.validFrom);
      const end = new Date(promo.validUntil);
      return start <= now && now <= end;
    })
    .sort((a, b) => new Date(a.validUntil).getTime() - new Date(b.validUntil).getTime());
}

export function getTopPromotions(limit = 3): Promotion[] {
  return getActivePromotions().slice(0, limit);
}

export function getLastUpdate(): string {
  const promos = promotionsData as Promotion[];
  if (promos.length === 0) return new Date().toISOString().slice(0, 10);
  const latest = promos
    .map((p) => p.validFrom)
    .sort()
    .reverse()[0];
  return latest ?? new Date().toISOString().slice(0, 10);
}

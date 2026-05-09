import promotionsData from '@/site/data/promotions.json';
import type { Promotion } from '@/types/promotion';

export function getPromotions(): Promotion[] {
  const items = (promotionsData as { promotions: Promotion[] }).promotions;
  return [...items].sort((a, b) => {
    const aFrom = new Date(a.validFrom).getTime();
    const bFrom = new Date(b.validFrom).getTime();
    return bFrom - aFrom;
  });
}

export function getActivePromotions(now: Date = new Date()): Promotion[] {
  return getPromotions().filter((p) => {
    const start = new Date(p.validFrom);
    const end = new Date(p.validTo);
    return start <= now && now <= end;
  });
}

export function getTopPromotions(count: number = 3): Promotion[] {
  return getActivePromotions().slice(0, count);
}

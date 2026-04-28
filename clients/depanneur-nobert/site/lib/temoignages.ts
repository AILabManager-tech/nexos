import temoignagesData from '@/data/temoignages.json';
import type { Temoignage } from '@/types';

export function getTemoignages(): Temoignage[] {
  return temoignagesData as Temoignage[];
}

import horairesData from '@/data/horaires.json';
import type { HoraireJour, Horaires } from '@/types';

export function getHoraires(): Horaires {
  return horairesData as Horaires;
}

export function getRegularHoraires(): HoraireJour[] {
  return getHoraires().regular;
}

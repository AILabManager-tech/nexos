'use client';

import { useEffect, useReducer } from 'react';
import { useTranslations } from 'next-intl';

// P10 — Démo interactive DANS le hero (ref S17 Monday.com).
// Kanban animé : 6 cartes réparties sur 3 colonnes, une carte avance à la colonne suivante
// toutes les 3500 ms. Boucle cyclique : done → todo.
//
// Garde-fous accessibilité (anti-patterns P10) :
// - `role="img"` + `aria-label` traduit → l'animation est annoncée comme image équivalente.
// - `prefers-reduced-motion` honoré → animation arrêtée (pas seulement ralentie), état statique
//   reste lisible et non-trompeur.
// - Pas de données client réelles : noms de clients fictifs (CPL, FDV, BH, NRN, CNC, SSR).
// - Cleanup du setInterval au démontage.
// - Pas de dépendance Framer Motion → bundle propre (CSS transitions + tailwind keyframes).

type ColumnId = 'todo' | 'doing' | 'done';
const COLUMN_ORDER: readonly ColumnId[] = ['todo', 'doing', 'done'] as const;
type CardId = 'c1' | 'c2' | 'c3' | 'c4' | 'c5' | 'c6';

type Card = {
  id: CardId;
  column: ColumnId;
};

const INITIAL_STATE: Card[] = [
  { id: 'c1', column: 'done' },
  { id: 'c2', column: 'doing' },
  { id: 'c3', column: 'doing' },
  { id: 'c4', column: 'todo' },
  { id: 'c5', column: 'todo' },
  { id: 'c6', column: 'todo' }
];

function advance(state: Card[]): Card[] {
  // Prend la première carte en `done`, la réenvoie en `todo`.
  // Puis avance une carte par colonne : todo→doing, doing→done.
  // Évite l'effet "grosse vague" — une seule carte bouge par tick.
  const indexInDone = state.findIndex((c) => c.column === 'done');
  if (indexInDone === -1) return state;

  // On déplace UNE carte par tick, cycliquement : on prend la carte la plus à gauche
  // dans la colonne la plus à droite, et on la fait avancer d'un cran (en bouclant).
  const cycle: ColumnId[] = ['done', 'doing', 'todo'];
  for (const fromCol of cycle) {
    const idx = state.findIndex((c) => c.column === fromCol);
    if (idx !== -1) {
      const fromColIdx = COLUMN_ORDER.indexOf(fromCol);
      const nextColIdx = (fromColIdx + 1) % COLUMN_ORDER.length;
      const nextCol = COLUMN_ORDER[nextColIdx]!;
      return state.map((c, i) => (i === idx ? { ...c, column: nextCol } : c));
    }
  }
  return state;
}

type Action = { type: 'advance' };

function reducer(state: Card[], action: Action): Card[] {
  switch (action.type) {
    case 'advance':
      return advance(state);
  }
}

export function InteractiveDemo() {
  const t = useTranslations('home.demo');
  const [cards, dispatch] = useReducer(reducer, INITIAL_STATE);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (media.matches) return;

    const id = window.setInterval(() => dispatch({ type: 'advance' }), 3500);
    return () => window.clearInterval(id);
  }, []);

  const byColumn: Record<ColumnId, Card[]> = {
    todo: cards.filter((c) => c.column === 'todo'),
    doing: cards.filter((c) => c.column === 'doing'),
    done: cards.filter((c) => c.column === 'done')
  };

  return (
    <div
      role="img"
      aria-label={t('aria_label')}
      className="relative rounded-xl border border-surface-raised bg-surface-alt p-4 shadow-2xl shadow-accent/5"
    >
      <div className="flex items-center justify-between pb-3 border-b border-surface-raised">
        <div>
          <p className="font-display text-sm font-bold text-ink">{t('caption_title')}</p>
          <p className="text-xs text-ink-muted">{t('caption_subtitle')}</p>
        </div>
        <div className="flex gap-1.5" aria-hidden="true">
          <span className="h-2.5 w-2.5 rounded-full bg-kpi-warning/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-kpi-success/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-accent/70" />
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3">
        {COLUMN_ORDER.map((col) => (
          <div key={col} className="flex flex-col gap-2">
            <p className="text-[10px] uppercase tracking-widest text-ink-muted font-medium">
              {t(`columns.${col}`)}
              <span className="ml-1.5 text-ink-soft">· {byColumn[col].length}</span>
            </p>
            <ul className="flex flex-col gap-2 min-h-[12rem]">
              {byColumn[col].map((card) => (
                <li
                  key={card.id}
                  className="rounded-md border border-surface-raised bg-surface p-2.5 text-xs transition-all duration-500 animate-kanban-advance"
                >
                  <p className="font-medium text-ink leading-tight line-clamp-2">
                    {t(`cards.${card.id}.title`)}
                  </p>
                  <div className="mt-2 flex items-center justify-between">
                    <span className="text-[10px] font-mono text-ink-muted">
                      {t(`cards.${card.id}.client`)}
                    </span>
                    <span
                      className={`text-[10px] font-mono font-bold ${
                        col === 'done' ? 'text-kpi-success' : 'text-accent-soft'
                      }`}
                    >
                      {t(`cards.${card.id}.margin`)}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 border-t border-surface-raised pt-3">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-ink-muted">{t('kpi.margin_label')}</p>
          <p className="font-display text-2xl font-bold text-kpi-success">{t('kpi.margin_value')}</p>
          <p className="text-[10px] text-ink-muted">{t('kpi.margin_note')}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-widest text-ink-muted">{t('kpi.hours_label')}</p>
          <p className="font-display text-2xl font-bold text-accent-soft">{t('kpi.hours_value')}</p>
          <p className="text-[10px] text-ink-muted">{t('kpi.hours_note')}</p>
        </div>
      </div>
    </div>
  );
}

import { useTranslations } from 'next-intl';

// P19 StoryBrand étape "Problème reconnu" — le client se reconnaît dans le problème
// AVANT qu'on présente la solution. Reformulation directe : projets qui perdent de
// l'argent sans que personne ne le voie. Appuyé par une stat crédible (33%).
// 3 modes d'échec exposés → le lecteur se cale sur celui qu'il vit.
export function ProblemSolution() {
  const t = useTranslations('home.problem');

  const failures = ['f1', 'f2', 'f3'] as const;

  return (
    <section
      id="problem"
      className="border-b border-surface-raised bg-surface-alt py-20 md:py-28"
    >
      <div className="mx-auto max-w-7xl px-6 grid gap-16 md:grid-cols-[1fr,1.2fr] md:items-start">
        <div className="md:sticky md:top-28">
          <p className="text-xs uppercase tracking-widest text-accent-soft font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
          <p className="mt-6 max-w-prose text-ink-soft leading-relaxed">{t('body')}</p>

          <div className="mt-10 rounded-xl border border-surface-raised bg-surface p-6">
            <p className="font-display text-5xl font-bold text-kpi-warning">
              {t('proof_stat')}
            </p>
            <p className="mt-2 text-sm text-ink-soft max-w-prose">{t('proof_caption')}</p>
          </div>
        </div>

        <ul className="space-y-6">
          {failures.map((f) => (
            <li
              key={f}
              className="rounded-xl border border-surface-raised bg-surface p-6 md:p-8"
            >
              <p className="font-display text-xl font-bold text-ink">{t(`failures.${f}.title`)}</p>
              <p className="mt-3 text-ink-soft leading-relaxed">{t(`failures.${f}.body`)}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

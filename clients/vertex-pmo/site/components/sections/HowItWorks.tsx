import { useTranslations } from 'next-intl';

// P19 StoryBrand étape "Plan clair" — 3 étapes, pas 10 (anti-pattern "plan en 10 étapes" listé
// dans pattern-matrix.json P19). Structure : Connecter → Visualiser → Agir.
// Clôture avec "Résultat attendu" métrique (+12 %) aligné P19 "résultat promis concret".
export function HowItWorks() {
  const t = useTranslations('home.howItWorks');
  const steps = ['s1', 's2', 's3'] as const;

  return (
    <section id="how" className="py-20 md:py-28">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-widest text-accent-soft font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
          <p className="mt-6 text-ink-soft leading-relaxed">{t('subtitle')}</p>
        </div>

        <ol className="mt-14 grid gap-6 md:grid-cols-3">
          {steps.map((step, idx) => (
            <li
              key={step}
              className="relative rounded-xl border border-surface-raised bg-surface-alt p-6 md:p-8"
            >
              <p className="font-mono text-sm text-accent-soft">{t(`steps.${step}.number`)}</p>
              <p className="mt-3 font-display text-2xl font-bold text-ink">
                {t(`steps.${step}.title`)}
              </p>
              <p className="mt-3 text-sm text-ink-soft leading-relaxed">
                {t(`steps.${step}.body`)}
              </p>
              {idx < steps.length - 1 && (
                <span
                  aria-hidden="true"
                  className="hidden md:block absolute top-1/2 -right-3 -translate-y-1/2 text-accent text-2xl"
                >
                  →
                </span>
              )}
            </li>
          ))}
        </ol>

        <div className="mt-14 rounded-xl border border-accent/30 bg-gradient-to-br from-surface-alt to-surface p-8 md:p-10 md:flex md:items-center md:justify-between md:gap-10">
          <div>
            <p className="text-xs uppercase tracking-widest text-accent-soft font-medium">
              {t('result_label')}
            </p>
            <p className="mt-2 font-display text-4xl md:text-5xl font-bold text-kpi-success">
              {t('result_value')}
            </p>
          </div>
          <p className="mt-4 md:mt-0 max-w-md text-sm text-ink-soft leading-relaxed">
            {t('result_note')}
          </p>
        </div>
      </div>
    </section>
  );
}

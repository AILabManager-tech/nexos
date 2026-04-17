import { useTranslations } from 'next-intl';
import { RevealOnScroll } from '@/components/atoms/RevealOnScroll';

// P14 rupture 3 — structure : liste éditoriale numérotée AU LIEU DE cards.
// Chaque expertise est une ligne en <article> avec numéro display serif, titre,
// description prose, séparateur border-top fin. Typographie porte le sens, pas
// des boîtes colorées standardisées. P17 léger : reveal en cascade via delayMs.
export function Expertises() {
  const t = useTranslations('home.expertises');
  const items = ['e1', 'e2', 'e3', 'e4', 'e5'] as const;

  return (
    <section id="expertises" className="bg-surface-alt border-b border-primary-100 py-20 md:py-28">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.18em] text-ink-muted font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
          <p className="mt-8 text-lg text-ink-soft leading-relaxed max-w-prose">
            {t('intro')}
          </p>
        </div>

        <ol className="mt-16 space-y-0 border-t border-primary-200">
          {items.map((item, idx) => (
            <RevealOnScroll key={item} delayMs={idx * 80}>
              <li>
                <article className="grid gap-6 md:grid-cols-12 md:items-baseline border-b border-primary-200 py-10 md:py-12">
                  <p className="md:col-span-2 font-display text-3xl md:text-4xl text-primary font-bold">
                    {t(`items.${item}.number`)}
                  </p>
                  <h3 className="md:col-span-4 font-display text-2xl md:text-3xl text-ink leading-tight">
                    {t(`items.${item}.title`)}
                  </h3>
                  <p className="md:col-span-6 text-ink-soft leading-relaxed max-w-prose">
                    {t(`items.${item}.body`)}
                  </p>
                </article>
              </li>
            </RevealOnScroll>
          ))}
        </ol>
      </div>
    </section>
  );
}

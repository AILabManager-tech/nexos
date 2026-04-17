import { useTranslations } from 'next-intl';
import { RevealOnScroll } from '@/components/atoms/RevealOnScroll';

// Section Approche — narrative éditoriale rédigée plutôt que bullet-list générique.
// Trois paragraphes révélés au scroll (P17 fade-in, pas grayscale ici — réservé aux photos).
// Largeur prose editorial pour respirer, pas de cards ni de boxes.
export function Approche() {
  const t = useTranslations('home.approche');

  return (
    <section id="approche" className="border-b border-primary-100 py-20 md:py-28">
      <div className="mx-auto max-w-4xl px-6">
        <RevealOnScroll>
          <p className="text-xs uppercase tracking-[0.18em] text-ink-muted font-medium">
            {t('eyebrow')}
          </p>
          <h2 className="mt-4 font-display text-4xl md:text-5xl font-bold text-ink leading-tight">
            {t('title')}
          </h2>
        </RevealOnScroll>

        <div className="mt-12 space-y-8 text-lg text-ink-soft leading-relaxed">
          <RevealOnScroll delayMs={100}>
            <p>{t('p1')}</p>
          </RevealOnScroll>
          <RevealOnScroll delayMs={200}>
            <p>{t('p2')}</p>
          </RevealOnScroll>
          <RevealOnScroll delayMs={300}>
            <p>{t('p3')}</p>
          </RevealOnScroll>
        </div>
      </div>
    </section>
  );
}

// Section: S-013 | produits.ProduitsHero | i18n: produits.hero
import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';

export function ProduitsHero() {
  const t = useTranslations('produits.hero');
  const tNav = useTranslations('produits.categoriesNav');

  const anchors: Array<{ key: 'bieres' | 'snacks' | 'lotto' | 'essentiels' }> = [
    { key: 'bieres' },
    { key: 'snacks' },
    { key: 'lotto' },
    { key: 'essentiels' },
  ];

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20 border-b border-border/60" aria-labelledby="prod-hero-title">
      <Container>
        <div className="max-w-3xl space-y-4">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h1 id="prod-hero-title" className="font-heading font-bold text-4xl sm:text-5xl text-text">
            {t('title')}
          </h1>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>
        <nav aria-label={t('anchorLabel')} className="mt-8">
          <ul className="flex flex-wrap gap-2">
            {anchors.map(({ key }) => (
              <li key={key}>
                <a
                  href={`#${key}`}
                  className="inline-flex items-center h-11 px-4 rounded-full border border-border bg-surface text-text font-semibold text-small hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary"
                >
                  {tNav(`items.${key}`)}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </Container>
    </section>
  );
}

// Section: S-009 | promotions.PromotionsHero | i18n: promotions.hero
import { useTranslations, useLocale } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { getLastUpdate } from '@/lib/promotions';
import type { Locale } from '@/i18n/routing';

export function PromotionsHero() {
  const t = useTranslations('promotions.hero');
  const locale = useLocale() as Locale;
  const lastUpdate = new Date(getLastUpdate()).toLocaleDateString(
    locale === 'fr' ? 'fr-CA' : 'en-CA',
    { year: 'numeric', month: 'long', day: 'numeric' }
  );

  return (
    <section className="bg-background py-12 sm:py-16 lg:py-20 border-b border-border/60" aria-labelledby="promo-hero-title">
      <Container>
        <div className="max-w-3xl space-y-4">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h1 id="promo-hero-title" className="font-heading font-bold text-4xl sm:text-5xl text-text">
            {t('title')}
          </h1>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
          <p className="text-small text-text-muted">{t('lastUpdate', { date: lastUpdate })}</p>
        </div>
      </Container>
    </section>
  );
}

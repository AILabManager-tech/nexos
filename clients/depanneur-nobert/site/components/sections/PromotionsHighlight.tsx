// Section: S-002 | home.PromotionsHighlight | i18n: home.promotionsHighlight
import { useTranslations, useLocale } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ArrowRight } from 'lucide-react';
import { getTopPromotions } from '@/lib/promotions';
import type { Locale } from '@/i18n/routing';

const dateFmt: Record<Locale, Intl.DateTimeFormatOptions> = {
  fr: { day: 'numeric', month: 'long' },
  en: { month: 'long', day: 'numeric' },
};

export function PromotionsHighlight() {
  const t = useTranslations('home.promotionsHighlight');
  const locale = useLocale() as Locale;
  const promotions = getTopPromotions(3);

  return (
    <section className="bg-surface py-12 sm:py-16 lg:py-20" aria-labelledby="promo-highlight-title">
      <Container>
        <div className="max-w-3xl space-y-3">
          <p className="text-small uppercase tracking-wider text-primary font-semibold">
            {t('eyebrow')}
          </p>
          <h2 id="promo-highlight-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
            {t('title')}
          </h2>
          <p className="text-lg text-text-muted">{t('subtitle')}</p>
        </div>

        {promotions.length === 0 ? (
          <p className="mt-10 text-text-muted">{t('emptyState')}</p>
        ) : (
          <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {promotions.map((promo) => {
              const validUntil = new Date(promo.validUntil).toLocaleDateString(
                locale === 'fr' ? 'fr-CA' : 'en-CA',
                dateFmt[locale]
              );
              return (
                <li key={promo.id}>
                  <Card className="h-full flex flex-col gap-4">
                    <Badge variant="accent">{t('badgeLabel')}</Badge>
                    <h3 className="font-heading font-bold text-xl text-text">
                      {promo.title[locale]}
                    </h3>
                    {promo.regularPrice && promo.promoPrice && (
                      <p className="text-text">
                        <span className="line-through text-text-muted mr-2">
                          {promo.regularPrice.toFixed(2)} $
                        </span>
                        <span className="font-bold text-2xl text-primary">
                          {promo.promoPrice.toFixed(2)} $
                        </span>
                      </p>
                    )}
                    <p className="text-small text-text-muted mt-auto">
                      {t('validUntil', { date: validUntil })}
                    </p>
                  </Card>
                </li>
              );
            })}
          </ul>
        )}

        <div className="mt-10">
          <Link
            href="/promotions"
            className="inline-flex items-center gap-2 text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
          >
            {t('ctaAll')}
            <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </section>
  );
}

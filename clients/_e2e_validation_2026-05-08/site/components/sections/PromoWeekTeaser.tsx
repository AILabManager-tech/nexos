import { ArrowRight } from 'lucide-react';
import Image from 'next/image';
import { useLocale, useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Badge } from '@/components/ui/Badge';
import { Card } from '@/components/ui/Card';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { formatDate, formatPrice } from '@/lib/format';
import { getTopPromotions } from '@/lib/promotions';

export function PromoWeekTeaser() {
  const t = useTranslations('home.promoTeaser');
  const locale = useLocale();
  const promos = getTopPromotions(3);

  if (promos.length === 0) return null;

  return (
    <Section alt data-manifest-id="S-002">
      <Container>
        <div className="mb-8 flex flex-col gap-2">
          <span className="text-sm font-semibold uppercase tracking-wide text-primary">
            {t('eyebrow')}
          </span>
          <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
          <p className="max-w-prose text-text-muted">{t('subtitle')}</p>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {promos.map((p) => {
            const title = locale === 'en' ? p.title_en : p.title_fr;
            const alt = locale === 'en' ? p.alt_en : p.alt_fr;
            const savings = p.priceBefore - p.priceAfter;
            return (
              <Card key={p.id} className="flex flex-col gap-3">
                <div className="relative aspect-[4/3] overflow-hidden rounded bg-surface-alt">
                  <Image
                    src={p.image}
                    alt={alt}
                    fill
                    sizes="(min-width: 768px) 33vw, 100vw"
                    className="object-cover"
                  />
                  <Badge className="absolute left-3 top-3">
                    {t('savingsLabel', { amount: formatPrice(savings, locale) })}
                  </Badge>
                </div>
                <h3 className="font-heading text-h3 text-text">{title}</h3>
                <div className="flex items-baseline gap-3">
                  <span className="text-sm text-text-muted line-through">
                    {formatPrice(p.priceBefore, locale)}
                  </span>
                  <span className="text-2xl font-extrabold text-primary">
                    {formatPrice(p.priceAfter, locale)}
                  </span>
                </div>
                <p className="text-xs text-text-muted">
                  {t('validityLabel', { dateEnd: formatDate(p.validTo, locale) })}
                </p>
              </Card>
            );
          })}
        </div>

        <div className="mt-8 flex justify-center">
          <Link
            href="/promotions"
            className="inline-flex min-h-[48px] items-center gap-2 rounded bg-primary px-6 py-3 text-base font-semibold text-primary-foreground hover:bg-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
          >
            {t('ctaAllPromos')}
            <ArrowRight size={20} aria-hidden="true" />
          </Link>
        </div>
      </Container>
    </Section>
  );
}

import { useLocale, useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { formatDate } from '@/lib/format';
import promotions from '@/site/data/promotions.json';

export function HeroPromoWeek() {
  const t = useTranslations('promotions.hero');
  const locale = useLocale();
  const range = (promotions as { weekRange: { from: string; to: string } }).weekRange;

  return (
    <section data-manifest-id="S-007" className="bg-background py-12 sm:py-16 lg:py-20">
      <Container>
        <h1 className="font-heading text-h1 text-primary">{t('title')}</h1>
        <p className="mt-4 max-w-prose text-lg text-text">{t('subtitle')}</p>
        <p className="mt-2 inline-flex items-center rounded-full bg-accent px-4 py-1 text-sm font-semibold text-accent-foreground">
          {t('validityLabel', {
            dateStart: formatDate(range.from, locale),
            dateEnd: formatDate(range.to, locale),
          })}
        </p>
      </Container>
    </section>
  );
}

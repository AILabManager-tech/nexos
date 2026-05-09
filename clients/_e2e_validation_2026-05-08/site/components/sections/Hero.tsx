import { ArrowRight, MapPin } from 'lucide-react';
import Image from 'next/image';
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';

export function Hero() {
  const t = useTranslations('home.hero');
  return (
    <section
      data-manifest-id="S-001"
      className="relative overflow-hidden bg-background pt-12 pb-16 lg:pt-20 lg:pb-24"
    >
      <Container className="grid gap-10 lg:grid-cols-2 lg:items-center">
        <div className="flex flex-col gap-6">
          <h1 className="font-heading text-h1 leading-tight text-primary">
            {t('title')}
          </h1>
          <p className="max-w-prose text-lg text-text">{t('subtitle')}</p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/promotions"
              className="inline-flex min-h-[48px] items-center gap-2 rounded bg-primary px-6 py-3 text-base font-semibold text-primary-foreground hover:bg-primary-hover focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              {t('ctaPrimary')}
              <ArrowRight size={20} aria-hidden="true" />
            </Link>
            <Link
              href="/contact"
              className="inline-flex min-h-[48px] items-center gap-2 rounded border border-border-strong px-6 py-3 text-base font-semibold text-primary hover:bg-surface-alt focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
            >
              <MapPin size={20} aria-hidden="true" />
              {t('ctaSecondary')}
            </Link>
          </div>
        </div>
        <div className="relative aspect-[4/3] overflow-hidden rounded-lg border border-border bg-surface-alt lg:aspect-[21/9]">
          <Image
            src="/images/hero-nobert.jpg"
            alt={t('imageAlt')}
            fill
            sizes="(min-width: 1024px) 50vw, 100vw"
            className="object-cover"
            priority
          />
        </div>
      </Container>
    </section>
  );
}

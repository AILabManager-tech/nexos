// Section: S-001 | home.Hero | i18n: home.hero
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { ArrowRight, MapPin } from 'lucide-react';
import { getClientConfig } from '@/lib/clientConfig';

export function Hero() {
  const t = useTranslations('home.hero');
  const { ville, city } = getClientConfig();

  return (
    <section
      className="bg-background py-16 sm:py-20 lg:py-28 border-b border-border/60"
      aria-labelledby="hero-title"
    >
      <Container>
        <div className="grid items-center gap-10 lg:gap-16 lg:grid-cols-[3fr_2fr]">
          <div className="space-y-6">
            <p className="text-small uppercase tracking-wider text-primary font-semibold">
              {t('eyebrow', { ville, city })}
            </p>
            <h1
              id="hero-title"
              className="font-heading font-bold text-4xl sm:text-5xl text-text leading-tight"
            >
              {t('title', { ville, city })}
            </h1>
            <p className="text-lg text-text-muted max-w-2xl">{t('subtitle')}</p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/promotions"
                aria-label={t('ctaPrimaryAria')}
                className="inline-flex items-center justify-center gap-2 h-14 px-7 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                {t('ctaPrimary')}
                <ArrowRight size={18} aria-hidden="true" />
              </Link>
              <Link
                href="/contact"
                aria-label={t('ctaSecondaryAria')}
                className="inline-flex items-center justify-center gap-2 h-14 px-7 rounded font-semibold border border-primary text-primary bg-surface hover:bg-primary-subtle focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
              >
                <MapPin size={18} aria-hidden="true" />
                {t('ctaSecondary')}
              </Link>
            </div>
            <p className="text-small text-text-muted pt-2">{t('trustNote')}</p>
          </div>
          <div className="relative aspect-[4/3] rounded-lg overflow-hidden bg-primary-subtle/40 border border-border">
            <div className="absolute inset-0 flex items-center justify-center text-center px-6">
              <p className="text-small text-text-muted italic">
                {t('imageAlt', { ville, city })}
              </p>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}

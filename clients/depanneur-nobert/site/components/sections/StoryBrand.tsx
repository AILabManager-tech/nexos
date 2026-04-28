// Section: S-006 | home.StoryBrand | i18n: home.storyBrand
import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { ArrowRight } from 'lucide-react';
import { getClientConfig } from '@/lib/clientConfig';

export function StoryBrand() {
  const t = useTranslations('home.storyBrand');
  const { ville, city, anneeFondation } = getClientConfig();

  return (
    <section className="bg-surface py-12 sm:py-16 lg:py-20" aria-labelledby="story-title">
      <Container>
        <div className="grid gap-10 lg:grid-cols-[2fr_3fr] items-start">
          <div className="aspect-[4/5] rounded-lg overflow-hidden bg-primary-subtle/40 border border-border flex items-center justify-center px-6 py-10">
            <p className="text-small text-text-muted italic text-center">
              {t('imageAlt', { ville, city })}
            </p>
          </div>
          <div className="space-y-5">
            <p className="text-small uppercase tracking-wider text-primary font-semibold">
              {t('eyebrow')}
            </p>
            <h2 id="story-title" className="font-heading font-bold text-3xl sm:text-4xl text-text">
              {t('title')}
            </h2>
            <p className="text-lg text-text leading-relaxed">{t('paragraphHero')}</p>
            <p className="text-lg text-text leading-relaxed">
              {t('paragraphGuide', { anneeFondation })}
            </p>
            <p className="text-lg text-text leading-relaxed">{t('paragraphPromise')}</p>
            <Link
              href="/promotions"
              className="inline-flex items-center gap-2 text-primary font-semibold hover:underline focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary rounded"
            >
              {t('ctaPromotions')}
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </Container>
    </section>
  );
}

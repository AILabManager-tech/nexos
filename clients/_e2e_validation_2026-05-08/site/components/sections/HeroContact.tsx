import { useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';

export function HeroContact() {
  const t = useTranslations('contact.hero');
  return (
    <section
      data-manifest-id="S-012"
      className="bg-background py-12 sm:py-16 lg:py-20"
    >
      <Container>
        <h1 className="font-heading text-h1 text-primary">{t('title')}</h1>
        <p className="mt-4 max-w-prose text-lg text-text">{t('subtitle')}</p>
      </Container>
    </section>
  );
}

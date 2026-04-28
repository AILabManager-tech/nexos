import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';
import { ArrowLeft } from 'lucide-react';

export default function NotFound() {
  const t = useTranslations('common.errors');
  return (
    <section className="bg-background py-20 sm:py-28" aria-labelledby="nf-title">
      <Container className="max-w-2xl text-center space-y-6">
        <h1 id="nf-title" className="font-heading font-bold text-4xl text-text">
          {t('notFoundTitle')}
        </h1>
        <p className="text-lg text-text-muted">{t('notFoundBody')}</p>
        <Link
          href="/"
          className="inline-flex items-center justify-center gap-2 h-12 px-6 rounded font-semibold bg-primary text-primary-foreground hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2"
        >
          <ArrowLeft size={18} aria-hidden="true" />
          {t('notFoundCta')}
        </Link>
      </Container>
    </section>
  );
}

import { useTranslations } from 'next-intl';
import { Link } from '@/i18n/routing';
import { Container } from '@/components/ui/Container';

export default function NotFound() {
  const t = useTranslations('common.errors');
  return (
    <Container className="py-20 text-center">
      <h1 className="font-heading text-h1 text-primary">{t('notFoundTitle')}</h1>
      <p className="mt-4 text-text-muted">{t('notFoundDescription')}</p>
      <Link
        href="/"
        className="mt-6 inline-flex min-h-[48px] items-center rounded bg-primary px-6 py-3 text-primary-foreground"
      >
        {t('notFoundCta')}
      </Link>
    </Container>
  );
}

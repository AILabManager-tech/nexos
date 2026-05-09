import { useTranslations } from 'next-intl';

export function SkipToContent() {
  const t = useTranslations('common.nav');
  return (
    <a href="#main" className="skip-link sr-only focus:not-sr-only">
      {t('skipToContent')}
    </a>
  );
}

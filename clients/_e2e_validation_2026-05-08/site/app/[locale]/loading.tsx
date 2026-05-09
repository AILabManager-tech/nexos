import { useTranslations } from 'next-intl';

export default function Loading() {
  return (
    <div
      role="status"
      aria-busy="true"
      className="flex min-h-[40vh] items-center justify-center"
    >
      <LoadingLabel />
    </div>
  );
}

function LoadingLabel() {
  const t = useTranslations('common.loading');
  return <span className="text-text-muted">{t('label')}</span>;
}

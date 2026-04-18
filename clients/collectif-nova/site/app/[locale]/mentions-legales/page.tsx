import { useTranslations } from 'next-intl';
import { setRequestLocale } from 'next-intl/server';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function LegalMentionsPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  return <LegalContent />;
}

function LegalContent() {
  const t = useTranslations('legal.mentions');

  const rows: Array<[string, string]> = [
    [t('neq_label'), t('neq_value')],
    [t('address_label'), t('address_value')],
    [t('phone_label'), t('phone_value')],
    [t('email_label'), t('email_value')],
    [t('host_label'), t('host_value')]
  ];

  return (
    <article className="mx-auto max-w-prose px-6 py-24">
      <h1 className="text-4xl md:text-5xl">{t('title')}</h1>
      <p className="mt-6 text-xl font-heading">{t('company')}</p>

      <dl className="mt-10 divide-y divide-primary-100">
        {rows.map(([label, value]) => (
          <div key={label} className="grid grid-cols-1 md:grid-cols-3 gap-2 py-4">
            <dt className="text-sm uppercase tracking-widest text-ink-muted">{label}</dt>
            <dd className="md:col-span-2">{value}</dd>
          </div>
        ))}
      </dl>
    </article>
  );
}

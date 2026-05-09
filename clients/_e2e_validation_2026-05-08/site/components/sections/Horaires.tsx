import { useLocale, useTranslations } from 'next-intl';
import { Container } from '@/components/ui/Container';
import { Section } from '@/components/ui/Section';
import { getHours } from '@/lib/site-info';

export function Horaires() {
  const t = useTranslations('contact.horaires');
  const locale = useLocale();
  const hours = getHours();

  return (
    <Section data-manifest-id="S-014">
      <Container>
        <h2 className="font-heading text-h2 text-text">{t('title')}</h2>
        <p className="mt-2 max-w-prose text-text-muted">{t('subtitle')}</p>

        <table className="mt-6 w-full max-w-md border-collapse text-left">
          <caption className="sr-only">{t('title')}</caption>
          <tbody>
            {hours.weekly.map((d) => (
              <tr key={d.day} className="border-b border-border last:border-0">
                <th
                  scope="row"
                  className="py-2 pr-4 font-semibold text-text"
                >
                  {t(`days.${d.day}`)}
                </th>
                <td className="py-2 text-text-muted">
                  {d.closed ? (
                    <span className="font-semibold text-error">
                      {t('closedLabel')}
                    </span>
                  ) : (
                    <span>
                      {d.open} – {d.close}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <h3 className="mt-8 font-heading text-xl font-bold text-text">
          {t('holidaysTitle')}
        </h3>
        <p className="mt-2 max-w-prose text-text-muted">{t('holidaysNote')}</p>
        <ul className="mt-4 space-y-1 text-sm text-text-muted">
          {hours.holidays.map((h) => (
            <li key={h.date}>
              {h.date} —{' '}
              <span className="font-semibold text-text">
                {locale === 'en' ? h.name_en : h.name_fr}
              </span>
              {h.closed && <span> ({t('closedLabel').toLowerCase()})</span>}
            </li>
          ))}
        </ul>
      </Container>
    </Section>
  );
}

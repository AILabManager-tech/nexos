import { useTranslations } from 'next-intl';
import { getRegularHoraires } from '@/lib/horaires';

interface HoursTableProps {
  caption?: string;
}

export function HoursTable({ caption }: HoursTableProps) {
  const t = useTranslations('common.schedule');
  const tContact = useTranslations('contact.coordonnees');
  const horaires = getRegularHoraires();

  return (
    <table className="w-full border-collapse text-base">
      <caption className="sr-only">
        {caption ?? tContact('hoursTableCaption')}
      </caption>
      <thead>
        <tr className="border-b border-border">
          <th scope="col" className="text-left py-2 pr-4 font-semibold text-text">
            {tContact('hoursColumnDay')}
          </th>
          <th scope="col" className="text-left py-2 font-semibold text-text">
            {tContact('hoursColumnHours')}
          </th>
        </tr>
      </thead>
      <tbody>
        {horaires.map((h) => (
          <tr key={h.day} className="border-b border-border/60 last:border-0">
            <th scope="row" className="text-left py-2 pr-4 font-normal text-text">
              {t(h.day)}
            </th>
            <td className="py-2 text-text-muted">
              {h.closed ? t('closed') : `${h.open} – ${h.close}`}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

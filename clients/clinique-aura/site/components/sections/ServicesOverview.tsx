import { useTranslations } from 'next-intl';
import { Activity, Heart, Sparkles, type LucideIcon } from 'lucide-react';

type ServiceKey = 'physio' | 'osteo' | 'massage';

const ICONS: Record<ServiceKey, LucideIcon> = {
  physio: Activity,
  osteo: Heart,
  massage: Sparkles
};

export function ServicesOverview() {
  const t = useTranslations('home.services');
  const keys: ServiceKey[] = ['physio', 'osteo', 'massage'];

  return (
    <section id="services" aria-labelledby="services-heading" className="bg-surface-alt">
      <div className="mx-auto max-w-7xl px-6 py-24">
        <div className="max-w-2xl">
          <p className="text-sm uppercase tracking-widest text-primary">
            {t('eyebrow')}
          </p>
          <h2 id="services-heading" className="mt-4 text-3xl md:text-5xl">
            {t('title')}
          </h2>
          <p className="mt-4 text-ink-soft">{t('subtitle')}</p>
        </div>

        <ul className="mt-16 grid gap-8 md:grid-cols-3">
          {keys.map((key) => {
            const Icon = ICONS[key];
            return (
              <li
                key={key}
                className="rounded-3xl bg-surface p-8 shadow-sm ring-1 ring-primary-100"
              >
                <Icon aria-hidden="true" className="h-8 w-8 text-primary" />
                <h3 className="mt-6 text-2xl">{t(`items.${key}.title`)}</h3>
                <p className="mt-3 text-ink-soft">{t(`items.${key}.description`)}</p>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}

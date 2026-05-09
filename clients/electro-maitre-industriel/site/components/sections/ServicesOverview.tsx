import { useTranslations } from 'next-intl';
import { Cpu, Factory, Wrench, Phone, type LucideIcon } from 'lucide-react';

type ServiceKey = 'industrial' | 'automation' | 'maintenance' | 'emergency';

const ICONS: Record<ServiceKey, LucideIcon> = {
  industrial: Factory,
  automation: Cpu,
  maintenance: Wrench,
  emergency: Phone
};

/**
 * Grid 4 colonnes (industrial / automation / maintenance / emergency).
 * Cards sans rounded (mécanique), bordure top primary 2px, icônes accent or.
 * I18n : `home.services.items.<key>.{title,description}`.
 */
export function ServicesOverview() {
  const t = useTranslations('home.services');
  const keys: ServiceKey[] = ['industrial', 'automation', 'maintenance', 'emergency'];

  return (
    <section id="services" aria-labelledby="services-heading" className="bg-surface-alt">
      <div className="mx-auto max-w-7xl px-6 py-24">
        <div className="max-w-2xl">
          <p className="text-sm uppercase tracking-[0.3em] text-accent">
            {t('eyebrow')}
          </p>
          <h2 id="services-heading" className="mt-4 text-3xl md:text-5xl">
            {t('title')}
          </h2>
          <p className="mt-4 text-ink-soft">{t('subtitle')}</p>
        </div>

        <ul className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {keys.map((key) => {
            const Icon = ICONS[key];
            return (
              <li
                key={key}
                className="border-t-2 border-primary bg-surface p-8"
              >
                <Icon aria-hidden="true" className="h-8 w-8 text-accent" />
                <h3 className="mt-6 text-xl">{t(`items.${key}.title`)}</h3>
                <p className="mt-3 text-sm text-ink-soft">{t(`items.${key}.description`)}</p>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}

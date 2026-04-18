import { useTranslations } from 'next-intl';

export function Services() {
  const t = useTranslations('services');

  const items = [
    { id: 1, key: 'item1' },
    { id: 2, key: 'item2' },
    { id: 3, key: 'item3' },
    { id: 4, key: 'item4' }
  ];

  return (
    <section data-section="services" className="min-h-screen flex items-center py-20 px-6">
      <div className="max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold mb-12" style={{ fontFamily: 'var(--font-serif)' }}>
          {t('title')}
        </h2>
        <div className="grid md:grid-cols-2 gap-8">
          {items.map((item, idx) => (
            <div key={idx} className="stagger-item p-6 border-l-4" style={{ borderColor: 'var(--section-accent)' }}>
              <h3 className="text-xl font-bold mb-3" style={{ fontFamily: 'var(--font-serif)' }}>
                {t(`${item.key}.title`)}
              </h3>
              <p className="opacity-90">
                {t(`${item.key}.desc`)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

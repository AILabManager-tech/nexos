import { useTranslations } from 'next-intl';

export function Hero() {
  const t = useTranslations('hero');

  return (
    <section data-section="hero" className="min-h-screen flex items-center justify-center px-6 py-20">
      <div className="max-w-3xl text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6" style={{ fontFamily: 'var(--font-display)' }}>
          {t('title')}
        </h1>
        <p className="text-lg md:text-xl mb-8 opacity-90">
          {t('subtitle')}
        </p>
        <button className="px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition">
          {t('cta')}
        </button>
      </div>
    </section>
  );
}

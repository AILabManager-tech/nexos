import { useTranslations } from 'next-intl';
import Link from 'next/link';

export function Footer() {
  const t = useTranslations('footer');

  return (
    <footer className="bg-black/50 border-t border-white/10 py-12 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="font-bold mb-4">Collectif Nova</h3>
            <p className="opacity-60 text-sm">{t('tagline')}</p>
          </div>
          <div>
            <h4 className="font-bold mb-4">{t('quicklinks')}</h4>
            <nav className="space-y-2 text-sm">
              <Link href="/" className="block opacity-60 hover:opacity-100 transition">
                {t('home')}
              </Link>
              <Link href="/" className="block opacity-60 hover:opacity-100 transition">
                {t('projects')}
              </Link>
              <Link href="/" className="block opacity-60 hover:opacity-100 transition">
                {t('contact')}
              </Link>
            </nav>
          </div>
          <div>
            <h4 className="font-bold mb-4">{t('legal')}</h4>
            <nav className="space-y-2 text-sm">
              <Link href="/politique-confidentialite" className="block opacity-60 hover:opacity-100 transition">
                {t('privacy')}
              </Link>
              <Link href="/mentions-legales" className="block opacity-60 hover:opacity-100 transition">
                {t('mentions')}
              </Link>
            </nav>
          </div>
        </div>
        <div className="border-t border-white/10 pt-8 text-center opacity-50 text-sm">
          <p>© 2026 Collectif Nova. {t('rights')}</p>
        </div>
      </div>
    </footer>
  );
}

import { Link } from '@/i18n/routing';

export default function NotFound() {
  return (
    <section className="mx-auto max-w-prose px-6 py-32 text-center">
      <p className="text-sm uppercase tracking-widest text-ink-muted">404</p>
      <h1 className="mt-4 text-4xl md:text-5xl">Page introuvable</h1>
      <p className="mt-4 text-ink-soft">
        Le lien que vous avez suivi n&apos;existe pas ou a été déplacé.
      </p>
      <Link
        href="/"
        className="mt-8 inline-block rounded-full bg-primary px-6 py-3 text-surface hover:bg-primary-600 transition-colors"
      >
        Retour à l&apos;accueil
      </Link>
    </section>
  );
}

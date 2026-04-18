import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Dépanneur Nobert | Ton dépanneur. Ton quartier.',
  description: 'Commerce de proximité authentique — provisions, snacks, loterie.',
  openGraph: {
    type: 'website',
    locale: 'fr_CA',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body className="bg-white text-gray-900 font-sans">
        {children}
      </body>
    </html>
  );
}

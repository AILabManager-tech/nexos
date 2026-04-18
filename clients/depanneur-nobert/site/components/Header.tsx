'use client';

import Link from 'next/link';
import { MapPin, Phone } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-amber-900 text-white border-b-4 border-amber-700 sticky top-0 z-40 shadow-lg">
      <div className="max-w-5xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="group">
            <div className="text-3xl font-bold tracking-tight">
              DÉPANNEUR<br />
              <span className="text-amber-200 text-2xl">NOBERT</span>
            </div>
            <p className="text-amber-100 text-xs mt-1 group-hover:text-white transition">
              Ton quartier. Authentique.
            </p>
          </Link>

          <nav className="flex gap-8 items-center">
            <Link href="#produits" className="hover:text-amber-200 transition font-medium">
              Produits
            </Link>
            <Link href="#nous" className="hover:text-amber-200 transition font-medium">
              Qui sommes-nous
            </Link>
            <div className="flex items-center gap-2">
              <Phone className="w-4 h-4" />
              <a href="tel:+14165551234" className="font-bold">
                (416) 555-1234
              </a>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
}

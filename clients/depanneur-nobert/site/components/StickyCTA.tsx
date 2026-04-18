'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export default function StickyCTA() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-gradient-to-t from-amber-700 to-amber-600 text-white shadow-2xl p-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full max-w-2xl mx-auto flex items-center justify-between px-6 py-3 bg-white text-amber-900 font-bold rounded-lg hover:bg-amber-50 transition"
        aria-label="Voir les promotions de la semaine"
      >
        <span className="text-lg">📢 Voir les promotions de la semaine</span>
        <ChevronDown
          className={`w-5 h-5 transition ${isExpanded ? 'rotate-180' : ''}`}
        />
      </button>

      {isExpanded && (
        <div className="mt-3 max-w-2xl mx-auto bg-amber-800 rounded-lg p-4 space-y-2">
          <p className="text-sm text-amber-100">✨ Cette semaine :</p>
          <ul className="space-y-1 text-sm font-medium">
            <li>🛒 Bière Molson — 2 x 6 pour $15.99</li>
            <li>🍿 Chips Lay's — 3 sacs pour $5.49</li>
            <li>🎫 Billet Lotto-Québec — 1 gratuit pour 5 achetés</li>
          </ul>
        </div>
      )}
    </div>
  );
}

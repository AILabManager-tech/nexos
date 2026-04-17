'use client';

import { useEffect, useRef, useState } from 'react';

// P17 — Reveal on scroll via IntersectionObserver + CSS transitions.
// Garde-fous :
// - SSR-safe : rendu initial `opacity-100` si `as="server-visible"` (pas de flash contenu caché
//   chez l'utilisateur sans JS). Par défaut, l'élément démarre invisible et devient visible
//   à l'entrée en viewport (comportement client enrichi).
// - `prefers-reduced-motion` : visible immédiatement, pas d'observer attaché.
// - Pas de lib JS (Framer Motion, etc.) — IntersectionObserver natif.
// - Supporte le mode `grayscale` → couleur : image en N&B puis couleur révélée (P17 + P14).
type Props = {
  children: React.ReactNode;
  className?: string;
  /** Active le mode mono→couleur (grayscale → grayscale-0) en plus du fade-translate. */
  grayscale?: boolean;
  /** Threshold IntersectionObserver (0-1). 0.2 = 20% de l'élément visible. */
  threshold?: number;
  /** Délai avant apparition (ms). Permet d'échelonner des listes. */
  delayMs?: number;
};

export function RevealOnScroll({
  children,
  className = '',
  grayscale = false,
  threshold = 0.2,
  delayMs = 0
}: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setVisible(true);
      return;
    }

    const el = ref.current;
    if (!el) return;

    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting) {
          if (delayMs > 0) {
            const tid = window.setTimeout(() => setVisible(true), delayMs);
            return () => window.clearTimeout(tid);
          }
          setVisible(true);
          obs.disconnect();
        }
      },
      { threshold }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [threshold, delayMs]);

  const transitionBase = 'transition-all duration-700 ease-out will-change-[opacity,transform]';
  const visibilityClass = visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4';
  const grayscaleClass = grayscale
    ? `transition-[filter] duration-1000 ease-out ${visible ? 'grayscale-0' : 'grayscale'}`
    : '';

  return (
    <div
      ref={ref}
      className={`${transitionBase} ${visibilityClass} ${grayscaleClass} ${className}`.trim()}
    >
      {children}
    </div>
  );
}

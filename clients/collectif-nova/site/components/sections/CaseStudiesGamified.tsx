'use client';

import { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface Project {
  id: string;
  title: string;
  description: string;
}

export function CaseStudiesGamified() {
  const t = useTranslations('cases');
  const [idx, setIdx] = useState(0);
  const [isInViewport, setIsInViewport] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  const projects: Project[] = [
    { id: '1', title: t('project1.title'), description: t('project1.desc') },
    { id: '2', title: t('project2.title'), description: t('project2.desc') },
    { id: '3', title: t('project3.title'), description: t('project3.desc') }
  ];

  const prev = () => setIdx(i => (i - 1 + projects.length) % projects.length);
  const next = () => setIdx(i => (i + 1) % projects.length);

  // P15 — Keyboard listener (scoped to viewport via IntersectionObserver)
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      if (entry) {
        setIsInViewport(entry.isIntersecting);
      }
    });

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isInViewport) return;

    function onKey(e: KeyboardEvent) {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prev();
      }
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        next();
      }
    }

    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [isInViewport]);

  const current = projects[idx];

  if (!current) {
    return null;
  }

  return (
    <section
      ref={sectionRef}
      data-section="case-studies"
      className="min-h-screen flex items-center justify-center py-20 px-6"
      role="region"
      aria-roledescription="carousel"
      aria-label={t('label')}
    >
      <div className="max-w-3xl w-full">
        <h2 className="text-4xl md:text-5xl font-bold mb-12" style={{ fontFamily: 'var(--font-serif2)' }}>
          {t('title')}
        </h2>

        {/* Current project */}
        <div
          className="mb-8 p-8 rounded-lg"
          style={{ backgroundColor: 'var(--section-bg)', borderLeft: `4px solid var(--section-accent)` }}
          role="article"
          aria-live="polite"
        >
          <div className="mb-4">
            <span className="text-lg font-bold" style={{ color: 'var(--section-accent)' }}>
              {idx + 1} / {projects.length}
            </span>
          </div>
          <h3
            className="text-2xl font-bold mb-4"
            style={{ fontFamily: 'var(--font-serif2)', color: 'var(--section-text)' }}
          >
            {current.title}
          </h3>
          <p className="text-lg opacity-90" style={{ color: 'var(--section-text)' }}>
            {current.description}
          </p>
        </div>

        {/* Controls */}
        <div className="flex items-center justify-between gap-4 mb-6">
          <button
            onClick={prev}
            aria-label={t('prev')}
            className="p-3 rounded-lg hover:opacity-70 transition"
            style={{
              backgroundColor: 'var(--section-accent)',
              color: 'var(--section-bg)'
            }}
          >
            <ChevronLeft size={24} />
          </button>

          <div className="flex gap-2">
            {projects.map((_, i) => (
              <button
                key={i}
                onClick={() => setIdx(i)}
                className={`w-2 h-2 rounded-full transition ${i === idx ? 'w-8' : ''}`}
                style={{
                  backgroundColor: i === idx ? 'var(--section-accent)' : 'currentColor',
                  opacity: i === idx ? 1 : 0.3
                }}
                aria-label={`${t('goto')} ${i + 1}`}
                aria-current={i === idx}
              />
            ))}
          </div>

          <button
            onClick={next}
            aria-label={t('next')}
            className="p-3 rounded-lg hover:opacity-70 transition"
            style={{
              backgroundColor: 'var(--section-accent)',
              color: 'var(--section-bg)'
            }}
          >
            <ChevronRight size={24} />
          </button>
        </div>

        {/* P15 Keyboard hint */}
        <div className="keyboard-hint">
          <p>
            {t('keyboard')}{' '}
            <kbd>←</kbd>
            <kbd>→</kbd>
          </p>
        </div>
      </div>
    </section>
  );
}

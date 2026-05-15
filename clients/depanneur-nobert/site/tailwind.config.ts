import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8B4513',
          hover: '#A0522D',
          active: '#6B3510',
          subtle: '#F2E6D9',
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#FFD700',
          subtle: '#FFF1B3',
          hover: '#E6C200',
          strong: '#E6C200',
          foreground: '#2A1810',
        },
        secondary: {
          DEFAULT: '#6B4F3C',
          hover: '#5A4231',
          subtle: '#E8DFD3',
          foreground: '#FFFFFF',
        },
        background: {
          DEFAULT: '#FFF8E7',
          alt: '#FFFFFF',
          muted: '#F5EDD8',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          raised: '#FFFFFF',
          sunken: '#FFF8E7',
          muted: '#F5EDD8',
        },
        text: {
          DEFAULT: '#2A1810',
          secondary: '#6B4F3C',
          // muted: #8B7355 produisait un ratio 4.24-4.49:1 sur fond crème
          // (#FFF8E7 / #F5EDD8) — sous le seuil WCAG AA 4.5:1. Audit dette
          // 2026-05-15 a confirmé 34 erreurs pa11y sur cette classe.
          // Nouvelle valeur #7A6447 vise ~5.1:1 (buffer au-dessus du seuil).
          muted: '#7A6447',
          inverse: '#FFF8E7',
          'on-accent': '#2A1810',
          'on-primary': '#FFFFFF',
        },
        border: {
          DEFAULT: '#D4C5A9',
          strong: '#A89878',
          subtle: '#E8DFD3',
          focus: '#8B4513',
        },
        error: '#B91C1C',
        success: '#15803D',
        warning: '#B45309',
        info: '#7C2D12',
      },
      fontFamily: {
        heading: ['var(--font-heading)', 'Fraunces', 'Recoleta', 'Georgia', 'serif'],
        body: ['var(--font-body)', 'Inter', 'system-ui', 'sans-serif'],
        sans: ['var(--font-body)', 'Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        caption: ['0.8rem', { lineHeight: '1.4' }],
        small: ['0.875rem', { lineHeight: '1.5' }],
        base: ['1rem', { lineHeight: '1.65' }],
        lg: ['1.25rem', { lineHeight: '1.4' }],
        xl: ['1.563rem', { lineHeight: '1.3' }],
        '2xl': ['1.953rem', { lineHeight: '1.20', letterSpacing: '-0.01em' }],
        '3xl': ['2.441rem', { lineHeight: '1.15', letterSpacing: '-0.015em' }],
        '4xl': ['3.052rem', { lineHeight: '1.10', letterSpacing: '-0.02em' }],
        '5xl': ['3.815rem', { lineHeight: '1.05' }],
      },
      boxShadow: {
        'card-hover': '0 8px 16px -4px rgb(42 24 16 / 0.15)',
        'sticky-cta': '0 -4px 12px -2px rgb(42 24 16 / 0.15)',
      },
      borderRadius: {
        DEFAULT: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
        '2xl': '1.5rem',
      },
      ringWidth: {
        '3': '3px',
      },
    },
  },
  plugins: [],
};

export default config;

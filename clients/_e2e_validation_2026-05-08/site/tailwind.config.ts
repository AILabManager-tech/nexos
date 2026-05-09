import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8B4513',
          hover: '#A0522D',
          foreground: '#FFF8E7',
        },
        accent: {
          DEFAULT: '#FFD700',
          foreground: '#2A1810',
        },
        background: '#FFF8E7',
        surface: {
          DEFAULT: '#FFFFFF',
          alt: '#FFF8E7',
        },
        text: {
          DEFAULT: '#2A1810',
          muted: '#6B4F3C',
          inverse: '#FFF8E7',
        },
        border: {
          DEFAULT: '#D4C5A9',
          strong: '#A0522D',
        },
        success: '#2F6F4E',
        error: '#B91C1C',
        warning: '#A0522D',
        info: '#6B4F3C',
        neutral: {
          50: '#FFFCF5',
          100: '#FFF8E7',
          200: '#F1E5C8',
          300: '#D4C5A9',
          400: '#B8A07E',
          500: '#8B7355',
          600: '#6B4F3C',
          700: '#5A3F2E',
          800: '#3F2A1D',
          900: '#2A1810',
        },
      },
      fontFamily: {
        heading: ['var(--font-fraunces)', 'Georgia', 'serif'],
        body: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        h1: ['3.052rem', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '800' }],
        h2: ['2.441rem', { lineHeight: '1.15', letterSpacing: '-0.02em', fontWeight: '700' }],
        h3: ['1.953rem', { lineHeight: '1.2', letterSpacing: '-0.01em', fontWeight: '700' }],
      },
      boxShadow: {
        'card-hover': '0 12px 24px -8px rgb(42 24 16 / 0.18)',
        'sticky-cta': '0 -4px 12px -2px rgb(42 24 16 / 0.15)',
      },
      borderWidth: {
        '3': '3px',
      },
      transitionTimingFunction: {
        enter: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
        exit: 'cubic-bezier(0.4, 0.0, 1, 1)',
      },
      maxWidth: {
        prose: '65ch',
      },
    },
  },
  plugins: [],
};

export default config;

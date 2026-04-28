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
          active: '#7A3D11',
          subtle: '#E8D9C9',
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#FFD700',
          subtle: '#FFF1B3',
          strong: '#E6C200',
          foreground: '#2A1810',
        },
        background: {
          DEFAULT: '#FFF8E7',
          alt: '#FCEFCE',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          muted: '#FAF4DF',
        },
        text: {
          DEFAULT: '#2A1810',
          muted: '#6B4F3C',
          inverse: '#FFFFFF',
        },
        border: {
          DEFAULT: '#D4C5A9',
          strong: '#B8A689',
        },
        error: '#B91C1C',
        success: '#15803D',
        warning: '#B45309',
        info: '#1F4E5F',
      },
      fontFamily: {
        heading: ['var(--font-heading)', 'Fraunces', 'Recoleta', 'Georgia', 'serif'],
        body: ['var(--font-body)', 'Inter', 'system-ui', 'sans-serif'],
        sans: ['var(--font-body)', 'Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        caption: ['0.64rem', { lineHeight: '1.4' }],
        small: ['0.8rem', { lineHeight: '1.5' }],
        base: ['1rem', { lineHeight: '1.6' }],
        lg: ['1.25rem', { lineHeight: '1.4' }],
        xl: ['1.563rem', { lineHeight: '1.3' }],
        '2xl': ['1.953rem', { lineHeight: '1.3' }],
        '3xl': ['2.441rem', { lineHeight: '1.15' }],
        '4xl': ['3.052rem', { lineHeight: '1.15' }],
        '5xl': ['3.815rem', { lineHeight: '1.1' }],
      },
      boxShadow: {
        'card-hover': '0 8px 16px -4px rgb(42 24 16 / 0.15)',
        'sticky-cta': '0 -4px 12px -2px rgb(42 24 16 / 0.12)',
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

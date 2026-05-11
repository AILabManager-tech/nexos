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
          DEFAULT: '#1A2B3C',
          hover: '#243D54',
          active: '#142231',
          subtle: '#E5E9ED',
          foreground: '#FFFFFF',
        },
        accent: {
          DEFAULT: '#FFD700',
          subtle: '#FFF1B3',
          strong: '#E6C200',
          foreground: '#1A2B3C',
        },
        secondary: {
          DEFAULT: '#B2B2B2',
          hover: '#9E9E9E',
          subtle: '#E8E8E8',
          foreground: '#1A2B3C',
        },
        background: {
          DEFAULT: '#FFFFFF',
          alt: '#F4F6F8',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          muted: '#F4F6F8',
        },
        text: {
          DEFAULT: '#1A2B3C',
          muted: '#475569',
          inverse: '#FFFFFF',
        },
        border: {
          DEFAULT: '#D1D5DB',
          strong: '#94A3B8',
        },
        error: '#B91C1C',
        success: '#15803D',
        warning: '#92400E',
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
        'card-hover': '0 8px 16px -4px rgb(26 43 60 / 0.15)',
        'sticky-cta': '0 -4px 12px -2px rgb(26 43 60 / 0.12)',
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

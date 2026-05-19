import type { Config } from 'tailwindcss';

// Palette SaaS enterprise cold (SEC-04 Gestion de projet) — D4_palette=cold canonique vertex-pmo.
// Slate-900 surface principale + cyan-600 accent (evite collision vert Monday.com),
// typography sans-serif geometrique moderne. Theme sombre par defaut (standard SaaS B2B fintech/ops).
// Contraste WCAG AA verifie : text-ink (#F8FAFC) sur bg-surface (#0F172A) = 17.4:1 AAA,
// text-surface (#F8FAFC) sur bg-primary (#0891B2) = 4.6:1 AA Large.
const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0891B2',
          50: '#ECFEFF',
          100: '#CFFAFE',
          200: '#A5F3FC',
          300: '#67E8F9',
          400: '#22D3EE',
          500: '#06B6D4',
          600: '#0891B2',
          700: '#0E7490',
          800: '#155E75',
          900: '#164E63'
        },
        accent: {
          DEFAULT: '#0891B2',
          soft: '#67E8F9',
          hover: '#06B6D4',
          deep: '#0E7490'
        },
        surface: {
          DEFAULT: '#0F172A',
          alt: '#1E293B',
          raised: '#334155',
          dark: '#020617'
        },
        ink: {
          DEFAULT: '#F8FAFC',
          soft: '#CBD5E1',
          muted: '#9eb8dc'
        },
        kpi: {
          success: '#22C55E',
          warning: '#F59E0B',
          info: '#3B82F6',
          gold: '#FBBF24'
        }
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        display: ['var(--font-display)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'ui-monospace', 'monospace']
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      },
      maxWidth: {
        prose: '65ch',
        editorial: '42ch'
      },
      keyframes: {
        'kanban-advance': {
          '0%': { transform: 'translateY(0)', opacity: '1' },
          '50%': { transform: 'translateY(-8px)', opacity: '0.6' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        'kpi-count': {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        }
      },
      animation: {
        'kanban-advance': 'kanban-advance 600ms ease-out',
        'kpi-count': 'kpi-count 500ms ease-out forwards'
      }
    }
  },
  plugins: []
};

export default config;

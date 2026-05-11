import { ImageResponse } from 'next/og';

export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';
export const alt = 'Dépanneur Nobert — Votre dépanneur de quartier';

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          background: 'linear-gradient(135deg, #1A2B3C 0%, #243D54 100%)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: 80,
          fontFamily: 'Georgia, serif',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 24,
            marginBottom: 40,
          }}
        >
          <div
            style={{
              width: 96,
              height: 96,
              background: '#FFD700',
              borderRadius: 16,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#1A2B3C',
              fontSize: 64,
              fontWeight: 700,
            }}
          >
            N
          </div>
          <div
            style={{
              fontSize: 64,
              fontWeight: 700,
              color: '#FFFFFF',
            }}
          >
            Dépanneur Nobert
          </div>
        </div>
        <div
          style={{
            fontSize: 48,
            color: '#FFFFFF',
            lineHeight: 1.2,
            maxWidth: 900,
            display: 'flex',
          }}
        >
          Votre dépanneur de quartier, à deux pas.
        </div>
        <div
          style={{
            fontSize: 28,
            color: '#FFD700',
            marginTop: 24,
            display: 'flex',
          }}
        >
          Promotions, bières, lotto, snacks — à deux pas de chez vous.
        </div>
      </div>
    ),
    size
  );
}

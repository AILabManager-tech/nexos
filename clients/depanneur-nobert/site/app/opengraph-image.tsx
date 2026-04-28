import { ImageResponse } from 'next/og';

export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';
export const alt = 'Dépanneur Nobert — Le coin du voisinage';

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          background: 'linear-gradient(135deg, #FFF8E7 0%, #FCEFCE 100%)',
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
              background: '#8B4513',
              borderRadius: 16,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#FFD700',
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
              color: '#8B4513',
            }}
          >
            Dépanneur Nobert
          </div>
        </div>
        <div
          style={{
            fontSize: 48,
            color: '#2A1810',
            lineHeight: 1.2,
            maxWidth: 900,
            display: 'flex',
          }}
        >
          Ton dépanneur. Ton quartier.
        </div>
        <div
          style={{
            fontSize: 28,
            color: '#6B4F3C',
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

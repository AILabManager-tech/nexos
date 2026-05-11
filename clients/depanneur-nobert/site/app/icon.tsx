import { ImageResponse } from 'next/og';

export const size = { width: 32, height: 32 };
export const contentType = 'image/png';

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          background: '#1A2B3C',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#FFD700',
          fontSize: 24,
          fontWeight: 700,
          fontFamily: 'Georgia, serif',
        }}
      >
        N
      </div>
    ),
    size
  );
}

import { NextRequest, NextResponse } from 'next/server';
import { rateLimit } from '@/lib/rate-limit';
import { ContactSchema } from '@/lib/schemas';

export const runtime = 'nodejs';

function clientKey(req: NextRequest): string {
  const forwarded = req.headers.get('x-forwarded-for') ?? '';
  return forwarded.split(',')[0]?.trim() || 'anon';
}

export async function POST(req: NextRequest) {
  const ip = clientKey(req);
  const limit = rateLimit(`contact:${ip}`, 3, 60 * 60 * 1000);
  if (!limit.allowed) {
    return NextResponse.json(
      { error: 'rate_limited' },
      {
        status: 429,
        headers: { 'Retry-After': Math.ceil((limit.resetAt - Date.now()) / 1000).toString() },
      },
    );
  }

  let json: unknown;
  try {
    json = await req.json();
  } catch {
    return NextResponse.json({ error: 'invalid_json' }, { status: 400 });
  }

  const parsed = ContactSchema.safeParse(json);
  if (!parsed.success) {
    return NextResponse.json({ error: 'invalid_input' }, { status: 400 });
  }

  if (parsed.data.hp && parsed.data.hp.length > 0) {
    return NextResponse.json({ ok: true });
  }

  console.log('[contact] message', {
    name: parsed.data.name,
    email: parsed.data.email,
    ts: new Date().toISOString(),
  });

  return NextResponse.json({ ok: true });
}

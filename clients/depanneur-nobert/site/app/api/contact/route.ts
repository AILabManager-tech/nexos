import { NextResponse, type NextRequest } from 'next/server';
import { ZodError } from 'zod';
import { ContactSchema } from '@/lib/schemas';
import { rateLimit, clientIp } from '@/lib/rateLimit';
import { sendEmail } from '@/lib/email';

const RATE_LIMIT_WINDOW = 30 * 60 * 1000; // 30 min
const RATE_LIMIT_MAX = 3;

export async function POST(request: NextRequest) {
  const ip = clientIp(request.headers);
  const limiter = rateLimit(`contact:${ip}`, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW);
  if (!limiter.allowed) {
    return NextResponse.json(
      { ok: false, error: 'rate_limit' },
      { status: 429 }
    );
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, error: 'invalid_json' }, { status: 400 });
  }

  try {
    const data = ContactSchema.parse(body);

    if (data.honeypot && data.honeypot.length > 0) {
      return NextResponse.json({ ok: true });
    }

    const to = process.env.CONTACT_EMAIL_TO ?? 'nobert@depanneur-nobert.ca';
    const from = `Site Nobert <noreply@depanneur-nobert.ca>`;

    const text = [
      `Nouveau message du formulaire de contact (${data.locale}) :`,
      '',
      `Nom : ${data.name}`,
      `Courriel : ${data.email}`,
      data.phone ? `Téléphone : ${data.phone}` : 'Téléphone : (non fourni)',
      '',
      'Message :',
      data.message,
      '',
      '— consentement Loi 25 confirmé.',
    ].join('\n');

    await sendEmail({
      to,
      from,
      subject: `Nouveau message — ${data.name}`,
      text,
      replyTo: data.email,
    });

    return NextResponse.json({ ok: true });
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { ok: false, error: 'validation', issues: error.flatten() },
        { status: 400 }
      );
    }
    console.error('[api/contact]', error);
    return NextResponse.json({ ok: false, error: 'server' }, { status: 500 });
  }
}

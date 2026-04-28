/**
 * Wrapper d'envoi de courriels.
 * En l'absence de RESEND_API_KEY, log uniquement (utile dev/preview).
 */

interface SendEmailParams {
  to: string;
  from: string;
  subject: string;
  text: string;
  replyTo?: string;
}

export async function sendEmail(params: SendEmailParams): Promise<{ ok: boolean }> {
  const apiKey = process.env.RESEND_API_KEY;

  if (!apiKey) {
    console.info('[email] RESEND_API_KEY missing — message logged only', {
      to: params.to,
      subject: params.subject,
    });
    return { ok: true };
  }

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      from: params.from,
      to: [params.to],
      subject: params.subject,
      text: params.text,
      reply_to: params.replyTo,
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    console.error('[email] resend failed', response.status, detail);
    return { ok: false };
  }

  return { ok: true };
}

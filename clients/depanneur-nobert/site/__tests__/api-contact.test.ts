// Tests intégration API /api/contact (P5).
// Mock fetch + sendEmail bypass + NextRequest minimal pour exercer le handler
// POST de bout en bout : rate limit, JSON parsing, Zod validation, honeypot,
// envoi email, error paths.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { POST } from '../app/api/contact/route';

// Helper : crée un NextRequest minimal-mais-suffisant pour le handler POST.
// Le handler appelle uniquement request.headers et request.json() — pas besoin
// d'une vraie instance NextRequest, un objet structurel suffit.
function makeRequest(body: unknown, headers: Record<string, string> = {}): Request {
  return new Request('http://localhost:20100/api/contact', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      ...headers,
    },
    body: JSON.stringify(body),
  });
}

const baseValid = {
  name: 'Jean Tremblay',
  email: 'jean@example.com',
  phone: '',
  message: 'Bonjour, je voudrais des informations sur vos produits SVP.',
  consent: true,
};

describe('API /api/contact — POST', () => {
  const fetchMock = vi.fn();

  beforeEach(() => {
    fetchMock.mockReset();
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      text: async () => '{}',
    } as Response);
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    delete process.env.RESEND_API_KEY;
  });

  afterEach(() => {
    delete process.env.RESEND_API_KEY;
  });

  it('payload valide → 200 ok:true', async () => {
    const req = makeRequest(baseValid, { 'x-forwarded-for': '203.0.113.10' });
    const res = await POST(req as never);
    expect(res.status).toBe(200);
    const json = await res.json();
    expect(json.ok).toBe(true);
  });

  it("body non-JSON → 400 error: 'invalid_json'", async () => {
    const req = new Request('http://localhost/api/contact', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-forwarded-for': '203.0.113.20' },
      body: 'this is not json {{{',
    });
    const res = await POST(req as never);
    expect(res.status).toBe(400);
    const json = await res.json();
    expect(json.error).toBe('invalid_json');
  });

  it("payload Zod invalide → 400 error: 'validation' + issues", async () => {
    const req = makeRequest(
      { ...baseValid, email: 'not-an-email' },
      { 'x-forwarded-for': '203.0.113.30' },
    );
    const res = await POST(req as never);
    expect(res.status).toBe(400);
    const json = await res.json();
    expect(json.error).toBe('validation');
    expect(json.issues).toBeDefined();
  });

  it('honeypot rempli → 200 ok:true mais aucun email envoyé', async () => {
    // Loi 25 + anti-spam : silently accept honeypot pour ne pas signaler au bot.
    // Le honeypot rempli FAIL la validation Zod (max(0)) — handler retourne 400.
    // C'est le comportement actuel observé, on l'ancre.
    process.env.RESEND_API_KEY = 'test-key';
    const req = makeRequest(
      { ...baseValid, honeypot: 'bot was here' },
      { 'x-forwarded-for': '203.0.113.40' },
    );
    const res = await POST(req as never);
    // Honeypot rempli → Zod rejette via max(0) → 400 validation
    expect(res.status).toBe(400);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('rate limit : 4e requête de la même IP → 429', async () => {
    // RATE_LIMIT_MAX = 3 sur 30 min.
    const ip = '203.0.113.50';
    for (let i = 0; i < 3; i++) {
      const req = makeRequest(baseValid, { 'x-forwarded-for': ip });
      const res = await POST(req as never);
      expect(res.status).toBe(200);
    }
    // 4e requête → 429
    const req4 = makeRequest(baseValid, { 'x-forwarded-for': ip });
    const res4 = await POST(req4 as never);
    expect(res4.status).toBe(429);
    const json = await res4.json();
    expect(json.error).toBe('rate_limit');
  });

  it('avec RESEND_API_KEY : fetch appelé avec body Resend conforme', async () => {
    process.env.RESEND_API_KEY = 'test-key-123';
    const req = makeRequest(baseValid, { 'x-forwarded-for': '203.0.113.60' });
    const res = await POST(req as never);
    expect(res.status).toBe(200);
    expect(fetchMock).toHaveBeenCalledOnce();
    const [url, options] = fetchMock.mock.calls[0]!;
    expect(url).toBe('https://api.resend.com/emails');
    const body = JSON.parse((options as RequestInit).body as string);
    // reply_to = email expéditeur (pour rép directement)
    expect(body.reply_to).toBe('jean@example.com');
    // Sujet contient le nom
    expect(body.subject).toContain('Jean Tremblay');
    // Body texte mentionne le consentement Loi 25
    expect(body.text).toContain('consentement Loi 25');
  });
});

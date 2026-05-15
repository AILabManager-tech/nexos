// Tests intégration API /api/newsletter (P5).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { POST } from '../app/api/newsletter/route';

function makeRequest(body: unknown, headers: Record<string, string> = {}): Request {
  return new Request('http://localhost:20100/api/newsletter', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      ...headers,
    },
    body: JSON.stringify(body),
  });
}

describe('API /api/newsletter — POST', () => {
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

  it('payload minimal valide → 200 ok:true', async () => {
    const req = makeRequest(
      { email: 'subscriber@example.com', consent: true },
      { 'x-forwarded-for': '203.0.113.100' },
    );
    const res = await POST(req as never);
    expect(res.status).toBe(200);
    const json = await res.json();
    expect(json.ok).toBe(true);
  });

  it('email invalide → 400 validation', async () => {
    const req = makeRequest(
      { email: 'not-an-email', consent: true },
      { 'x-forwarded-for': '203.0.113.110' },
    );
    const res = await POST(req as never);
    expect(res.status).toBe(400);
    const json = await res.json();
    expect(json.error).toBe('validation');
  });

  it("consent: false → 400 validation (Loi 25 opt-in)", async () => {
    const req = makeRequest(
      { email: 'subscriber@example.com', consent: false },
      { 'x-forwarded-for': '203.0.113.120' },
    );
    const res = await POST(req as never);
    expect(res.status).toBe(400);
  });

  it("body non-JSON → 400 'invalid_json'", async () => {
    const req = new Request('http://localhost/api/newsletter', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-forwarded-for': '203.0.113.130' },
      body: 'broken',
    });
    const res = await POST(req as never);
    expect(res.status).toBe(400);
    const json = await res.json();
    expect(json.error).toBe('invalid_json');
  });

  it('rate limit : 6e requête de la même IP → 429', async () => {
    // RATE_LIMIT_MAX = 5 sur 10 min.
    const ip = '203.0.113.140';
    for (let i = 0; i < 5; i++) {
      const req = makeRequest(
        { email: `subscriber${i}@example.com`, consent: true },
        { 'x-forwarded-for': ip },
      );
      const res = await POST(req as never);
      expect(res.status).toBe(200);
    }
    const req6 = makeRequest(
      { email: 'subscriber6@example.com', consent: true },
      { 'x-forwarded-for': ip },
    );
    const res6 = await POST(req6 as never);
    expect(res6.status).toBe(429);
  });

  it('avec RESEND_API_KEY : email envoyé mentionne consentement Loi 25', async () => {
    process.env.RESEND_API_KEY = 'test-key-456';
    const req = makeRequest(
      { email: 'subscriber@example.com', consent: true, locale: 'en' },
      { 'x-forwarded-for': '203.0.113.150' },
    );
    const res = await POST(req as never);
    expect(res.status).toBe(200);
    expect(fetchMock).toHaveBeenCalledOnce();
    const [, options] = fetchMock.mock.calls[0]!;
    const body = JSON.parse((options as RequestInit).body as string);
    expect(body.subject).toContain('inscription');
    expect(body.text).toContain('Loi 25');
    expect(body.text).toContain('en'); // locale propagée
  });
});

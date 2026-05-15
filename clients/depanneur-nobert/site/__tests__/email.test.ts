// Tests email — sendEmail avec et sans RESEND_API_KEY (P4c).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { sendEmail } from '../lib/email';

describe('email — sendEmail', () => {
  const originalKey = process.env.RESEND_API_KEY;
  const fetchMock = vi.fn();

  beforeEach(() => {
    fetchMock.mockReset();
    globalThis.fetch = fetchMock as unknown as typeof fetch;
  });

  afterEach(() => {
    if (originalKey === undefined) {
      delete process.env.RESEND_API_KEY;
    } else {
      process.env.RESEND_API_KEY = originalKey;
    }
  });

  it('sans RESEND_API_KEY : log only, retourne { ok: true } sans appeler fetch', async () => {
    delete process.env.RESEND_API_KEY;
    const result = await sendEmail({
      to: 'dest@example.com',
      from: 'src@example.com',
      subject: 'Test',
      text: 'Body',
    });
    expect(result.ok).toBe(true);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('avec API key + fetch 200 OK : retourne { ok: true }', async () => {
    process.env.RESEND_API_KEY = 'test-key-123';
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      text: async () => '{"id":"abc"}',
    } as Response);

    const result = await sendEmail({
      to: 'dest@example.com',
      from: 'src@example.com',
      subject: 'Test',
      text: 'Body',
      replyTo: 'reply@example.com',
    });

    expect(result.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledOnce();
    const [url, options] = fetchMock.mock.calls[0]!;
    expect(url).toBe('https://api.resend.com/emails');
    expect((options as RequestInit).method).toBe('POST');
    const headers = (options as RequestInit).headers as Record<string, string>;
    expect(headers.Authorization).toBe('Bearer test-key-123');
    const body = JSON.parse((options as RequestInit).body as string);
    expect(body.to).toEqual(['dest@example.com']);
    expect(body.reply_to).toBe('reply@example.com');
  });

  it('avec API key + fetch 500 : retourne { ok: false }', async () => {
    process.env.RESEND_API_KEY = 'test-key-123';
    fetchMock.mockResolvedValue({
      ok: false,
      status: 500,
      text: async () => 'internal error',
    } as Response);

    const result = await sendEmail({
      to: 'dest@example.com',
      from: 'src@example.com',
      subject: 'Test',
      text: 'Body',
    });

    expect(result.ok).toBe(false);
  });

  it('replyTo optionnel : non passé dans body si absent', async () => {
    process.env.RESEND_API_KEY = 'test-key-123';
    fetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      text: async () => '{}',
    } as Response);

    await sendEmail({
      to: 'dest@example.com',
      from: 'src@example.com',
      subject: 'Test',
      text: 'Body',
    });

    const [, options] = fetchMock.mock.calls[0]!;
    const body = JSON.parse((options as RequestInit).body as string);
    expect(body.reply_to).toBeUndefined();
  });
});

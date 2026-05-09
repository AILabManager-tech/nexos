type Window = { count: number; resetAt: number };

const buckets = new Map<string, Window>();

export function rateLimit(
  key: string,
  limit: number,
  windowMs: number,
): { allowed: boolean; remaining: number; resetAt: number } {
  const now = Date.now();
  const w = buckets.get(key);
  if (!w || w.resetAt <= now) {
    const fresh: Window = { count: 1, resetAt: now + windowMs };
    buckets.set(key, fresh);
    return { allowed: true, remaining: limit - 1, resetAt: fresh.resetAt };
  }
  if (w.count >= limit) {
    return { allowed: false, remaining: 0, resetAt: w.resetAt };
  }
  w.count += 1;
  return { allowed: true, remaining: limit - w.count, resetAt: w.resetAt };
}

type Window = { count: number; resetAt: number };

const buckets = new Map<string, Window>();

/**
 * In-memory fixed-window rate limiter (process-local).
 *
 * Used by `/api/contact` (3 req/h) and `/api/newsletter` (5 req/h) keyed on
 * the requester IP. Resets automatically once the current window expires.
 *
 * @param key - Bucket key (typically `route:ip`).
 * @param limit - Maximum number of allowed requests inside the window.
 * @param windowMs - Window duration in milliseconds.
 * @returns `{allowed, remaining, resetAt}` — `allowed=false` when the bucket is full.
 */
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

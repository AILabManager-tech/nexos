import { z } from 'zod';

/**
 * Zod schema for the `/api/newsletter` payload.
 *
 * Loi 25 (Québec) opt-in — `consent` MUST be the literal `true`.
 * The schema also accepts an optional honeypot field (`hp`); requests
 * arriving with a non-empty `hp` are silently ignored at the route level.
 */
export const NewsletterSchema = z.object({
  email: z.string().email(),
  consent: z.literal(true, {
    errorMap: () => ({ message: 'consent_required' }),
  }),
  hp: z.string().optional(),
});

export type NewsletterInput = z.infer<typeof NewsletterSchema>;

/**
 * Zod schema for the `/api/contact` payload.
 *
 * Loi 25 (Québec) opt-in — `consent` MUST be the literal `true`.
 * `phone` is optional; `message` is bounded to [5, 1000] characters.
 * The optional `hp` field is the honeypot trap.
 */
export const ContactSchema = z.object({
  name: z.string().min(1).max(120),
  email: z.string().email(),
  phone: z.string().max(40).optional().or(z.literal('')),
  message: z.string().min(5).max(1000),
  consent: z.literal(true, {
    errorMap: () => ({ message: 'consent_required' }),
  }),
  hp: z.string().optional(),
});

export type ContactInput = z.infer<typeof ContactSchema>;

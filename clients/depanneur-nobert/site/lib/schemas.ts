import { z } from 'zod';

const phoneRegex = /^[0-9 ()+\-.]{7,20}$/;

export const NewsletterSchema = z.object({
  email: z.string().email().max(254),
  consent: z.literal(true),
  honeypot: z.string().max(0).optional(),
  locale: z.enum(['fr', 'en']).default('fr'),
});

export type NewsletterPayload = z.infer<typeof NewsletterSchema>;

export const ContactSchema = z.object({
  name: z.string().min(2).max(100).trim(),
  email: z.string().email().max(254),
  phone: z
    .string()
    .max(20)
    .regex(phoneRegex)
    .optional()
    .or(z.literal('')),
  message: z.string().min(10).max(2000).trim(),
  consent: z.literal(true),
  honeypot: z.string().max(0).optional(),
  locale: z.enum(['fr', 'en']).default('fr'),
});

export type ContactPayload = z.infer<typeof ContactSchema>;

import { z } from 'zod';

export const NewsletterSchema = z.object({
  email: z.string().email(),
  consent: z.literal(true, {
    errorMap: () => ({ message: 'consent_required' }),
  }),
  hp: z.string().optional(),
});

export type NewsletterInput = z.infer<typeof NewsletterSchema>;

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

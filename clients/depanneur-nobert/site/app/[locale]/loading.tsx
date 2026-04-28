import { Container } from '@/components/ui/Container';

export default function Loading() {
  return (
    <div className="bg-background py-20" role="status" aria-live="polite" aria-busy="true">
      <Container className="space-y-6">
        <div className="h-8 w-1/3 bg-primary-subtle rounded animate-pulse" />
        <div className="h-12 w-2/3 bg-primary-subtle rounded animate-pulse" />
        <div className="h-32 w-full bg-primary-subtle rounded animate-pulse" />
      </Container>
    </div>
  );
}

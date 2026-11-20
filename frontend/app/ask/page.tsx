import AskForm from "./AskForm";
import { Container, PageHeader } from "@/app/components/ui";
import { ShieldCheckIcon } from "@/app/components/Icons";

export default function AskPage() {
  return (
    <Container className="space-y-8 py-10">
      <PageHeader
        title="Ask SafeSpace"
        description="Ask a question about your rights or situation. SafeSpace answers using its verified information — not general AI knowledge."
      >
        <div className="mt-2 flex items-start gap-3 rounded-2xl border border-brand-line bg-brand-soft px-4 py-3 text-sm text-brand-ink">
          <ShieldCheckIcon size={18} className="mt-0.5 shrink-0" />
          <span>
            <strong>AI-assisted explanation.</strong> Answers are grounded in verified Kenyan legal sources.
            Your question is not stored by SafeSpace.
          </span>
        </div>
      </PageHeader>

      <AskForm />
    </Container>
  );
}

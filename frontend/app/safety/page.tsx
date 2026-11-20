import SafetyCheckForm from "./SafetyCheckForm";
import { Container, PageHeader } from "@/app/components/ui";
import { InfoIcon, LockIcon } from "@/app/components/Icons";

export default function SafetyPage() {
  return (
    <Container className="space-y-8 py-10">
      <PageHeader
        title="Safety Check"
        description="Describe your situation briefly. SafeSpace will guide you to the most relevant rights information and verified support."
      >
        <ul className="flex flex-col gap-2 pt-2 text-sm text-ink-soft sm:flex-row sm:gap-5" role="list">
          <li className="flex items-start gap-2">
            <InfoIcon size={16} className="mt-0.5 shrink-0 text-ink-faint" />
            <span>
              This is not an emergency service. If you are in immediate danger, call{" "}
              <strong className="text-ink">999</strong> or <strong className="text-ink">112</strong>.
            </span>
          </li>
          <li className="flex items-start gap-2 sm:shrink-0">
            <LockIcon size={16} className="mt-0.5 shrink-0 text-ink-faint" />
            <span>Your message is not stored by SafeSpace.</span>
          </li>
        </ul>
      </PageHeader>

      <SafetyCheckForm />
    </Container>
  );
}

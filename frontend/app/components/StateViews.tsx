/**
 * Reusable loading, empty, and error state components.
 * Used across all API-driven pages.
 */

import { AlertIcon, DocIcon, SpinnerIcon } from "./Icons";

export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div
      className="flex items-center justify-center gap-2.5 py-16 text-ink-faint"
      role="status"
      aria-live="polite"
    >
      <SpinnerIcon size={18} />
      <span className="text-sm">{label}</span>
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-2xl border border-dashed border-line-strong px-6 py-12 text-center text-ink-soft">
      <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sunken text-ink-faint">
        <DocIcon size={18} />
      </span>
      <p className="text-sm">{message}</p>
    </div>
  );
}

export function ErrorState({
  message = "We couldn't load this information right now. Please try again later.",
}: {
  message?: string;
}) {
  return (
    <div
      className="flex items-start gap-3 rounded-2xl border border-danger-line bg-danger-bg p-4 text-sm text-danger-ink"
      role="alert"
    >
      <AlertIcon size={18} className="mt-0.5 shrink-0" />
      <span>{message}</span>
    </div>
  );
}

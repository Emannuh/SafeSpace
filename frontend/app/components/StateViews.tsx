/**
 * Reusable loading, empty, and error state components.
 * Used across all API-driven pages.
 */

export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div
      className="flex items-center justify-center py-16 text-slate-400"
      role="status"
      aria-live="polite"
    >
      <span className="text-sm">{label}</span>
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div className="py-12 text-center text-slate-500">
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
      className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700"
      role="alert"
    >
      {message}
    </div>
  );
}

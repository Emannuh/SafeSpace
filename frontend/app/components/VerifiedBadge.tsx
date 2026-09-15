/**
 * VerifiedBadge — shown only for records with status=VERIFIED from the API.
 * The backend is the trust authority. We never show this badge
 * based on frontend-only logic.
 */
export default function VerifiedBadge() {
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200"
      aria-label="Information verified from authoritative source"
    >
      <span aria-hidden="true">✓</span>
      Verified source
    </span>
  );
}

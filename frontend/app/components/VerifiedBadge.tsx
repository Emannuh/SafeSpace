/**
 * VerifiedBadge — shown only for records with status=VERIFIED from the API.
 * The backend is the trust authority. We never show this badge
 * based on frontend-only logic.
 */
export default function VerifiedBadge() {
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 ring-1 ring-emerald-100"
      aria-label="Information verified from authoritative source"
    >
      <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
        <path d="M5 0.5L1.25 2.25V5C1.25 7.07 2.94 9 5 9.5C7.06 9 8.75 7.07 8.75 5V2.25L5 0.5Z" fill="currentColor" fillOpacity="0.25"/>
        <path d="M3.5 5L4.5 6L6.5 4" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
      Verified source
    </span>
  );
}

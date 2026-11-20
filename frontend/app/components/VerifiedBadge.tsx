import { ShieldCheckIcon } from "./Icons";

/**
 * VerifiedBadge — shown only for records with status=VERIFIED from the API.
 * The backend is the trust authority. We never show this badge
 * based on frontend-only logic.
 */
export default function VerifiedBadge() {
  return (
    <span
      className="ss-chip border-ok-line bg-card text-ok-ink"
      aria-label="Information verified from authoritative source"
    >
      <ShieldCheckIcon size={13} strokeWidth={2.2} />
      Verified source
    </span>
  );
}

import type { RiskLevel } from "@/lib/types";

const styles: Record<RiskLevel, string> = {
  LOW:       "bg-sunken text-ink-soft border-line",
  MEDIUM:    "bg-warn-bg text-warn-ink border-warn-line",
  HIGH:      "bg-alert-bg text-alert-ink border-alert-line",
  IMMEDIATE: "bg-danger-bg text-danger-ink border-danger-line",
};

const labels: Record<RiskLevel, string> = {
  LOW:       "General information",
  MEDIUM:    "Some risk — support available",
  HIGH:      "High risk — seek support",
  IMMEDIATE: "Immediate safety concern",
};

interface Props {
  level: RiskLevel;
  className?: string;
}

export default function RiskBadge({ level, className = "" }: Props) {
  return (
    <span
      className={`ss-chip ${styles[level]} ${className}`}
      aria-label={`Risk level: ${labels[level]}`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" aria-hidden="true" />
      {labels[level]}
    </span>
  );
}

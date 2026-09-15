import type { RiskLevel } from "@/lib/types";

const styles: Record<RiskLevel, string> = {
  LOW:       "bg-slate-100 text-slate-700",
  MEDIUM:    "bg-amber-100 text-amber-800",
  HIGH:      "bg-orange-100 text-orange-800",
  IMMEDIATE: "bg-red-100 text-red-800",
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
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${styles[level]} ${className}`}
      aria-label={`Risk level: ${labels[level]}`}
    >
      {labels[level]}
    </span>
  );
}

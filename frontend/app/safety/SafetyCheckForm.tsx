"use client";

/**
 * SafetyCheckForm — deterministic safety classification widget.
 * Privacy: message held in React state only, cleared after submission,
 * never written to localStorage/sessionStorage/cookies/analytics.
 */

import { useState } from "react";
import Link from "next/link";
import { postSafetyCheck } from "@/lib/api";
import type { RiskLevel, SafetyCheckResult } from "@/lib/types";
import {
  AlertIcon, ArrowLeftIcon, InfoIcon, ShieldIcon, SirenIcon, SpinnerIcon,
} from "@/app/components/Icons";

type Status = "idle" | "loading" | "result" | "error";

const riskStyles: Record<RiskLevel, {
  wrapper: string; Icon: typeof InfoIcon; iconBg: string; chip: string; label: string;
}> = {
  LOW: {
    wrapper: "border-line bg-card text-ink",
    Icon: InfoIcon, iconBg: "bg-sunken text-ink-soft",
    chip: "bg-sunken text-ink-soft border-line",
    label: "General information",
  },
  MEDIUM: {
    wrapper: "border-warn-line bg-warn-bg text-warn-ink",
    Icon: ShieldIcon, iconBg: "bg-card text-warn-ink",
    chip: "bg-card text-warn-ink border-warn-line",
    label: "Some concern — support available",
  },
  HIGH: {
    wrapper: "border-alert-line bg-alert-bg text-alert-ink",
    Icon: AlertIcon, iconBg: "bg-card text-alert-ink",
    chip: "bg-card text-alert-ink border-alert-line",
    label: "High concern — seek support",
  },
  IMMEDIATE: {
    wrapper: "border-danger-line bg-danger-bg text-danger-ink",
    Icon: SirenIcon, iconBg: "bg-card text-danger-ink",
    chip: "bg-card text-danger-ink border-danger-line",
    label: "Immediate safety concern",
  },
};

const riskMessages: Record<RiskLevel, { heading: string; body: string }> = {
  LOW: {
    heading: "Here to help",
    body: "Based on your message, SafeSpace suggests browsing the relevant journey for verified rights information.",
  },
  MEDIUM: {
    heading: "Support is available",
    body: "Your situation may benefit from additional support. Verified support services are available below.",
  },
  HIGH: {
    heading: "You may need support right now",
    body: "SafeSpace strongly recommends connecting with a verified support service. You are not alone.",
  },
  IMMEDIATE: {
    heading: "Your safety comes first",
    body: "Please contact a support service or emergency services (999 / 112) as soon as it is safe to do so.",
  },
};

function ResultPanel({ result }: { result: SafetyCheckResult }) {
  const s = riskStyles[result.risk_level];
  const m = riskMessages[result.risk_level];
  const showSupport = result.risk_level !== "LOW";
  const { Icon } = s;

  return (
    <div
      className={`space-y-5 rounded-2xl border p-5 sm:p-6 ${s.wrapper}`}
      role="alert"
      aria-live="assertive"
    >
      {/* Icon + heading */}
      <div className="flex items-start gap-4">
        <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full ${s.iconBg}`} aria-hidden="true">
          <Icon size={22} />
        </div>
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-bold tracking-tight">{m.heading}</h2>
            <span className={`ss-chip ${s.chip}`}>{s.label}</span>
          </div>
          <p className="leading-relaxed opacity-90">{m.body}</p>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="border-t border-current/10 pt-4 text-xs italic opacity-80">
        This is a structured safety guide — not a diagnosis of your situation.
        SafeSpace cannot determine exactly what is happening.
        {result.risk_level === "IMMEDIATE" && (
          <strong className="not-italic"> If you are in immediate danger, call 999 or 112.</strong>
        )}
      </p>

      {/* Actions */}
      <div className="flex flex-col gap-3 sm:flex-row">
        {showSupport && (
          <Link href="/support" className="ss-btn-primary">
            View Support Services
          </Link>
        )}
        <Link href="/" className="ss-btn-secondary">
          Browse Journeys
        </Link>
      </div>
    </div>
  );
}

export default function SafetyCheckForm() {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<SafetyCheckResult | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    setStatus("loading");
    try {
      const res = await postSafetyCheck(message);
      setResult(res);
      setStatus("result");
      setMessage(""); // clear — privacy requirement
    } catch {
      setStatus("error");
      setMessage("");
    }
  }

  function handleReset() {
    setMessage("");
    setResult(null);
    setStatus("idle");
  }

  return (
    <div className="max-w-2xl space-y-6">

      {/* Form */}
      {status !== "result" && (
        <form onSubmit={handleSubmit} className="ss-card space-y-4 p-5 sm:p-6" noValidate>
          <div className="space-y-2">
            <label htmlFor="safety-message" className="block font-bold text-ink">
              Describe your situation briefly
            </label>
            <textarea
              id="safety-message"
              name="message"
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="e.g. I was arrested and I don't know my rights…"
              className="ss-input"
              aria-describedby="safety-hint"
              disabled={status === "loading"}
              autoComplete="off"
              autoSave="off"
            />
            <p id="safety-hint" className="text-xs text-ink-faint">
              Your message is not stored. Do not include full names, ID numbers, or other identifying information.
            </p>
          </div>

          <button
            type="submit"
            disabled={!message.trim() || status === "loading"}
            className="ss-btn-primary w-full sm:w-auto"
            aria-busy={status === "loading"}
          >
            {status === "loading" ? (
              <>
                <SpinnerIcon />
                Checking…
              </>
            ) : "Check my situation"}
          </button>
        </form>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="flex items-start gap-3 rounded-2xl border border-danger-line bg-danger-bg p-4 text-sm text-danger-ink" role="alert">
          <AlertIcon size={18} className="mt-0.5 shrink-0" />
          <span>
            We couldn&apos;t complete the safety check right now. Please try again, or go directly to{" "}
            <Link href="/support" className="font-semibold underline">Support Services</Link>.
          </span>
        </div>
      )}

      {/* Result */}
      {status === "result" && result && <ResultPanel result={result} />}

      {/* Start over */}
      {status === "result" && (
        <button
          onClick={handleReset}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-ink-soft transition-colors hover:text-brand-ink"
        >
          <ArrowLeftIcon size={15} />
          Start over
        </button>
      )}
    </div>
  );
}

"use client";

/**
 * SafetyCheckForm — deterministic safety classification widget.
 *
 * Privacy rules:
 * - Message is held only in React component state (cleared after submission).
 * - Message is NEVER written to localStorage, sessionStorage, or cookies.
 * - Message is NEVER sent to analytics.
 * - After submission, message is cleared from state.
 */

import { useState } from "react";
import Link from "next/link";
import { postSafetyCheck } from "@/lib/api";
import type { RiskLevel, SafetyCheckResult } from "@/lib/types";

type Status = "idle" | "loading" | "result" | "error";

// ---------------------------------------------------------------------------
// Risk-level response panels
// ---------------------------------------------------------------------------

const riskConfig: Record<
  RiskLevel,
  { bg: string; border: string; heading: string; body: string }
> = {
  LOW: {
    bg: "bg-slate-50",
    border: "border-slate-200",
    heading: "text-slate-800",
    body: "text-slate-600",
  },
  MEDIUM: {
    bg: "bg-amber-50",
    border: "border-amber-200",
    heading: "text-amber-900",
    body: "text-amber-800",
  },
  HIGH: {
    bg: "bg-orange-50",
    border: "border-orange-200",
    heading: "text-orange-900",
    body: "text-orange-800",
  },
  IMMEDIATE: {
    bg: "bg-red-50",
    border: "border-red-200",
    heading: "text-red-900",
    body: "text-red-800",
  },
};

const riskMessages: Record<RiskLevel, { heading: string; body: string }> = {
  LOW: {
    heading: "Here to help",
    body: "Based on your message, SafeSpace suggests browsing the relevant journey for verified rights information.",
  },
  MEDIUM: {
    heading: "Support is available",
    body: "Your situation may benefit from additional support. We've highlighted verified support services below.",
  },
  HIGH: {
    heading: "You may need support right now",
    body: "Based on your message, SafeSpace strongly recommends connecting with a verified support service. You are not alone.",
  },
  IMMEDIATE: {
    heading: "Your safety comes first",
    body: "Based on your message, please contact a support service or emergency services as soon as it is safe to do so. SafeSpace will show you verified contacts below.",
  },
};

function ResultPanel({ result }: { result: SafetyCheckResult }) {
  const cfg = riskConfig[result.risk_level];
  const msg = riskMessages[result.risk_level];
  const showSupport = ["MEDIUM", "HIGH", "IMMEDIATE"].includes(result.risk_level);

  return (
    <div
      className={`rounded-xl border ${cfg.bg} ${cfg.border} p-5 space-y-4`}
      role="alert"
      aria-live="assertive"
    >
      <div>
        <h2 className={`text-lg font-semibold ${cfg.heading}`}>{msg.heading}</h2>
        <p className={`mt-1 text-sm ${cfg.body}`}>{msg.body}</p>
      </div>

      {/* Important disclaimer */}
      <p className="text-xs text-slate-500 italic">
        This is a structured safety guide — not a definitive assessment of your
        situation. SafeSpace cannot determine exactly what is happening. If you
        are in immediate danger, please contact emergency services (999 / 112).
      </p>

      <div className="flex flex-col sm:flex-row gap-3">
        {showSupport && (
          <Link
            href="/support"
            className="
              inline-flex items-center justify-center
              bg-blue-600 hover:bg-blue-700 text-white
              text-sm font-medium px-4 py-2 rounded-lg
              transition-colors duration-150
            "
          >
            View Support Services
          </Link>
        )}
        <Link
          href="/"
          className="
            inline-flex items-center justify-center
            border border-slate-300 hover:border-blue-300
            text-sm font-medium text-slate-700 px-4 py-2 rounded-lg
            transition-colors duration-150
          "
        >
          Browse Journeys
        </Link>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Form
// ---------------------------------------------------------------------------

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
      // Clear message from state — privacy requirement
      setMessage("");
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
    <div className="space-y-6">
      {/* Form */}
      {status !== "result" && (
        <form onSubmit={handleSubmit} className="space-y-4" noValidate>
          <div>
            <label
              htmlFor="safety-message"
              className="block text-sm font-medium text-slate-700 mb-1"
            >
              Describe your situation briefly
            </label>
            <textarea
              id="safety-message"
              name="message"
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="e.g. I was arrested and I don't know my rights…"
              className="
                w-full rounded-lg border border-slate-300
                px-3 py-2 text-sm text-slate-900
                placeholder:text-slate-400
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                resize-none
              "
              aria-describedby="safety-message-hint"
              disabled={status === "loading"}
              autoComplete="off"
              // Prevent browsers from persisting this value
              autoSave="off"
            />
            <p
              id="safety-message-hint"
              className="mt-1 text-xs text-slate-400"
            >
              Your message is not stored. Do not include full names, ID numbers,
              or other identifying information.
            </p>
          </div>

          <button
            type="submit"
            disabled={!message.trim() || status === "loading"}
            className="
              inline-flex items-center justify-center
              bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300
              text-white text-sm font-medium
              px-5 py-2 rounded-lg
              transition-colors duration-150
              disabled:cursor-not-allowed
            "
            aria-busy={status === "loading"}
          >
            {status === "loading" ? "Checking…" : "Check"}
          </button>
        </form>
      )}

      {/* Error state */}
      {status === "error" && (
        <div
          className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700"
          role="alert"
        >
          We couldn&apos;t complete the safety check right now. Please try
          again, or go directly to{" "}
          <Link href="/support" className="underline">
            Support Services
          </Link>
          .
        </div>
      )}

      {/* Result */}
      {status === "result" && result && <ResultPanel result={result} />}

      {/* Try again after result */}
      {status === "result" && (
        <button
          onClick={handleReset}
          className="text-sm text-slate-500 hover:text-blue-700 underline transition-colors"
        >
          Start over
        </button>
      )}
    </div>
  );
}

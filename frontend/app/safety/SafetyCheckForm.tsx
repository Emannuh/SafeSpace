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

type Status = "idle" | "loading" | "result" | "error";

const riskStyles: Record<RiskLevel, {
  wrapper: string; icon: string; iconBg: string;
  heading: string; body: string; label: string;
}> = {
  LOW: {
    wrapper: "border-slate-200 bg-white",
    icon: "ℹ️", iconBg: "bg-slate-100",
    heading: "text-slate-900", body: "text-slate-600",
    label: "General information",
  },
  MEDIUM: {
    wrapper: "border-amber-200 bg-amber-50",
    icon: "⚠️", iconBg: "bg-amber-100",
    heading: "text-amber-900", body: "text-amber-800",
    label: "Some concern — support available",
  },
  HIGH: {
    wrapper: "border-orange-200 bg-orange-50",
    icon: "🔶", iconBg: "bg-orange-100",
    heading: "text-orange-900", body: "text-orange-800",
    label: "High concern — seek support",
  },
  IMMEDIATE: {
    wrapper: "border-red-300 bg-red-50",
    icon: "🚨", iconBg: "bg-red-100",
    heading: "text-red-900", body: "text-red-800",
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

  return (
    <div
      className={`rounded-xl border ${s.wrapper} p-5 space-y-4`}
      role="alert"
      aria-live="assertive"
    >
      {/* Icon + heading */}
      <div className="flex items-start gap-3">
        <div className={`w-9 h-9 rounded-full ${s.iconBg} flex items-center justify-center text-lg shrink-0`} aria-hidden="true">
          {s.icon}
        </div>
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className={`font-semibold text-base ${s.heading}`}>{m.heading}</h2>
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full border ${
              result.risk_level === "LOW" ? "bg-slate-100 text-slate-600 border-slate-200" :
              result.risk_level === "MEDIUM" ? "bg-amber-100 text-amber-700 border-amber-200" :
              result.risk_level === "HIGH" ? "bg-orange-100 text-orange-700 border-orange-200" :
              "bg-red-100 text-red-700 border-red-200"
            }`}>
              {s.label}
            </span>
          </div>
          <p className={`mt-1 text-sm leading-relaxed ${s.body}`}>{m.body}</p>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-slate-500 italic border-t border-black/5 pt-3">
        This is a structured safety guide — not a diagnosis of your situation.
        SafeSpace cannot determine exactly what is happening.
        {result.risk_level === "IMMEDIATE" && (
          <strong className="text-red-700"> If you are in immediate danger, call 999 or 112.</strong>
        )}
      </p>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3 pt-1">
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
    <div className="space-y-6 max-w-xl">

      {/* Form */}
      {status !== "result" && (
        <form onSubmit={handleSubmit} className="space-y-4" noValidate>
          <div className="space-y-1.5">
            <label htmlFor="safety-message" className="block text-sm font-semibold text-slate-800">
              Describe your situation briefly
            </label>
            <textarea
              id="safety-message"
              name="message"
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="e.g. I was arrested and I don't know my rights…"
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none shadow-sm"
              aria-describedby="safety-hint"
              disabled={status === "loading"}
              autoComplete="off"
              autoSave="off"
            />
            <p id="safety-hint" className="text-xs text-slate-400">
              Your message is not stored. Do not include full names, ID numbers, or other identifying information.
            </p>
          </div>

          <button
            type="submit"
            disabled={!message.trim() || status === "loading"}
            className="ss-btn-primary"
            aria-busy={status === "loading"}
          >
            {status === "loading" ? (
              <>
                <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.25"/>
                  <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
                </svg>
                Checking…
              </>
            ) : "Check my situation"}
          </button>
        </form>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700" role="alert">
          We couldn&apos;t complete the safety check right now. Please try again, or go directly to{" "}
          <Link href="/support" className="underline font-medium">Support Services</Link>.
        </div>
      )}

      {/* Result */}
      {status === "result" && result && <ResultPanel result={result} />}

      {/* Start over */}
      {status === "result" && (
        <button
          onClick={handleReset}
          className="text-sm text-slate-500 hover:text-blue-700 underline transition-colors"
        >
          ← Start over
        </button>
      )}
    </div>
  );
}

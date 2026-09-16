"use client";

/**
 * AskForm — guided question experience for SafeSpace AI-assisted answers.
 *
 * Privacy rules:
 * - Question held in React state only, cleared after response.
 * - NEVER written to localStorage, sessionStorage, or cookies.
 * - No chat history is maintained.
 * - Quick Exit remains available via header.
 */

import { useState } from "react";
import Link from "next/link";
import { postAsk } from "@/lib/api";
import type { AskResponse, EvidenceStatus, RiskLevel } from "@/lib/types";

type Status = "idle" | "loading" | "result" | "error";

// ---------------------------------------------------------------------------
// Evidence status banner
// ---------------------------------------------------------------------------
const evidenceMeta: Record<EvidenceStatus, { label: string; style: string }> = {
  SUPPORTED:    { label: "Supported by verified sources",       style: "bg-emerald-50 border-emerald-200 text-emerald-800" },
  PARTIAL:      { label: "Partially supported by evidence",     style: "bg-amber-50 border-amber-200 text-amber-800" },
  INSUFFICIENT: { label: "Insufficient verified evidence",      style: "bg-slate-100 border-slate-200 text-slate-600" },
};

// ---------------------------------------------------------------------------
// Risk banner (for HIGH / IMMEDIATE)
// ---------------------------------------------------------------------------
const riskBannerMeta: Partial<Record<RiskLevel, { style: string; message: string }>> = {
  HIGH: {
    style: "bg-orange-50 border-orange-300 text-orange-900",
    message: "Your message suggests a concerning situation. Verified support services are shown below.",
  },
  IMMEDIATE: {
    style: "bg-red-50 border-red-300 text-red-900",
    message: "Based on your message, please contact a support service or call 999 / 112 if you are in immediate danger.",
  },
};

// ---------------------------------------------------------------------------
// Source card
// ---------------------------------------------------------------------------
function SourceCard({ source }: { source: import("@/lib/types").LegalSource }) {
  return (
    <div className="ss-provenance space-y-1">
      <div className="flex items-center gap-1.5">
        <svg width="10" height="10" viewBox="0 0 14 14" fill="none" aria-hidden="true">
          <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="currentColor" fillOpacity="0.35"/>
          <path d="M4.5 7L6 8.5L9.5 5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <span className="font-semibold text-emerald-900 text-sm">{source.title}</span>
      </div>
      <p className="text-emerald-700 text-xs">{source.source_type_display} · {source.publisher}</p>
      <p className="text-emerald-700 text-xs">Last verified: {source.last_verified}</p>
      {source.url && (
        <a
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-emerald-700 underline hover:no-underline"
        >
          View official source ↗
        </a>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Result display
// ---------------------------------------------------------------------------
function AskResult({ result }: { result: AskResponse }) {
  const evMeta = evidenceMeta[result.evidence_status];
  const riskBanner = riskBannerMeta[result.risk_level];

  return (
    <div className="space-y-6" data-testid="ask-result">

      {/* Risk banner for HIGH/IMMEDIATE */}
      {riskBanner && (
        <div className={`rounded-xl border p-4 text-sm font-medium ${riskBanner.style}`} role="alert">
          {riskBanner.message}
        </div>
      )}

      {/* Answer */}
      <div className="rounded-xl border border-slate-200 bg-white overflow-hidden">
        <div className="px-5 py-4 space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold text-slate-900">Answer</h2>
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full border ${evMeta.style}`}>
              {evMeta.label}
            </span>
          </div>
          <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">
            {result.answer}
          </p>
        </div>

        {/* AI disclosure */}
        {result.ai_used && (
          <div className="border-t border-blue-100 bg-blue-50 px-5 py-3">
            <p className="text-xs text-blue-700">{result.ai_disclosure}</p>
          </div>
        )}
      </div>

      {/* Sources */}
      {result.sources.length > 0 && (
        <section aria-labelledby="sources-heading" className="space-y-3">
          <div className="ss-divider-label">
            <span className="ss-section-label">Why you can trust this</span>
          </div>
          <div className="space-y-2">
            {result.sources.map((s) => (
              <SourceCard key={s.id} source={s} />
            ))}
          </div>
        </section>
      )}

      {/* Actions */}
      {result.actions.length > 0 && (
        <section aria-labelledby="actions-heading" className="space-y-3">
          <div className="ss-divider-label">
            <span className="ss-section-label">What you can do next</span>
          </div>
          <ol className="space-y-3 list-none" aria-label="Next steps">
            {result.actions.map((action) => (
              <li key={action.id} className="flex gap-3 rounded-xl border border-slate-200 bg-white p-4">
                <div className="ss-step-number shrink-0">{action.step_number}</div>
                <div className="space-y-1">
                  <p className="font-semibold text-slate-900 text-sm">{action.title}</p>
                  <p className="text-slate-600 text-sm leading-relaxed">{action.instruction}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      )}

      {/* Support services */}
      {result.support_services.length > 0 && (
        <section aria-labelledby="support-heading" className="space-y-3">
          <div className="ss-divider-label">
            <span className="ss-section-label">Where to get help</span>
          </div>
          <div className="space-y-3">
            {result.support_services.map((svc) => (
              <div key={svc.id} className="rounded-xl border border-blue-100 bg-blue-50 p-4 space-y-2">
                <div className="flex items-center justify-between gap-2">
                  <p className="font-semibold text-blue-900 text-sm">{svc.name}</p>
                  {svc.available_24_7 && (
                    <span className="text-[10px] font-bold uppercase tracking-wide text-emerald-700 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded-full">24/7</span>
                  )}
                </div>
                <p className="text-blue-700 text-xs">{svc.description}</p>
                {svc.phone && (
                  <a
                    href={`tel:${svc.phone}`}
                    className="inline-flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors"
                    aria-label={`Call ${svc.name}: ${svc.phone}`}
                  >
                    Call {svc.phone}
                  </a>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Browse link */}
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <Link href="/" className="ss-btn-secondary text-sm">Browse Journeys</Link>
        <Link href="/support" className="ss-btn-secondary text-sm">Support Services</Link>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Form
// ---------------------------------------------------------------------------
export default function AskForm() {
  const [question, setQuestion] = useState("");
  const [status, setStatus]   = useState<Status>("idle");
  const [result, setResult]   = useState<AskResponse | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setStatus("loading");
    try {
      const res = await postAsk(question);
      setResult(res);
      setStatus("result");
      setQuestion(""); // clear — privacy requirement
    } catch {
      setStatus("error");
      setQuestion("");
    }
  }

  function handleReset() {
    setQuestion("");
    setResult(null);
    setStatus("idle");
  }

  return (
    <div className="space-y-6">

      {/* Question form */}
      {status !== "result" && (
        <form onSubmit={handleSubmit} className="space-y-4 max-w-xl" noValidate>
          <div className="space-y-1.5">
            <label htmlFor="ask-question" className="block text-sm font-semibold text-slate-800">
              Your question
            </label>
            <textarea
              id="ask-question"
              name="question"
              rows={4}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. What are my rights if I am arrested?"
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none shadow-sm"
              aria-describedby="ask-hint"
              disabled={status === "loading"}
              autoComplete="off"
              autoSave="off"
            />
            <p id="ask-hint" className="text-xs text-slate-400">
              Your question is not stored. SafeSpace answers from verified Kenyan legal sources only.
            </p>
          </div>

          <button
            type="submit"
            disabled={!question.trim() || status === "loading"}
            className="ss-btn-primary"
            aria-busy={status === "loading"}
          >
            {status === "loading" ? (
              <>
                <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.25"/>
                  <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
                </svg>
                Searching verified sources…
              </>
            ) : "Ask SafeSpace"}
          </button>
        </form>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 max-w-xl" role="alert">
          We couldn&apos;t process your question right now. Please try again, or browse{" "}
          <Link href="/" className="underline font-medium">available journeys</Link>.
        </div>
      )}

      {/* Result */}
      {status === "result" && result && <AskResult result={result} />}

      {/* Reset */}
      {status === "result" && (
        <button onClick={handleReset} className="text-sm text-slate-500 hover:text-blue-700 underline transition-colors">
          ← Ask another question
        </button>
      )}
    </div>
  );
}

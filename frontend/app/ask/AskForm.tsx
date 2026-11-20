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
import type { AskResponse, EvidenceStatus, LegalSource, RiskLevel } from "@/lib/types";
import { Always247, SectionLabel, ServiceContactActions } from "@/app/components/ui";
import {
  AlertIcon, ArrowLeftIcon, ExternalIcon, ShieldCheckIcon, SparkIcon, SpinnerIcon,
} from "@/app/components/Icons";

type Status = "idle" | "loading" | "result" | "error";

// ---------------------------------------------------------------------------
// Evidence status chip
// ---------------------------------------------------------------------------
const evidenceMeta: Record<EvidenceStatus, { label: string; style: string }> = {
  SUPPORTED:    { label: "Supported by verified sources",   style: "bg-ok-bg border-ok-line text-ok-ink" },
  PARTIAL:      { label: "Partially supported by evidence", style: "bg-warn-bg border-warn-line text-warn-ink" },
  INSUFFICIENT: { label: "Insufficient verified evidence",  style: "bg-sunken border-line text-ink-soft" },
};

// ---------------------------------------------------------------------------
// Risk banner (for HIGH / IMMEDIATE)
// ---------------------------------------------------------------------------
const riskBannerMeta: Partial<Record<RiskLevel, { style: string; message: string }>> = {
  HIGH: {
    style: "bg-alert-bg border-alert-line text-alert-ink",
    message: "Your message suggests a concerning situation. Verified support services are shown below.",
  },
  IMMEDIATE: {
    style: "bg-danger-bg border-danger-line text-danger-ink",
    message: "Based on your message, please contact a support service or call 999 / 112 if you are in immediate danger.",
  },
};

// ---------------------------------------------------------------------------
// Source card
// ---------------------------------------------------------------------------
function SourceCard({ source }: { source: LegalSource }) {
  return (
    <div className="ss-provenance space-y-1">
      <div className="flex items-center gap-1.5">
        <ShieldCheckIcon size={14} className="shrink-0" />
        <span className="text-sm font-bold">{source.title}</span>
      </div>
      <p className="text-xs opacity-90">{source.source_type_display} · {source.publisher}</p>
      <p className="text-xs opacity-90">Last verified: {source.last_verified}</p>
      {source.url && (
        <a
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs font-semibold underline underline-offset-2 hover:no-underline"
        >
          View official source
          <ExternalIcon size={12} />
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
    <div className="space-y-8" data-testid="ask-result">

      {/* Risk banner for HIGH/IMMEDIATE */}
      {riskBanner && (
        <div className={`flex items-start gap-3 rounded-2xl border p-4 text-sm font-semibold ${riskBanner.style}`} role="alert">
          <AlertIcon size={18} className="mt-0.5 shrink-0" />
          <span>{riskBanner.message}</span>
        </div>
      )}

      {/* Answer */}
      <div className="ss-card overflow-hidden">
        <div className="space-y-3 p-5 sm:p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-lg font-bold tracking-tight text-ink">Answer</h2>
            <span className={`ss-chip ${evMeta.style}`}>{evMeta.label}</span>
          </div>
          <p className="whitespace-pre-wrap leading-relaxed text-ink-soft">
            {result.answer}
          </p>
        </div>

        {/* AI disclosure */}
        {result.ai_used && (
          <div className="flex items-start gap-2 border-t border-brand-line bg-brand-soft px-5 py-3 sm:px-6">
            <SparkIcon size={14} className="mt-0.5 shrink-0 text-brand-ink" />
            <p className="text-xs text-brand-ink">{result.ai_disclosure}</p>
          </div>
        )}
      </div>

      {/* Sources */}
      {result.sources.length > 0 && (
        <section aria-labelledby="sources-heading" className="space-y-3">
          <SectionLabel id="sources-heading">Why you can trust this</SectionLabel>
          <div className="grid gap-2 sm:grid-cols-2">
            {result.sources.map((s) => (
              <SourceCard key={s.id} source={s} />
            ))}
          </div>
        </section>
      )}

      {/* Actions */}
      {result.actions.length > 0 && (
        <section aria-labelledby="actions-heading" className="space-y-3">
          <SectionLabel id="actions-heading">What you can do next</SectionLabel>
          <ol className="list-none space-y-3" aria-label="Next steps">
            {result.actions.map((action) => (
              <li key={action.id} className="ss-card flex gap-4 p-4">
                <div className="ss-step-number">{action.step_number}</div>
                <div className="space-y-1">
                  <p className="font-bold text-ink">{action.title}</p>
                  <p className="text-sm leading-relaxed text-ink-soft">{action.instruction}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      )}

      {/* Support services */}
      {result.support_services.length > 0 && (
        <section aria-labelledby="support-heading" className="space-y-3">
          <SectionLabel id="support-heading">Where to get help</SectionLabel>
          <div className="space-y-3">
            {result.support_services.map((svc) => (
              <div key={svc.id} className="space-y-2.5 rounded-2xl border border-brand-line bg-brand-soft p-4">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-bold text-brand-ink">{svc.name}</p>
                  {svc.available_24_7 && <Always247 />}
                </div>
                <p className="text-xs leading-relaxed text-ink-soft">{svc.description}</p>
                <ServiceContactActions compact name={svc.name} phone={svc.phone} />
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Browse link */}
      <div className="flex flex-col gap-3 pt-2 sm:flex-row">
        <Link href="/" className="ss-btn-secondary">Browse Journeys</Link>
        <Link href="/support" className="ss-btn-secondary">Support Services</Link>
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
        <form onSubmit={handleSubmit} className="ss-card max-w-2xl space-y-4 p-5 sm:p-6" noValidate>
          <div className="space-y-2">
            <label htmlFor="ask-question" className="block font-bold text-ink">
              Your question
            </label>
            <textarea
              id="ask-question"
              name="question"
              rows={4}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. What are my rights if I am arrested?"
              className="ss-input"
              aria-describedby="ask-hint"
              disabled={status === "loading"}
              autoComplete="off"
              autoSave="off"
            />
            <p id="ask-hint" className="text-xs text-ink-faint">
              Your question is not stored. SafeSpace answers from verified Kenyan legal sources only.
            </p>
          </div>

          <button
            type="submit"
            disabled={!question.trim() || status === "loading"}
            className="ss-btn-primary w-full sm:w-auto"
            aria-busy={status === "loading"}
          >
            {status === "loading" ? (
              <>
                <SpinnerIcon />
                Searching verified sources…
              </>
            ) : "Ask SafeSpace"}
          </button>
        </form>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="flex max-w-2xl items-start gap-3 rounded-2xl border border-danger-line bg-danger-bg p-4 text-sm text-danger-ink" role="alert">
          <AlertIcon size={18} className="mt-0.5 shrink-0" />
          <span>
            We couldn&apos;t process your question right now. Please try again, or browse{" "}
            <Link href="/" className="font-semibold underline">available journeys</Link>.
          </span>
        </div>
      )}

      {/* Result */}
      {status === "result" && result && <AskResult result={result} />}

      {/* Reset */}
      {status === "result" && (
        <button
          onClick={handleReset}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-ink-soft transition-colors hover:text-brand-ink"
        >
          <ArrowLeftIcon size={15} />
          Ask another question
        </button>
      )}
    </div>
  );
}

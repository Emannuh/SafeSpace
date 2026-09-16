/**
 * SafeSpace landing page.
 * Journey cards are fetched from the Django API — no legal content is hard-coded.
 */

import Link from "next/link";
import { fetchJourneys } from "@/lib/api";
import type { Journey } from "@/lib/types";
import { ErrorState } from "./components/StateViews";

const journeyMeta: Record<string, { icon: string; colour: string }> = {
  "child-justice":       { icon: "⚖️", colour: "bg-violet-50 border-violet-200" },
  "teenage-pregnancy":   { icon: "🎓", colour: "bg-sky-50 border-sky-200" },
  "sexual-exploitation": { icon: "🛡️", colour: "bg-teal-50 border-teal-200" },
};

async function JourneyCards() {
  let journeys: Journey[] = [];
  let error = false;

  try {
    journeys = await fetchJourneys();
  } catch {
    error = true;
  }

  if (error) {
    return <ErrorState message="We couldn't load the SafeSpace journeys right now. Please try again later." />;
  }

  if (journeys.length === 0) {
    return <p className="text-slate-500 text-sm">No journeys are available right now. Please check back soon.</p>;
  }

  return (
    <ul className="space-y-3" role="list">
      {journeys.map((journey) => {
        const meta = journeyMeta[journey.slug] ?? { icon: "📋", colour: "bg-slate-50 border-slate-200" };
        return (
          <li key={journey.slug}>
            <Link
              href={`/journeys/${journey.slug}`}
              className="group block rounded-xl border bg-white p-4 hover:border-blue-300 hover:shadow-md transition-all duration-150 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
              aria-label={`Explore ${journey.name}`}
            >
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-xl border flex items-center justify-center text-2xl shrink-0 ${meta.colour}`} aria-hidden="true">
                  {meta.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-slate-900 group-hover:text-blue-700 transition-colors">{journey.name}</p>
                  <p className="mt-0.5 text-sm text-slate-500 line-clamp-1">{journey.description}</p>
                </div>
                <svg className="w-5 h-5 text-slate-300 group-hover:text-blue-400 shrink-0 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

export default function HomePage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12 space-y-12">

      {/* ── Hero ── */}
      <section aria-labelledby="hero-heading" className="space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 border border-blue-200 rounded-full text-xs font-medium text-blue-700">
          <span aria-hidden="true">🇰🇪</span>
          Built for young people in Kenya
        </div>
        <h1 id="hero-heading" className="text-3xl sm:text-4xl font-bold text-slate-900 leading-tight tracking-tight">
          Understand your rights.<br />
          <span className="text-blue-600">Know your options.</span>
        </h1>
        <p className="text-slate-600 text-lg max-w-xl leading-relaxed">
          SafeSpace gives you clear, verified information about your rights —
          and practical steps you can take. No account required.
        </p>
        <p className="flex items-center gap-2 text-sm text-slate-500">
          <span className="w-4 h-4 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 text-xs" aria-hidden="true">✓</span>
          Built around verified Kenyan legal and institutional sources
        </p>
      </section>

      {/* ── Journeys ── */}
      <section aria-labelledby="journeys-heading" className="space-y-4">
        <div className="ss-divider-label">
          <span className="ss-section-label">Choose your journey</span>
        </div>
        {/* async Server Component */}
        <JourneyCards />
      </section>

      {/* ── Not sure ── */}
      <section aria-labelledby="not-sure-heading" className="rounded-2xl border border-slate-200 bg-white p-6 space-y-3">
        <h2 id="not-sure-heading" className="font-semibold text-slate-900">
          Not sure where to start?
        </h2>
        <p className="text-sm text-slate-500 leading-relaxed">
          Describe your situation briefly and SafeSpace will guide you to
          the most relevant rights information and support.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 pt-1">
          <Link href="/safety" className="ss-btn-primary">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="currentColor" fillOpacity="0.8"/>
            </svg>
            Safety Check
          </Link>
          <Link href="/support" className="ss-btn-secondary">
            View Support Services
          </Link>
        </div>
      </section>

      {/* ── Privacy footnote ── */}
      <aside className="text-xs text-slate-400 border-t border-slate-100 pt-4">
        No account required. SafeSpace minimises personal-data collection.
        The Safety Check does not store your message.
      </aside>
    </div>
  );
}

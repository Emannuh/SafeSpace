/**
 * SafeSpace landing page.
 *
 * Journey cards are fetched from the Django API.
 * No legal content is hard-coded here.
 */

import Link from "next/link";
import { fetchJourneys } from "@/lib/api";
import type { Journey } from "@/lib/types";
import { ErrorState } from "./components/StateViews";

// Journey icon mapping — purely presentational, not content
const journeyIcons: Record<string, string> = {
  "child-justice": "⚖️",
  "teenage-pregnancy": "🎓",
  "sexual-exploitation": "🛡️",
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
    return (
      <ErrorState message="We couldn't load the SafeSpace journeys right now. Please try again later." />
    );
  }

  if (journeys.length === 0) {
    return (
      <p className="text-slate-500 text-sm">
        No journeys are available right now. Please check back soon.
      </p>
    );
  }

  return (
    <ul className="space-y-4" role="list">
      {journeys.map((journey) => (
        <li key={journey.slug}>
          <Link
            href={`/journeys/${journey.slug}`}
            className="
              block rounded-xl border border-slate-200 bg-white p-5
              hover:border-blue-300 hover:shadow-sm
              transition-all duration-150
              focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600
            "
            aria-label={`Start ${journey.name} journey`}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl leading-none mt-0.5" aria-hidden="true">
                {journeyIcons[journey.slug] ?? "📋"}
              </span>
              <div>
                <h2 className="text-base font-semibold text-slate-900">
                  {journey.name}
                </h2>
                <p className="mt-1 text-sm text-slate-500 line-clamp-2">
                  {journey.description}
                </p>
              </div>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}

export default function HomePage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10 space-y-10">
      {/* Hero */}
      <section aria-labelledby="hero-heading">
        <h1
          id="hero-heading"
          className="text-2xl sm:text-3xl font-bold text-slate-900 leading-tight"
        >
          Understand your rights.
          <br />
          <span className="text-blue-700">Know your options.</span>
        </h1>
        <p className="mt-3 text-slate-600 max-w-xl">
          SafeSpace gives young people in Kenya clear, verified information about
          their rights — and practical next steps. No account required.
        </p>
        <p className="mt-2 text-sm text-slate-500">
          Every piece of information comes from a verified legal source.
        </p>
      </section>

      {/* Journeys */}
      <section aria-labelledby="journeys-heading">
        <h2
          id="journeys-heading"
          className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4"
        >
          Choose your journey
        </h2>
        {/* @ts-expect-error — async Server Component */}
        <JourneyCards />
      </section>

      {/* Not sure */}
      <section
        aria-labelledby="not-sure-heading"
        className="rounded-xl border border-slate-200 bg-white p-5"
      >
        <h2
          id="not-sure-heading"
          className="text-base font-semibold text-slate-900"
        >
          Not sure where your situation fits?
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          That&apos;s okay. You can start with a Safety Check — describe your
          situation briefly and SafeSpace will help guide you to the most relevant
          information.
        </p>
        <div className="mt-4 flex flex-col sm:flex-row gap-3">
          <Link
            href="/safety"
            className="
              inline-flex items-center justify-center
              bg-blue-600 hover:bg-blue-700 text-white
              text-sm font-medium px-4 py-2 rounded-lg
              transition-colors duration-150
            "
          >
            Safety Check
          </Link>
          <Link
            href="/support"
            className="
              inline-flex items-center justify-center
              border border-slate-300 hover:border-blue-300
              text-sm font-medium text-slate-700 px-4 py-2 rounded-lg
              transition-colors duration-150
            "
          >
            View Support Services
          </Link>
        </div>
      </section>

      {/* Privacy note */}
      <aside className="text-xs text-slate-400 border-t border-slate-200 pt-4">
        SafeSpace does not require an account. We aim to minimise personal-data
        collection. The Safety Check does not store your message.
      </aside>
    </div>
  );
}

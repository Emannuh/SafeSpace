/**
 * SafeSpace landing page.
 * Journey cards are fetched from the Django API — no legal content is hard-coded.
 */

import Link from "next/link";
import { fetchJourneys } from "@/lib/api";
import type { Journey } from "@/lib/types";
import { ErrorState } from "./components/StateViews";
import { Container, SectionLabel } from "./components/ui";
import {
  ArrowRightIcon, CheckIcon, DocIcon, GraduationIcon, LockIcon,
  ScaleIcon, ShieldIcon, SparkIcon,
} from "./components/Icons";

type IconComp = typeof ScaleIcon;

const journeyMeta: Record<string, { Icon: IconComp; tint: string }> = {
  "child-justice":       { Icon: ScaleIcon,      tint: "bg-violet-500/10 text-violet-600 dark:text-violet-300" },
  "teenage-pregnancy":   { Icon: GraduationIcon, tint: "bg-sky-500/10 text-sky-600 dark:text-sky-300" },
  "sexual-exploitation": { Icon: ShieldIcon,     tint: "bg-teal-500/10 text-teal-600 dark:text-teal-300" },
};
const fallbackMeta = { Icon: DocIcon, tint: "bg-sunken text-ink-soft" };

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
    return <p className="text-ink-soft text-sm">No journeys are available right now. Please check back soon.</p>;
  }

  return (
    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" role="list">
      {journeys.map((journey) => {
        const { Icon, tint } = journeyMeta[journey.slug] ?? fallbackMeta;
        return (
          <li key={journey.slug} className="flex">
            <Link
              href={`/journeys/${journey.slug}`}
              className="ss-card-link group flex w-full flex-col gap-4 p-5"
              aria-label={`Explore ${journey.name}`}
            >
              <span className={`flex h-12 w-12 items-center justify-center rounded-2xl ${tint}`}>
                <Icon size={24} />
              </span>
              <span className="flex-1 space-y-1.5">
                <span className="block text-lg font-bold tracking-tight text-ink group-hover:text-brand-ink transition-colors">
                  {journey.name}
                </span>
                <span className="block text-sm leading-relaxed text-ink-soft line-clamp-3">
                  {journey.description}
                </span>
              </span>
              <span className="inline-flex items-center gap-1.5 text-sm font-semibold text-brand-ink">
                Explore
                <ArrowRightIcon size={16} className="transition-transform group-hover:translate-x-1" />
              </span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

const pillars = [
  { title: "Understand", body: "Plain-language explanations of your rights." },
  { title: "Verify",     body: "Every answer links to its official Kenyan source." },
  { title: "Act",        body: "Clear next steps you can take today." },
  { title: "Protect",    body: "Verified helplines and support services." },
];

export default function HomePage() {
  return (
    <div className="relative">
      {/* Decorative backdrop */}
      <div
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[520px] overflow-hidden"
        aria-hidden="true"
      >
        <div className="absolute -top-40 left-1/2 h-[480px] w-[880px] -translate-x-1/2 rounded-full bg-brand/15 blur-3xl" />
        <div className="absolute -top-10 right-[8%] h-64 w-64 rounded-full bg-teal-400/15 blur-3xl" />
      </div>

      <Container wide className="space-y-16 pt-12 pb-4 sm:pt-20">

        {/* ── Hero ── */}
        <section aria-labelledby="hero-heading" className="max-w-2xl space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-brand-line bg-card/70 px-3.5 py-1.5 text-xs font-semibold text-brand-ink backdrop-blur">
            <span className="flex gap-0.5" aria-hidden="true">
              <span className="h-2.5 w-1 rounded-full bg-black dark:bg-white" />
              <span className="h-2.5 w-1 rounded-full bg-red-600" />
              <span className="h-2.5 w-1 rounded-full bg-green-700" />
            </span>
            Built for young people in Kenya
          </div>
          <h1
            id="hero-heading"
            className="text-4xl font-extrabold leading-[1.08] tracking-tight text-ink text-balance sm:text-6xl"
          >
            Understand your rights.{" "}
            <span className="bg-linear-to-r from-brand to-teal-500 bg-clip-text text-transparent dark:from-brand-ink dark:to-teal-300">
              Know your options.
            </span>
          </h1>
          <p className="max-w-xl text-lg leading-relaxed text-ink-soft text-pretty sm:text-xl">
            SafeSpace gives you clear, verified information about your rights —
            and practical steps you can take. No account required.
          </p>
          <div className="flex flex-col gap-3 pt-1 sm:flex-row">
            <Link href="/ask" className="ss-btn-primary px-6">
              <SparkIcon size={16} />
              Ask a question
            </Link>
            <Link href="/safety" className="ss-btn-secondary px-6">
              <ShieldIcon size={16} />
              Safety Check
            </Link>
          </div>
          <p className="flex items-center gap-2 text-sm text-ink-soft">
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-ok-bg text-ok-ink" aria-hidden="true">
              <CheckIcon size={12} strokeWidth={3} />
            </span>
            Built around verified Kenyan legal and institutional sources
          </p>
        </section>

        {/* ── Journeys ── */}
        <section aria-labelledby="journeys-heading" className="space-y-5">
          <SectionLabel id="journeys-heading">Choose your journey</SectionLabel>
          {/* async Server Component */}
          <JourneyCards />
        </section>

        {/* ── How it works ── */}
        <section aria-labelledby="how-heading" className="space-y-5">
          <SectionLabel id="how-heading">How SafeSpace helps</SectionLabel>
          <ol className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4" role="list">
            {pillars.map((p, i) => (
              <li key={p.title} className="ss-card space-y-2 p-5">
                <span className="text-xs font-bold tabular-nums text-brand-ink">0{i + 1}</span>
                <p className="font-bold text-ink">{p.title}</p>
                <p className="text-sm leading-relaxed text-ink-soft">{p.body}</p>
              </li>
            ))}
          </ol>
        </section>

        {/* ── Not sure ── */}
        <section
          aria-labelledby="not-sure-heading"
          className="relative overflow-hidden rounded-3xl bg-linear-to-br from-brand to-brand-strong p-7 text-white sm:p-10"
        >
          <div className="absolute -right-16 -top-16 h-56 w-56 rounded-full bg-white/10 blur-2xl" aria-hidden="true" />
          <div className="relative max-w-xl space-y-3">
            <h2 id="not-sure-heading" className="text-2xl font-extrabold tracking-tight">
              Not sure where to start?
            </h2>
            <p className="leading-relaxed text-white/85">
              Describe your situation briefly and SafeSpace will guide you to
              the most relevant rights information and support.
            </p>
            <div className="flex flex-col gap-3 pt-3 sm:flex-row">
              <Link
                href="/safety"
                className="inline-flex min-h-[44px] items-center justify-center gap-2 rounded-full bg-white px-6 text-[15px] font-semibold text-brand-strong transition-transform hover:bg-white/90 active:scale-[0.98]"
              >
                <ShieldIcon size={16} />
                Safety Check
              </Link>
              <Link
                href="/support"
                className="inline-flex min-h-[44px] items-center justify-center gap-2 rounded-full border border-white/30 px-6 text-[15px] font-semibold text-white transition-colors hover:bg-white/10"
              >
                View Support Services
              </Link>
            </div>
          </div>
        </section>

        {/* ── Privacy footnote ── */}
        <aside className="flex items-start gap-3 rounded-2xl border border-line bg-card p-4 text-sm text-ink-soft">
          <LockIcon size={18} className="mt-0.5 shrink-0 text-ink-faint" />
          <p>
            No account required. SafeSpace minimises personal-data collection.
            The Safety Check does not store your message.
          </p>
        </aside>
      </Container>
    </div>
  );
}

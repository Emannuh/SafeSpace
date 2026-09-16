import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchTopics, fetchJourneys } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import RiskBadge from "@/app/components/RiskBadge";
import type { RiskLevel } from "@/lib/types";

interface Props {
  params: Promise<{ journeySlug: string }>;
}

export default async function JourneyPage({ params }: Props) {
  const { journeySlug } = await params;

  let topics = null;
  let journeyName = journeySlug.replace(/-/g, " ");
  let journeyDescription = "";
  let fetchError = false;

  try {
    const [allJourneys, topicsData] = await Promise.all([
      fetchJourneys(),
      fetchTopics(journeySlug),
    ]);

    if (topicsData === null) notFound();

    topics = topicsData;
    const journey = allJourneys.find((j) => j.slug === journeySlug);
    if (journey) {
      journeyName = journey.name;
      journeyDescription = journey.description;
    }
  } catch {
    fetchError = true;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb">
        <ol className="flex items-center gap-1.5 text-sm text-slate-500">
          <li><Link href="/" className="hover:text-blue-700 transition-colors">SafeSpace</Link></li>
          <li aria-hidden="true" className="text-slate-300">/</li>
          <li className="text-slate-800 font-medium truncate" aria-current="page">{journeyName}</li>
        </ol>
      </nav>

      {/* Journey header */}
      <header className="space-y-2">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{journeyName}</h1>
        {journeyDescription && (
          <p className="text-slate-600 leading-relaxed max-w-xl">{journeyDescription}</p>
        )}
      </header>

      {/* Topics */}
      <section aria-labelledby="topics-heading" className="space-y-4">
        <div className="ss-divider-label">
          <span className="ss-section-label">Topics in this journey</span>
        </div>

        {fetchError && <ErrorState message="We couldn't load the topics right now. Please try again later." />}

        {!fetchError && topics !== null && topics.length === 0 && (
          <EmptyState message="No topics are available for this journey yet." />
        )}

        {!fetchError && topics && topics.length > 0 && (
          <ul className="space-y-3" role="list">
            {topics.map((topic) => (
              <li key={topic.slug}>
                <Link
                  href={`/journeys/${journeySlug}/topics/${topic.slug}`}
                  className="group flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 hover:border-blue-300 hover:shadow-md transition-all duration-150 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
                  aria-label={`Explore topic: ${topic.title}`}
                >
                  <div className="flex-1 min-w-0 space-y-1">
                    <p className="font-semibold text-slate-900 group-hover:text-blue-700 transition-colors">
                      {topic.title}
                    </p>
                    <p className="text-sm text-slate-500 line-clamp-2 leading-relaxed">
                      {topic.description}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <RiskBadge level={topic.default_risk_level as RiskLevel} />
                    <svg className="w-4 h-4 text-slate-300 group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Safety prompt */}
      <aside className="rounded-xl border border-amber-200 bg-amber-50 p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <p className="text-sm text-amber-800">
          <strong>Concerned about your safety right now?</strong>
        </p>
        <Link href="/safety" className="ss-btn-primary text-xs shrink-0">
          Safety Check
        </Link>
      </aside>
    </div>
  );
}

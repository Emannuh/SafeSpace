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

  // Fetch journey info (from journey list) and topics in parallel
  let topics = null;
  let journeyName = journeySlug;
  let journeyDescription = "";
  let fetchError = false;

  try {
    const [allJourneys, topicsData] = await Promise.all([
      fetchJourneys(),
      fetchTopics(journeySlug),
    ]);

    if (topicsData === null) {
      // 404 from API — journey not found or inactive
      notFound();
    }

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
      <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
        <ol className="flex items-center gap-2">
          <li>
            <Link href="/" className="hover:text-blue-700 transition-colors">
              SafeSpace
            </Link>
          </li>
          <li aria-hidden="true">/</li>
          <li className="text-slate-800 font-medium" aria-current="page">
            {journeyName}
          </li>
        </ol>
      </nav>

      {/* Journey header */}
      <header>
        <h1 className="text-2xl font-bold text-slate-900">{journeyName}</h1>
        {journeyDescription && (
          <p className="mt-2 text-slate-600">{journeyDescription}</p>
        )}
      </header>

      {/* Topics */}
      <section aria-labelledby="topics-heading">
        <h2
          id="topics-heading"
          className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4"
        >
          Topics in this journey
        </h2>

        {fetchError && (
          <ErrorState message="We couldn't load the topics right now. Please try again later." />
        )}

        {!fetchError && topics !== null && topics.length === 0 && (
          <EmptyState message="No topics are available for this journey yet." />
        )}

        {!fetchError && topics && topics.length > 0 && (
          <ul className="space-y-3" role="list">
            {topics.map((topic) => (
              <li key={topic.slug}>
                <Link
                  href={`/journeys/${journeySlug}/topics/${topic.slug}`}
                  className="
                    block rounded-xl border border-slate-200 bg-white p-4
                    hover:border-blue-300 hover:shadow-sm
                    transition-all duration-150
                    focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600
                  "
                  aria-label={`Explore topic: ${topic.title}`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold text-slate-900">
                        {topic.title}
                      </h3>
                      <p className="mt-1 text-sm text-slate-500 line-clamp-2">
                        {topic.description}
                      </p>
                    </div>
                    <RiskBadge
                      level={topic.default_risk_level as RiskLevel}
                      className="shrink-0"
                    />
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

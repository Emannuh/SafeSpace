import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchTopics, fetchJourneys } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import RiskBadge from "@/app/components/RiskBadge";
import { Breadcrumbs, Container, PageHeader, SafetyPrompt, SectionLabel } from "@/app/components/ui";
import { ArrowRightIcon } from "@/app/components/Icons";
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
    <Container className="space-y-10 py-10">
      <Breadcrumbs items={[{ label: "SafeSpace", href: "/" }, { label: journeyName }]} />

      <PageHeader eyebrow="Journey" title={journeyName} description={journeyDescription || undefined} />

      {/* Topics */}
      <section aria-labelledby="topics-heading" className="space-y-4">
        <SectionLabel id="topics-heading">Topics in this journey</SectionLabel>

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
                  className="ss-card-link group flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:gap-5"
                  aria-label={`Explore topic: ${topic.title}`}
                >
                  <div className="min-w-0 flex-1 space-y-1.5">
                    <p className="text-base font-bold tracking-tight text-ink transition-colors group-hover:text-brand-ink">
                      {topic.title}
                    </p>
                    <p className="text-sm leading-relaxed text-ink-soft line-clamp-2">
                      {topic.description}
                    </p>
                  </div>
                  <div className="flex shrink-0 items-center justify-between gap-3">
                    <RiskBadge level={topic.default_risk_level as RiskLevel} />
                    <span className="flex h-9 w-9 items-center justify-center rounded-full bg-sunken text-ink-faint transition-colors group-hover:bg-brand group-hover:text-white">
                      <ArrowRightIcon size={16} />
                    </span>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <SafetyPrompt />
    </Container>
  );
}

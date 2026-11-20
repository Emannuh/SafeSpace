import { notFound } from "next/navigation";
import { fetchRights, fetchActions, fetchTopics } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import RiskBadge from "@/app/components/RiskBadge";
import VerifiedBadge from "@/app/components/VerifiedBadge";
import {
  Always247, Breadcrumbs, Container, PageHeader, SafetyPrompt, SectionLabel, ServiceContactActions,
} from "@/app/components/ui";
import { ArrowRightIcon, ExternalIcon, InfoIcon } from "@/app/components/Icons";
import type { ActionPath, RightsRecord, RiskLevel } from "@/lib/types";

interface Props {
  params: Promise<{ journeySlug: string; topicSlug: string }>;
}

/* ─── Source provenance ─── */
function SourceBlock({ record }: { record: RightsRecord }) {
  return (
    <div className="ss-provenance space-y-2.5">
      <div className="flex flex-wrap items-center gap-2">
        <VerifiedBadge />
        <span className="text-xs opacity-90">Last verified: {record.last_verified}</span>
      </div>
      <div className="space-y-0.5">
        <p className="text-sm font-bold">{record.source.title}</p>
        <p className="text-xs opacity-90">{record.source.source_type_display} · {record.source.publisher}</p>
        <p className="text-xs opacity-90">
          {record.legal_reference}
          {record.section_reference ? ` — ${record.section_reference}` : ""}
        </p>
      </div>
      {record.source.url && (
        <a
          href={record.source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs font-semibold underline underline-offset-2 hover:no-underline"
          aria-label={`View source: ${record.source.title} (opens in new tab)`}
        >
          View official source
          <ExternalIcon size={12} />
        </a>
      )}
    </div>
  );
}

/* ─── Rights cards (UNDERSTAND + VERIFY) ─── */
function RightsSection({ rights }: { rights: RightsRecord[] }) {
  if (rights.length === 0) {
    return <EmptyState message="No verified rights information is available for this topic yet." />;
  }

  return (
    <div className="space-y-5">
      {rights.map((record) => (
        <article
          key={record.record_code}
          className="ss-card overflow-hidden"
          aria-labelledby={`record-${record.record_code}-title`}
        >
          {/* Record header */}
          <div className="space-y-3 p-5 sm:p-6">
            <div className="flex flex-col-reverse items-start gap-2 sm:flex-row sm:justify-between sm:gap-4">
              <h3
                id={`record-${record.record_code}-title`}
                className="text-lg font-bold leading-snug tracking-tight text-ink"
              >
                {record.title}
              </h3>
              <RiskBadge level={record.risk_level as RiskLevel} className="shrink-0" />
            </div>
            <p className="leading-relaxed text-ink-soft">
              {record.plain_language_summary}
            </p>
            {record.next_step_text && (
              <p className="flex items-start gap-2 rounded-xl bg-brand-soft px-3.5 py-2.5 text-sm font-semibold text-brand-ink">
                <ArrowRightIcon size={16} className="mt-0.5 shrink-0" />
                {record.next_step_text}
              </p>
            )}
          </div>

          {/* Provenance strip */}
          <div className="border-t border-line bg-sunken/50 px-5 py-4 sm:px-6">
            <SourceBlock record={record} />
          </div>

          {/* Limitations */}
          {record.limitations && (
            <div className="flex items-start gap-2 border-t border-line px-5 py-3 sm:px-6">
              <InfoIcon size={14} className="mt-0.5 shrink-0 text-ink-faint" />
              <p className="text-xs italic leading-relaxed text-ink-faint">{record.limitations}</p>
            </div>
          )}
        </article>
      ))}
    </div>
  );
}

/* ─── Action steps (ACT + PROTECT) ─── */
function ActionSection({ actions }: { actions: ActionPath[] }) {
  if (actions.length === 0) {
    return <EmptyState message="No verified next steps are available for this topic yet." />;
  }

  return (
    <ol className="relative list-none space-y-4" aria-label="Verified next steps">
      {/* Timeline rail */}
      <span className="absolute bottom-6 left-[1.0625rem] top-6 w-px bg-line" aria-hidden="true" />
      {actions.map((action) => (
        <li key={action.id} className="relative flex gap-4">
          <div className="ss-step-number relative mt-4 ring-4 ring-canvas" aria-label={`Step ${action.step_number}`}>
            {action.step_number}
          </div>

          <div className="ss-card min-w-0 flex-1 space-y-2 p-5">
            <p className="font-bold leading-snug text-ink">{action.title}</p>
            <p className="text-sm leading-relaxed text-ink-soft">{action.instruction}</p>

            {/* PROTECT — linked support service */}
            {action.support_service && (
              <div className="mt-3 space-y-2.5 rounded-xl border border-brand-line bg-brand-soft p-4">
                <div className="flex items-start justify-between gap-2">
                  <p className="text-sm font-bold text-brand-ink">{action.support_service.name}</p>
                  {action.support_service.available_24_7 && <Always247 />}
                </div>
                <p className="text-xs leading-relaxed text-ink-soft">{action.support_service.description}</p>
                <ServiceContactActions
                  compact
                  name={action.support_service.name}
                  phone={action.support_service.phone}
                  whatsapp={action.support_service.whatsapp}
                  website={action.support_service.website}
                />
              </div>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}

/* ─── Page ─── */
export default async function TopicPage({ params }: Props) {
  const { journeySlug, topicSlug } = await params;

  let rights: RightsRecord[] = [];
  let actions: ActionPath[] = [];
  let topicTitle = topicSlug.replace(/-/g, " ");
  let topicDescription = "";
  let fetchError = false;

  try {
    const [rightsData, actionsData, allTopics] = await Promise.all([
      fetchRights(journeySlug, topicSlug),
      fetchActions(journeySlug, topicSlug),
      fetchTopics(journeySlug),
    ]);

    if (rightsData === null && actionsData === null) notFound();

    rights  = rightsData  ?? [];
    actions = actionsData ?? [];

    const topic = allTopics?.find((t) => t.slug === topicSlug);
    if (topic) {
      topicTitle       = topic.title;
      topicDescription = topic.description;
    }
  } catch {
    fetchError = true;
  }

  return (
    <Container className="space-y-12 py-10">
      <Breadcrumbs
        items={[
          { label: "SafeSpace", href: "/" },
          { label: journeySlug.replace(/-/g, " "), href: `/journeys/${journeySlug}`, capitalize: true },
          { label: topicTitle },
        ]}
      />

      <PageHeader eyebrow="Topic" title={topicTitle} description={topicDescription || undefined} />

      {fetchError && (
        <ErrorState message="We couldn't load this information right now. Please try again later." />
      )}

      {!fetchError && (
        <>
          {/* UNDERSTAND + VERIFY */}
          <section aria-labelledby="understand-heading" className="space-y-4">
            <SectionLabel id="understand-heading">Understand — Your rights</SectionLabel>
            <RightsSection rights={rights} />
          </section>

          {/* ACT + PROTECT */}
          <section aria-labelledby="act-heading" className="space-y-4">
            <SectionLabel id="act-heading">Next steps — What you can do</SectionLabel>
            <ActionSection actions={actions} />
          </section>
        </>
      )}

      <SafetyPrompt />
    </Container>
  );
}

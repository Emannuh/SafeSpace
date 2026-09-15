import Link from "next/link";
import { notFound } from "next/navigation";
import { fetchRights, fetchActions, fetchTopics } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import RiskBadge from "@/app/components/RiskBadge";
import VerifiedBadge from "@/app/components/VerifiedBadge";
import type { ActionPath, RightsRecord, RiskLevel } from "@/lib/types";

interface Props {
  params: Promise<{ journeySlug: string; topicSlug: string }>;
}

// ---------------------------------------------------------------------------
// Source provenance block
// ---------------------------------------------------------------------------
function SourceBlock({ record }: { record: RightsRecord }) {
  return (
    <div className="mt-3 rounded-lg bg-slate-50 border border-slate-200 p-3 text-xs space-y-1">
      <div className="flex items-center gap-2">
        <VerifiedBadge />
        <span className="text-slate-500">
          Last verified: {record.last_verified}
        </span>
      </div>
      <p className="text-slate-700 font-medium">{record.source.title}</p>
      <p className="text-slate-500">
        {record.source.source_type_display} · {record.source.publisher}
      </p>
      <p className="text-slate-600">
        {record.legal_reference}
        {record.section_reference ? ` — ${record.section_reference}` : ""}
      </p>
      {record.source.url && (
        <a
          href={record.source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:underline"
          aria-label={`View source: ${record.source.title} (opens in new tab)`}
        >
          View source ↗
        </a>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Rights cards (UNDERSTAND + VERIFY)
// ---------------------------------------------------------------------------
function RightsSection({ rights }: { rights: RightsRecord[] }) {
  if (rights.length === 0) {
    return (
      <EmptyState message="No verified rights information is available for this topic yet." />
    );
  }

  return (
    <div className="space-y-6">
      {rights.map((record) => (
        <article
          key={record.record_code}
          className="rounded-xl border border-slate-200 bg-white p-5 space-y-3"
          aria-labelledby={`record-${record.record_code}-title`}
        >
          {/* UNDERSTAND */}
          <div>
            <div className="flex items-start justify-between gap-3">
              <h3
                id={`record-${record.record_code}-title`}
                className="font-semibold text-slate-900"
              >
                {record.title}
              </h3>
              <RiskBadge
                level={record.risk_level as RiskLevel}
                className="shrink-0"
              />
            </div>
            <p className="mt-2 text-slate-700 text-sm leading-relaxed">
              {record.plain_language_summary}
            </p>
          </div>

          {/* VERIFY — source provenance */}
          <SourceBlock record={record} />

          {/* Limitations */}
          {record.limitations && (
            <p className="text-xs text-slate-500 italic">
              {record.limitations}
            </p>
          )}
        </article>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Action steps (ACT)
// ---------------------------------------------------------------------------
function ActionSection({ actions }: { actions: ActionPath[] }) {
  if (actions.length === 0) {
    return (
      <EmptyState message="No verified next steps are available for this topic yet." />
    );
  }

  return (
    <ol className="space-y-4 list-none" aria-label="Next steps">
      {actions.map((action) => (
        <li
          key={action.id}
          className="flex gap-4 rounded-xl border border-slate-200 bg-white p-4"
        >
          {/* Step number */}
          <div
            className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-sm"
            aria-hidden="true"
          >
            {action.step_number}
          </div>

          <div className="space-y-2 flex-1">
            <p className="font-semibold text-slate-900 text-sm">
              {action.title}
            </p>
            <p className="text-sm text-slate-600 leading-relaxed">
              {action.instruction}
            </p>

            {/* PROTECT — linked support service */}
            {action.support_service && (
              <div className="rounded-lg bg-blue-50 border border-blue-100 p-3 text-sm space-y-1">
                <p className="font-semibold text-blue-900">
                  {action.support_service.name}
                </p>
                <p className="text-blue-700 text-xs">
                  {action.support_service.description}
                </p>
                {action.support_service.phone && (
                  <a
                    href={`tel:${action.support_service.phone}`}
                    className="inline-flex items-center gap-1 text-blue-700 font-medium hover:underline"
                    aria-label={`Call ${action.support_service.name}: ${action.support_service.phone}`}
                  >
                    📞 {action.support_service.phone}
                    {action.support_service.available_24_7 && (
                      <span className="text-xs text-blue-500 ml-1">(24/7)</span>
                    )}
                  </a>
                )}
                {action.support_service.website && (
                  <a
                    href={action.support_service.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-xs text-blue-600 hover:underline"
                    aria-label={`Visit ${action.support_service.name} website (opens in new tab)`}
                  >
                    {action.support_service.website} ↗
                  </a>
                )}
              </div>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export default async function TopicPage({ params }: Props) {
  const { journeySlug, topicSlug } = await params;

  let rights: RightsRecord[] = [];
  let actions: ActionPath[] = [];
  let topicTitle = topicSlug;
  let topicDescription = "";
  let fetchError = false;

  try {
    const [rightsData, actionsData, allTopics] = await Promise.all([
      fetchRights(journeySlug, topicSlug),
      fetchActions(journeySlug, topicSlug),
      fetchTopics(journeySlug),
    ]);

    if (rightsData === null && actionsData === null) {
      notFound();
    }

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
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-10">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="text-sm text-slate-500">
        <ol className="flex items-center gap-2 flex-wrap">
          <li>
            <Link href="/" className="hover:text-blue-700 transition-colors">
              SafeSpace
            </Link>
          </li>
          <li aria-hidden="true">/</li>
          <li>
            <Link
              href={`/journeys/${journeySlug}`}
              className="hover:text-blue-700 transition-colors capitalize"
            >
              {journeySlug.replace(/-/g, " ")}
            </Link>
          </li>
          <li aria-hidden="true">/</li>
          <li className="text-slate-800 font-medium" aria-current="page">
            {topicTitle}
          </li>
        </ol>
      </nav>

      {/* Topic header */}
      <header>
        <h1 className="text-2xl font-bold text-slate-900">{topicTitle}</h1>
        {topicDescription && (
          <p className="mt-2 text-slate-600">{topicDescription}</p>
        )}
      </header>

      {fetchError && (
        <ErrorState message="We couldn't load this information right now. Please try again later." />
      )}

      {!fetchError && (
        <>
          {/* UNDERSTAND + VERIFY */}
          <section aria-labelledby="understand-heading">
            <h2
              id="understand-heading"
              className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2"
            >
              <span aria-hidden="true">📋</span> Understand — What are my rights?
            </h2>
            <RightsSection rights={rights} />
          </section>

          {/* ACT + PROTECT */}
          <section aria-labelledby="act-heading">
            <h2
              id="act-heading"
              className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2"
            >
              <span aria-hidden="true">👣</span> Next steps
            </h2>
            <ActionSection actions={actions} />
          </section>
        </>
      )}

      {/* Safety check prompt */}
      <aside className="rounded-xl border border-amber-200 bg-amber-50 p-4">
        <p className="text-sm text-amber-800">
          <strong>Concerned about your safety right now?</strong>{" "}
          <Link
            href="/safety"
            className="underline hover:text-amber-900 transition-colors"
          >
            Use the Safety Check
          </Link>{" "}
          to get guidance on the most relevant support.
        </p>
      </aside>
    </div>
  );
}

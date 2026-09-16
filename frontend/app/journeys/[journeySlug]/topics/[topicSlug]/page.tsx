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

/* ─── Source provenance ─── */
function SourceBlock({ record }: { record: RightsRecord }) {
  return (
    <div className="ss-provenance space-y-2">
      <div className="flex flex-wrap items-center gap-2">
        <VerifiedBadge />
        <span className="text-emerald-700 text-xs">Last verified: {record.last_verified}</span>
      </div>
      <div className="space-y-0.5">
        <p className="font-semibold text-emerald-900 text-sm">{record.source.title}</p>
        <p className="text-emerald-700 text-xs">{record.source.source_type_display} · {record.source.publisher}</p>
        <p className="text-emerald-800 text-xs">
          {record.legal_reference}
          {record.section_reference ? ` — ${record.section_reference}` : ""}
        </p>
      </div>
      {record.source.url && (
        <a
          href={record.source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs text-emerald-700 underline hover:no-underline"
          aria-label={`View source: ${record.source.title} (opens in new tab)`}
        >
          View official source
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden="true">
            <path d="M7 1H9V3M5.5 4.5L9 1M4 2H2V8H8V6" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
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
          className="rounded-xl border border-slate-200 bg-white overflow-hidden"
          aria-labelledby={`record-${record.record_code}-title`}
        >
          {/* Record header */}
          <div className="px-5 pt-5 pb-4 space-y-2">
            <div className="flex items-start justify-between gap-3">
              <h3
                id={`record-${record.record_code}-title`}
                className="font-semibold text-slate-900 leading-snug"
              >
                {record.title}
              </h3>
              <RiskBadge level={record.risk_level as RiskLevel} className="shrink-0" />
            </div>
            <p className="text-slate-700 text-sm leading-relaxed">
              {record.plain_language_summary}
            </p>
            {record.next_step_text && (
              <p className="text-sm text-blue-700 font-medium pt-1">
                → {record.next_step_text}
              </p>
            )}
          </div>

          {/* Provenance strip */}
          <div className="border-t border-slate-100 px-5 py-3">
            <SourceBlock record={record} />
          </div>

          {/* Limitations */}
          {record.limitations && (
            <div className="border-t border-slate-100 px-5 py-3">
              <p className="text-xs text-slate-500 italic leading-relaxed">{record.limitations}</p>
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
    <ol className="space-y-3 list-none" aria-label="Verified next steps">
      {actions.map((action, idx) => (
        <li key={action.id} className="flex gap-4 rounded-xl border border-slate-200 bg-white p-4">
          {/* Step number */}
          <div className="ss-step-number shrink-0 mt-0.5" aria-label={`Step ${action.step_number}`}>
            {action.step_number}
          </div>

          <div className="space-y-2 flex-1 min-w-0">
            <p className="font-semibold text-slate-900 text-sm leading-snug">{action.title}</p>
            <p className="text-sm text-slate-600 leading-relaxed">{action.instruction}</p>

            {/* PROTECT — linked support service */}
            {action.support_service && (
              <div className="rounded-lg border border-blue-100 bg-blue-50 p-3 space-y-2 mt-2">
                <div className="flex items-start justify-between gap-2">
                  <p className="font-semibold text-blue-900 text-sm">{action.support_service.name}</p>
                  {action.support_service.available_24_7 && (
                    <span className="shrink-0 text-[10px] font-bold uppercase tracking-wide text-emerald-700 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded-full">
                      24/7
                    </span>
                  )}
                </div>
                <p className="text-xs text-blue-700 leading-relaxed">{action.support_service.description}</p>
                <div className="flex flex-wrap gap-2 pt-1">
                  {action.support_service.phone && (
                    <a
                      href={`tel:${action.support_service.phone}`}
                      className="inline-flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors min-h-[36px]"
                      aria-label={`Call ${action.support_service.name}: ${action.support_service.phone}`}
                    >
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                        <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012.18 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 8.15a16 16 0 006.94 6.94l1.51-1.51a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
                      </svg>
                      Call {action.support_service.phone}
                    </a>
                  )}
                  {action.support_service.whatsapp && (
                    <a
                      href={`https://wa.me/${action.support_service.whatsapp.replace(/\D/g, "")}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors min-h-[36px]"
                      aria-label={`WhatsApp ${action.support_service.name}`}
                    >
                      WhatsApp
                    </a>
                  )}
                  {action.support_service.website && (
                    <a
                      href={action.support_service.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-blue-700 hover:underline min-h-[36px] items-center"
                      aria-label={`Visit ${action.support_service.name} website`}
                    >
                      Official website ↗
                    </a>
                  )}
                </div>
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
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-10">

      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb">
        <ol className="flex items-center gap-1.5 text-sm text-slate-500 flex-wrap">
          <li><Link href="/" className="hover:text-blue-700 transition-colors">SafeSpace</Link></li>
          <li aria-hidden="true" className="text-slate-300">/</li>
          <li>
            <Link href={`/journeys/${journeySlug}`} className="hover:text-blue-700 transition-colors capitalize">
              {journeySlug.replace(/-/g, " ")}
            </Link>
          </li>
          <li aria-hidden="true" className="text-slate-300">/</li>
          <li className="text-slate-800 font-medium" aria-current="page">{topicTitle}</li>
        </ol>
      </nav>

      {/* Topic header */}
      <header className="space-y-2">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{topicTitle}</h1>
        {topicDescription && (
          <p className="text-slate-600 leading-relaxed max-w-xl">{topicDescription}</p>
        )}
      </header>

      {fetchError && (
        <ErrorState message="We couldn't load this information right now. Please try again later." />
      )}

      {!fetchError && (
        <>
          {/* UNDERSTAND + VERIFY */}
          <section aria-labelledby="understand-heading" className="space-y-4">
            <div className="ss-divider-label">
              <span className="ss-section-label">Understand — Your rights</span>
            </div>
            <RightsSection rights={rights} />
          </section>

          {/* ACT + PROTECT */}
          <section aria-labelledby="act-heading" className="space-y-4">
            <div className="ss-divider-label">
              <span className="ss-section-label">Next steps — What you can do</span>
            </div>
            <ActionSection actions={actions} />
          </section>
        </>
      )}

      {/* Safety prompt */}
      <aside className="rounded-xl border border-amber-200 bg-amber-50 p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <p className="text-sm text-amber-900 font-medium">Concerned about your safety right now?</p>
        <Link href="/safety" className="ss-btn-primary text-xs shrink-0 !min-h-[38px]">
          Safety Check
        </Link>
      </aside>
    </div>
  );
}

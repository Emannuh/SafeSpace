import Link from "next/link";
import { fetchSupportServices } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import type { SupportService } from "@/lib/types";

const categoryMeta: Record<string, { label: string; icon: string; colour: string }> = {
  CHILD_PROTECTION: { label: "Child Protection", icon: "🛡️", colour: "bg-violet-50 text-violet-700 border-violet-200" },
  GBV_SUPPORT:      { label: "GBV Support",       icon: "💜", colour: "bg-pink-50 text-pink-700 border-pink-200" },
  LEGAL_AID:        { label: "Legal Aid",          icon: "⚖️", colour: "bg-blue-50 text-blue-700 border-blue-200" },
  POLICE_OVERSIGHT: { label: "Police Oversight",   icon: "🔍", colour: "bg-slate-50 text-slate-700 border-slate-200" },
  HEALTH_SUPPORT:   { label: "Health Support",     icon: "🏥", colour: "bg-teal-50 text-teal-700 border-teal-200" },
  GENERAL_SUPPORT:  { label: "General Support",    icon: "🤝", colour: "bg-amber-50 text-amber-700 border-amber-200" },
};

function ServiceCard({ service }: { service: SupportService }) {
  const meta = categoryMeta[service.service_type] ?? { label: service.service_type_display, icon: "🤝", colour: "bg-slate-50 text-slate-700 border-slate-200" };

  return (
    <article
      className="rounded-xl border border-slate-200 bg-white overflow-hidden flex flex-col"
      aria-labelledby={`service-${service.slug}-name`}
    >
      {/* Card header */}
      <div className="p-5 flex-1 space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div className="space-y-1">
            <span className={`inline-flex items-center gap-1.5 text-[11px] font-semibold px-2 py-0.5 rounded-full border ${meta.colour}`}>
              <span aria-hidden="true">{meta.icon}</span>
              {meta.label}
            </span>
            {service.available_24_7 && (
              <span className="ml-1.5 inline-flex items-center text-[10px] font-bold uppercase tracking-wide text-emerald-700 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded-full">
                24/7
              </span>
            )}
          </div>
        </div>

        <h2
          id={`service-${service.slug}-name`}
          className="font-bold text-slate-900 text-base leading-snug"
        >
          {service.name}
        </h2>

        <p className="text-sm text-slate-600 leading-relaxed">
          {service.description}
        </p>
      </div>

      {/* Actions */}
      {(service.phone || service.whatsapp || service.website) && (
        <div className="border-t border-slate-100 px-5 py-3 bg-slate-50 flex flex-wrap gap-2">
          {service.phone && (
            <a
              href={`tel:${service.phone}`}
              className="inline-flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors min-h-[44px]"
              aria-label={`Call ${service.name}: ${service.phone}`}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012.18 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 8.15a16 16 0 006.94 6.94l1.51-1.51a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
              </svg>
              Call {service.phone}
            </a>
          )}
          {service.whatsapp && (
            <a
              href={`https://wa.me/${service.whatsapp.replace(/\D/g, "")}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors min-h-[44px]"
              aria-label={`WhatsApp ${service.name}`}
            >
              WhatsApp
            </a>
          )}
          {service.website && (
            <a
              href={service.website}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-sm text-slate-600 hover:text-blue-700 transition-colors min-h-[44px]"
              aria-label={`Visit ${service.name} official website`}
            >
              Website ↗
            </a>
          )}
        </div>
      )}

      {/* Trust footer */}
      <div className="border-t border-slate-100 px-5 py-2.5 flex items-center gap-2">
        <svg width="10" height="10" viewBox="0 0 14 14" fill="none" aria-hidden="true">
          <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="#16a34a" fillOpacity="0.5"/>
          <path d="M4.5 7L6 8.5L9.5 5" stroke="#16a34a" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <span className="text-[11px] text-slate-400">
          Verified source · Last verified {service.last_verified}
        </span>
      </div>
    </article>
  );
}

export default async function SupportPage() {
  let services: SupportService[] = [];
  let fetchError = false;

  try {
    services = await fetchSupportServices();
  } catch {
    fetchError = true;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">

      {/* Header */}
      <header className="space-y-3">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Find the right support</h1>
        <p className="text-slate-600 leading-relaxed max-w-xl">
          These are verified support organisations and helplines in Kenya.
          SafeSpace does not operate any of these services.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 pt-1">
          <Link href="/safety" className="ss-btn-primary text-sm">
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="currentColor" fillOpacity="0.8"/>
            </svg>
            Need urgent help? Safety Check
          </Link>
        </div>
      </header>

      {fetchError && <ErrorState message="We couldn't load support services right now. Please try again later." />}
      {!fetchError && services.length === 0 && <EmptyState message="No support services are currently listed." />}

      {!fetchError && services.length > 0 && (
        <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4" role="list" aria-label="Support services">
          {services.map((service) => (
            <li key={service.slug}>
              <ServiceCard service={service} />
            </li>
          ))}
        </ul>
      )}

      {/* Disclaimer */}
      <aside className="text-xs text-slate-400 border-t border-slate-100 pt-4">
        Always verify contact details through official sources before sharing sensitive information.
        SafeSpace does not guarantee service availability.
      </aside>
    </div>
  );
}

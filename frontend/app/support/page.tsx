import { fetchSupportServices } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import type { SupportService } from "@/lib/types";

function ServiceCard({ service }: { service: SupportService }) {
  return (
    <article
      className="rounded-xl border border-slate-200 bg-white p-5 space-y-3"
      aria-labelledby={`service-${service.slug}-name`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2
            id={`service-${service.slug}-name`}
            className="font-semibold text-slate-900"
          >
            {service.name}
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            {service.service_type_display}
            {service.available_24_7 && (
              <span className="ml-2 text-emerald-600 font-medium">· 24/7</span>
            )}
          </p>
        </div>
        <span className="text-xs text-slate-400 shrink-0">
          {service.jurisdiction}
        </span>
      </div>

      <p className="text-sm text-slate-600 leading-relaxed">
        {service.description}
      </p>

      <div className="flex flex-col gap-1.5 text-sm">
        {service.phone && (
          <a
            href={`tel:${service.phone}`}
            className="inline-flex items-center gap-2 text-blue-700 font-medium hover:underline"
            aria-label={`Call ${service.name}: ${service.phone}`}
          >
            📞 <span>{service.phone}</span>
          </a>
        )}
        {service.whatsapp && (
          <a
            href={`https://wa.me/${service.whatsapp.replace(/\D/g, "")}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-green-700 hover:underline"
            aria-label={`WhatsApp ${service.name}: ${service.whatsapp}`}
          >
            💬 <span>{service.whatsapp}</span>
          </a>
        )}
        {service.website && (
          <a
            href={service.website}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-blue-600 hover:underline"
            aria-label={`Visit ${service.name} website (opens in new tab)`}
          >
            🌐 <span className="break-all">{service.website}</span>
          </a>
        )}
      </div>

      <p className="text-xs text-slate-400">
        Last verified: {service.last_verified}
      </p>
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
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Support Services</h1>
        <p className="mt-2 text-slate-600">
          Verified support organisations and helplines available in Kenya.
        </p>
        <p className="mt-1 text-sm text-slate-500">
          SafeSpace does not operate these services. Always verify contact
          details through official sources before sharing sensitive information.
        </p>
      </header>

      {fetchError && (
        <ErrorState message="We couldn't load support services right now. Please try again later." />
      )}

      {!fetchError && services.length === 0 && (
        <EmptyState message="No support services are currently listed." />
      )}

      {!fetchError && services.length > 0 && (
        <ul className="space-y-4" role="list" aria-label="Support services">
          {services.map((service) => (
            <li key={service.slug}>
              <ServiceCard service={service} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

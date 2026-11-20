import Link from "next/link";
import { fetchSupportServices } from "@/lib/api";
import { EmptyState, ErrorState } from "@/app/components/StateViews";
import { Always247, Container, PageHeader, ServiceContactActions } from "@/app/components/ui";
import {
  HandsIcon, HealthIcon, HeartIcon, ScaleIcon, SearchIcon, ShieldCheckIcon, ShieldIcon,
} from "@/app/components/Icons";
import type { SupportService } from "@/lib/types";

type IconComp = typeof ShieldIcon;

const categoryMeta: Record<string, { label: string; Icon: IconComp; tint: string }> = {
  CHILD_PROTECTION: { label: "Child Protection", Icon: ShieldIcon, tint: "bg-violet-500/10 text-violet-700 dark:text-violet-300" },
  GBV_SUPPORT:      { label: "GBV Support",      Icon: HeartIcon,  tint: "bg-pink-500/10 text-pink-700 dark:text-pink-300" },
  LEGAL_AID:        { label: "Legal Aid",        Icon: ScaleIcon,  tint: "bg-blue-500/10 text-blue-700 dark:text-blue-300" },
  POLICE_OVERSIGHT: { label: "Police Oversight", Icon: SearchIcon, tint: "bg-slate-500/10 text-slate-700 dark:text-slate-300" },
  HEALTH_SUPPORT:   { label: "Health Support",   Icon: HealthIcon, tint: "bg-teal-500/10 text-teal-700 dark:text-teal-300" },
  GENERAL_SUPPORT:  { label: "General Support",  Icon: HandsIcon,  tint: "bg-amber-500/10 text-amber-700 dark:text-amber-300" },
};

function ServiceCard({ service }: { service: SupportService }) {
  const meta = categoryMeta[service.service_type] ?? {
    label: service.service_type_display, Icon: HandsIcon, tint: "bg-sunken text-ink-soft",
  };
  const { Icon } = meta;

  return (
    <article
      className="ss-card flex h-full flex-col overflow-hidden"
      aria-labelledby={`service-${service.slug}-name`}
    >
      <div className="flex-1 space-y-3 p-5">
        <div className="flex items-center justify-between gap-3">
          <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${meta.tint}`}>
            <Icon size={14} />
            {meta.label}
          </span>
          {service.available_24_7 && <Always247 />}
        </div>

        <h2
          id={`service-${service.slug}-name`}
          className="text-lg font-bold leading-snug tracking-tight text-ink"
        >
          {service.name}
        </h2>

        <p className="text-sm leading-relaxed text-ink-soft">
          {service.description}
        </p>
      </div>

      {(service.phone || service.whatsapp || service.website) && (
        <div className="px-5 pb-5">
          <ServiceContactActions
            name={service.name}
            phone={service.phone}
            whatsapp={service.whatsapp}
            website={service.website}
          />
        </div>
      )}

      <div className="flex items-center gap-2 border-t border-line bg-sunken/50 px-5 py-2.5 text-xs text-ink-faint">
        <ShieldCheckIcon size={13} className="text-ok-ink" />
        Verified source · Last verified {service.last_verified}
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
    <Container wide className="space-y-10 py-10">
      <PageHeader
        eyebrow="Support"
        title="Find the right support"
        description="These are verified support organisations and helplines in Kenya. SafeSpace does not operate any of these services."
      >
        <div className="flex flex-col gap-3 pt-2 sm:flex-row sm:items-center">
          <Link href="/safety" className="ss-btn-primary">
            <ShieldIcon size={16} />
            Need urgent help? Safety Check
          </Link>
          <p className="text-sm text-ink-soft">
            In immediate danger? Call <strong className="text-ink">999</strong> or <strong className="text-ink">112</strong>.
          </p>
        </div>
      </PageHeader>

      {fetchError && <ErrorState message="We couldn't load support services right now. Please try again later." />}
      {!fetchError && services.length === 0 && <EmptyState message="No support services are currently listed." />}

      {!fetchError && services.length > 0 && (
        <ul className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3" role="list" aria-label="Support services">
          {services.map((service) => (
            <li key={service.slug}>
              <ServiceCard service={service} />
            </li>
          ))}
        </ul>
      )}

      <aside className="border-t border-line pt-5 text-xs leading-relaxed text-ink-faint">
        Always verify contact details through official sources before sharing sensitive information.
        SafeSpace does not guarantee service availability.
      </aside>
    </Container>
  );
}

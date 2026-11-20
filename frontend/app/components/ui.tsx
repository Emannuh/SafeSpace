/**
 * Shared presentational building blocks used across SafeSpace pages.
 * Server-component safe (no hooks, no client state).
 */

import Link from "next/link";
import type { ReactNode } from "react";
import { ChatIcon, ChevronRightIcon, ExternalIcon, PhoneIcon, ShieldIcon } from "./Icons";

/* ─── Layout ─── */
export function Container({ children, wide = false, className = "" }: {
  children: ReactNode; wide?: boolean; className?: string;
}) {
  return (
    <div className={`mx-auto w-full px-4 sm:px-6 ${wide ? "max-w-5xl" : "max-w-3xl"} ${className}`}>
      {children}
    </div>
  );
}

/* ─── Page header ─── */
export function PageHeader({ eyebrow, title, description, children }: {
  eyebrow?: ReactNode; title: ReactNode; description?: ReactNode; children?: ReactNode;
}) {
  return (
    <header className="space-y-3">
      {eyebrow && <p className="ss-section-label text-brand-ink">{eyebrow}</p>}
      <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-ink text-balance leading-[1.15]">
        {title}
      </h1>
      {description && (
        <p className="text-ink-soft text-lg leading-relaxed max-w-2xl text-pretty">{description}</p>
      )}
      {children}
    </header>
  );
}

/* ─── Section heading ─── */
export function SectionLabel({ id, children }: { id?: string; children: ReactNode }) {
  return (
    <div className="ss-divider-label">
      <h2 id={id} className="ss-section-label">{children}</h2>
    </div>
  );
}

/* ─── Breadcrumbs ─── */
export function Breadcrumbs({ items }: { items: { label: string; href?: string; capitalize?: boolean }[] }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol className="flex flex-wrap items-center gap-1 text-sm text-ink-faint">
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-1 min-w-0">
            {i > 0 && <ChevronRightIcon size={14} className="shrink-0 opacity-60" />}
            {item.href ? (
              <Link
                href={item.href}
                className={`rounded px-1 hover:text-brand-ink transition-colors ${item.capitalize ? "capitalize" : ""}`}
              >
                {item.label}
              </Link>
            ) : (
              <span className="px-1 font-semibold text-ink truncate" aria-current="page">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

/* ─── 24/7 pill ─── */
export function Always247() {
  return (
    <span className="ss-chip shrink-0 border-ok-line bg-ok-bg text-ok-ink text-[11px] uppercase tracking-wide">
      <span className="h-1.5 w-1.5 rounded-full bg-current" aria-hidden="true" />
      24/7
    </span>
  );
}

/* ─── Service contact buttons (call / WhatsApp / website) ─── */
export function ServiceContactActions({ name, phone, whatsapp, website, compact = false }: {
  name: string; phone?: string; whatsapp?: string; website?: string; compact?: boolean;
}) {
  if (!phone && !whatsapp && !website) return null;
  const size = compact ? "text-sm px-3.5 min-h-[40px]" : "text-sm px-4 min-h-[44px]";

  return (
    <div className="flex flex-wrap items-center gap-2">
      {phone && (
        <a
          href={`tel:${phone}`}
          className={`inline-flex items-center gap-2 rounded-full bg-brand hover:bg-brand-strong text-white font-semibold transition-colors ${size}`}
          aria-label={`Call ${name}: ${phone}`}
        >
          <PhoneIcon size={15} />
          Call {phone}
        </a>
      )}
      {whatsapp && (
        <a
          href={`https://wa.me/${whatsapp.replace(/\D/g, "")}`}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center gap-2 rounded-full bg-whatsapp hover:bg-whatsapp-strong text-white font-semibold transition-colors ${size}`}
          aria-label={`WhatsApp ${name}`}
        >
          <ChatIcon size={15} />
          WhatsApp
        </a>
      )}
      {website && (
        <a
          href={website}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center gap-1.5 rounded-full border border-line-strong bg-card text-ink-soft hover:text-brand-ink hover:border-brand-line font-medium transition-colors ${size}`}
          aria-label={`Visit ${name} official website (opens in new tab)`}
        >
          Website
          <ExternalIcon size={14} />
        </a>
      )}
    </div>
  );
}

/* ─── "Concerned about your safety?" prompt ─── */
export function SafetyPrompt() {
  return (
    <aside className="rounded-2xl border border-warn-line bg-warn-bg p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div className="flex items-start gap-3">
        <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-card text-warn-ink">
          <ShieldIcon size={18} />
        </span>
        <div>
          <p className="font-semibold text-warn-ink">Concerned about your safety right now?</p>
          <p className="text-sm text-warn-ink/80">
            If you are in immediate danger, call <strong>999</strong> or <strong>112</strong>.
          </p>
        </div>
      </div>
      <Link href="/safety" className="ss-btn-primary shrink-0">
        Safety Check
      </Link>
    </aside>
  );
}

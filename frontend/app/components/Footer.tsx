import Link from "next/link";
import { BrandMark } from "./Header";

const links = [
  { href: "/", label: "Journeys" },
  { href: "/ask", label: "Ask SafeSpace" },
  { href: "/support", label: "Support Services" },
  { href: "/safety", label: "Safety Check" },
];

export default function Footer() {
  return (
    <footer className="mt-24 border-t border-line bg-card">
      <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <div className="flex flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">

          {/* Brand column */}
          <div className="max-w-sm space-y-3">
            <div className="flex items-center gap-2">
              <BrandMark size="sm" />
              <span className="font-extrabold tracking-tight text-ink">SafeSpace</span>
            </div>
            <p className="text-sm leading-relaxed text-ink-soft">
              Verified rights information for young people in Kenya.
              Not a substitute for qualified legal advice.
            </p>
            <p className="text-sm text-ink-soft">
              In immediate danger? Call <strong className="text-ink">999</strong> or{" "}
              <strong className="text-ink">112</strong>.
            </p>
          </div>

          {/* Links column */}
          <nav aria-label="Footer navigation" className="flex flex-col gap-2.5">
            <p className="ss-section-label">Navigate</p>
            {links.map((l) => (
              <Link key={l.href} href={l.href} className="text-sm text-ink-soft transition-colors hover:text-brand-ink">
                {l.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Bottom strip */}
        <div className="mt-10 flex flex-col gap-3 border-t border-line pt-6 text-xs leading-relaxed text-ink-faint sm:flex-row sm:items-center sm:justify-between">
          <p>No account required. Information is drawn from verified Kenyan legal and institutional sources.</p>
          <p className="shrink-0">
            <strong className="text-ink-soft">Quick Exit</strong> leaves SafeSpace immediately
            but does not erase browser history.
          </p>
        </div>
      </div>
    </footer>
  );
}

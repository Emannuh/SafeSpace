import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white mt-20">
      <div className="max-w-3xl mx-auto px-4 py-10">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6">

          {/* Brand column */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-blue-600 flex items-center justify-center">
                <svg width="12" height="12" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                  <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="white" fillOpacity="0.9"/>
                </svg>
              </div>
              <span className="text-sm font-semibold text-slate-900">SafeSpace</span>
            </div>
            <p className="text-xs text-slate-500 max-w-xs">
              Verified rights information for young people in Kenya.
              Not a substitute for qualified legal advice.
            </p>
          </div>

          {/* Links column */}
          <nav aria-label="Footer navigation" className="flex flex-col gap-2">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">Navigate</p>
            <Link href="/" className="text-sm text-slate-500 hover:text-blue-700 transition-colors">Journeys</Link>
            <Link href="/support" className="text-sm text-slate-500 hover:text-blue-700 transition-colors">Support Services</Link>
            <Link href="/safety" className="text-sm text-slate-500 hover:text-blue-700 transition-colors">Safety Check</Link>
          </nav>
        </div>

        {/* Bottom strip */}
        <div className="mt-8 pt-6 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-xs text-slate-400">
          <p>No account required. Information is drawn from verified Kenyan legal and institutional sources.</p>
          <p className="shrink-0">
            <strong className="text-slate-500">Quick Exit</strong> leaves SafeSpace immediately
            but does not erase browser history.
          </p>
        </div>
      </div>
    </footer>
  );
}

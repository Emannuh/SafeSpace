import Link from "next/link";
import QuickExit from "./QuickExit";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
        {/* Brand */}
        <Link
          href="/"
          className="flex flex-col leading-tight group"
          aria-label="SafeSpace home"
        >
          <span className="text-lg font-bold text-blue-700 group-hover:text-blue-800 transition-colors">
            SafeSpace
          </span>
          <span className="text-xs text-slate-500 hidden sm:block">
            Understand your rights. Know your options.
          </span>
        </Link>

        {/* Navigation */}
        <nav aria-label="Main navigation" className="flex items-center gap-4">
          <Link
            href="/support"
            className="text-sm text-slate-600 hover:text-blue-700 transition-colors hidden sm:block"
          >
            Support Services
          </Link>
          <Link
            href="/safety"
            className="text-sm text-slate-600 hover:text-blue-700 transition-colors hidden sm:block"
          >
            Safety Check
          </Link>
          <QuickExit />
        </nav>
      </div>
    </header>
  );
}

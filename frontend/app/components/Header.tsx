import Link from "next/link";
import QuickExit from "./QuickExit";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between gap-4">

        {/* Brand */}
        <Link href="/" className="group flex items-center gap-2.5" aria-label="SafeSpace home">
          <div className="w-7 h-7 rounded-md bg-blue-600 flex items-center justify-center shrink-0">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="white" fillOpacity="0.9"/>
            </svg>
          </div>
          <div className="flex flex-col leading-none">
            <span className="text-sm font-bold text-slate-900 tracking-tight">SafeSpace</span>
            <span className="text-[10px] text-slate-500 hidden sm:block leading-tight mt-0.5">
              Your rights. Your options.
            </span>
          </div>
        </Link>

        {/* Navigation */}
        <nav aria-label="Main navigation" className="flex items-center gap-1">
          <Link
            href="/ask"
            className="hidden sm:inline-flex items-center px-3 py-1.5 text-sm text-slate-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
          >
            Ask SafeSpace
          </Link>
          <Link
            href="/support"
            className="hidden sm:inline-flex items-center px-3 py-1.5 text-sm text-slate-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
          >
            Support
          </Link>
          <Link
            href="/safety"
            className="hidden sm:inline-flex items-center px-3 py-1.5 text-sm text-slate-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
          >
            Safety Check
          </Link>
          <div className="w-px h-5 bg-slate-200 mx-1 hidden sm:block" aria-hidden="true" />
          <QuickExit />
        </nav>
      </div>
    </header>
  );
}

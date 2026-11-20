import Link from "next/link";
import QuickExit from "./QuickExit";
import NavLinks from "./NavLinks";
import { ShieldIcon } from "./Icons";

export function BrandMark({ size = "md" }: { size?: "sm" | "md" }) {
  const box = size === "sm" ? "h-7 w-7 rounded-lg" : "h-8 w-8 rounded-[10px]";
  return (
    <span className={`${box} flex shrink-0 items-center justify-center bg-linear-to-br from-brand to-brand-strong text-white shadow-sm`}>
      <ShieldIcon size={size === "sm" ? 14 : 16} strokeWidth={2.2} />
    </span>
  );
}

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-line/80 bg-canvas/80 backdrop-blur-lg supports-[backdrop-filter]:bg-canvas/70">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between gap-4 px-4 sm:px-6">

        {/* Brand */}
        <Link href="/" className="group flex items-center gap-2.5 rounded-lg" aria-label="SafeSpace home">
          <BrandMark />
          <span className="flex flex-col leading-none">
            <span className="text-[15px] font-extrabold tracking-tight text-ink">SafeSpace</span>
            <span className="mt-1 hidden text-[11px] font-medium text-ink-faint sm:block">
              Your rights. Your options.
            </span>
          </span>
        </Link>

        {/* Navigation */}
        <nav aria-label="Main navigation" className="flex items-center gap-1">
          <div className="hidden items-center gap-1 sm:flex">
            <NavLinks variant="bar" />
          </div>
          <span className="mx-2 hidden h-5 w-px bg-line sm:block" aria-hidden="true" />
          <QuickExit />
        </nav>
      </div>

      {/* Mobile navigation */}
      <nav aria-label="Main navigation (mobile)" className="sm:hidden">
        <div className="flex gap-2 overflow-x-auto px-4 pb-3 [scrollbar-width:none]">
          <NavLinks variant="strip" />
        </div>
      </nav>
    </header>
  );
}

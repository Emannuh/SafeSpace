"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export const navItems = [
  { href: "/ask", label: "Ask SafeSpace" },
  { href: "/support", label: "Support" },
  { href: "/safety", label: "Safety Check" },
] as const;

/**
 * Primary navigation links with active-page state.
 * `variant="bar"` is the desktop inline nav; `variant="strip"` is the
 * scrollable row shown under the header on small screens.
 */
export default function NavLinks({ variant }: { variant: "bar" | "strip" }) {
  const pathname = usePathname();

  return (
    <>
      {navItems.map(({ href, label }) => {
        const active = pathname === href || pathname?.startsWith(`${href}/`);
        const base =
          variant === "bar"
            ? "inline-flex items-center rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors"
            : "inline-flex shrink-0 items-center rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors border";
        const state = active
          ? variant === "bar"
            ? "bg-brand-soft text-brand-ink"
            : "bg-brand-soft text-brand-ink border-brand-line"
          : variant === "bar"
            ? "text-ink-soft hover:text-ink hover:bg-sunken"
            : "text-ink-soft border-line bg-card hover:text-ink";

        return (
          <Link
            key={href}
            href={href}
            className={`${base} ${state}`}
            aria-current={active ? "page" : undefined}
          >
            {label}
          </Link>
        );
      })}
    </>
  );
}

"use client";

import { XIcon } from "./Icons";

/**
 * Quick Exit — navigates away from SafeSpace immediately on click.
 *
 * IMPORTANT: This does NOT erase browser history, network logs, or
 * device activity. We communicate this clearly to users.
 * No history manipulation is attempted.
 */
export default function QuickExit() {
  function handleExit() {
    // Navigate away immediately — no confirmation dialog
    window.location.replace("https://www.google.com");
  }

  return (
    <button
      onClick={handleExit}
      aria-label="Quick Exit — leave SafeSpace immediately"
      className="
        inline-flex items-center gap-1.5
        min-h-[40px] rounded-full px-4
        bg-danger hover:bg-danger-strong active:scale-[0.97]
        text-white text-sm font-bold
        shadow-sm shadow-danger/30
        transition-[background-color,transform] duration-150
        focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-danger
      "
    >
      <XIcon size={15} strokeWidth={2.6} />
      Quick Exit
    </button>
  );
}

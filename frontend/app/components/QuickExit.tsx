"use client";

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
        bg-red-600 hover:bg-red-700 active:bg-red-800
        text-white text-sm font-semibold
        px-3 py-1.5 rounded
        transition-colors duration-150
        focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600
      "
    >
      <span aria-hidden="true">✕</span>
      Quick Exit
    </button>
  );
}

import AskForm from "./AskForm";

export default function AskPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      <header className="space-y-3 max-w-xl">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Ask SafeSpace
        </h1>
        <p className="text-slate-600 leading-relaxed">
          Ask a question about your rights or situation. SafeSpace answers using
          its verified information — not general AI knowledge.
        </p>
        <div className="flex items-center gap-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-700">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
            <path d="M7 1L2 3.5V7.5C2 10.09 4.24 12.5 7 13C9.76 12.5 12 10.09 12 7.5V3.5L7 1Z" fill="currentColor" fillOpacity="0.4"/>
            <path d="M5 7L6.5 8.5L9 5.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>
            <strong>AI-assisted explanation.</strong> Answers are grounded in verified Kenyan legal sources.
            Your question is not stored by SafeSpace.
          </span>
        </div>
      </header>

      <AskForm />
    </div>
  );
}

import SafetyCheckForm from "./SafetyCheckForm";

export default function SafetyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      <header>
        <h1 className="text-2xl font-bold text-slate-900">Safety Check</h1>
        <p className="mt-2 text-slate-600">
          Describe your situation briefly. SafeSpace will help you find the most
          relevant information and support.
        </p>
        <p className="mt-1 text-sm text-slate-500">
          This is not a chatbot. It uses structured safety rules — not AI — to
          guide you to verified information.
        </p>
        <p className="mt-1 text-xs text-slate-400">
          Your message is not stored by SafeSpace.
        </p>
      </header>

      <SafetyCheckForm />
    </div>
  );
}

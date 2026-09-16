import SafetyCheckForm from "./SafetyCheckForm";

export default function SafetyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      <header className="space-y-3 max-w-xl">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Safety Check</h1>
        <p className="text-slate-600 leading-relaxed">
          Describe your situation briefly. SafeSpace will guide you to the
          most relevant rights information and verified support.
        </p>
        <div className="space-y-1.5 text-sm text-slate-500">
          <p className="flex items-start gap-2">
            <span className="mt-0.5 shrink-0 w-4 h-4 rounded-full bg-slate-100 flex items-center justify-center text-[10px] font-bold text-slate-600" aria-hidden="true">i</span>
            This is not an emergency service. If you are in immediate danger, call <strong>999</strong> or <strong>112</strong>.
          </p>
          <p className="flex items-start gap-2">
            <span className="mt-0.5 shrink-0 w-4 h-4 rounded-full bg-slate-100 flex items-center justify-center text-[10px] font-bold text-slate-600" aria-hidden="true">🔒</span>
            Your message is not stored by SafeSpace.
          </p>
        </div>
      </header>

      <SafetyCheckForm />
    </div>
  );
}

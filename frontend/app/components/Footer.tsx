export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white mt-16">
      <div className="max-w-3xl mx-auto px-4 py-8 text-sm text-slate-500 space-y-2">
        <p>
          SafeSpace provides verified rights information for young people in Kenya.
          It is not a substitute for qualified legal advice.
        </p>
        <p>
          Information is drawn from verified legal sources. Each record shows its
          source and last verification date.
        </p>
        <p className="text-xs text-slate-400">
          No account is required to browse SafeSpace.
          SafeSpace aims to minimise personal-data collection.
          The Safety Check feature does not store your message.
        </p>
        <p className="text-xs text-slate-400">
          <strong>Quick Exit note:</strong> Using Quick Exit leaves SafeSpace
          immediately but does not erase your browser history or device activity.
        </p>
      </div>
    </footer>
  );
}

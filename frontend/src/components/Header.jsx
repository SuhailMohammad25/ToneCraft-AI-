import { Sparkles } from 'lucide-react';

export default function Header() {
  return (
    <header className="border-b border-black/10 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-ink text-white">
            <Sparkles size={20} aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-ink">ToneCraft AI</h1>
            <p className="text-sm text-ink/60">Emotion-aware response composer</p>
          </div>
        </div>
        <div className="hidden rounded-full border border-moss/20 bg-mint px-4 py-2 text-sm font-medium text-moss sm:block">
          Support-ready drafts in seconds
        </div>
      </div>
    </header>
  );
}

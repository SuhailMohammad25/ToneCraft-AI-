import { Check, Clipboard, Save } from 'lucide-react';
import LoadingState from './LoadingState.jsx';

function CopyButton({ text, label = 'Copy' }) {
  const copy = async () => {
    await navigator.clipboard.writeText(text);
  };

  return (
    <button
      type="button"
      onClick={copy}
      className="inline-flex items-center gap-2 rounded-lg border border-black/10 bg-white px-3 py-2 text-xs font-semibold text-ink transition hover:border-moss hover:text-moss"
      title={label}
    >
      <Clipboard size={14} aria-hidden="true" />
      {label}
    </button>
  );
}

function ReplyBlock({ title, text }) {
  return (
    <div className="rounded-lg border border-black/10 bg-white p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-ink">{title}</h3>
        <CopyButton text={text} />
      </div>
      <p className="whitespace-pre-wrap text-sm leading-6 text-ink/75">{text}</p>
    </div>
  );
}

export default function ResultPanel({ result, isLoading, error, onSave, canSave, saveState }) {
  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-5 text-sm text-red-700">
        {error}
      </div>
    );
  }

  if (!result) {
    return (
      <div className="rounded-lg border border-dashed border-black/15 bg-white p-8 text-center">
        <p className="text-sm font-semibold text-ink">Your analysis will appear here</p>
        <p className="mt-2 text-sm leading-6 text-ink/60">
          Paste a customer message and ToneCraft will compose empathetic, channel-ready replies.
        </p>
      </div>
    );
  }

  const alternatives = [
    ['Short reply', result.alternatives.short],
    ['Detailed reply', result.alternatives.detailed],
    ['De-escalation reply', result.alternatives.de_escalation],
  ];

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-black/10 bg-white p-5 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">Sentiment</p>
            <p className="mt-1 text-lg font-semibold text-ink">{result.sentiment}</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">Emotion</p>
            <p className="mt-1 text-lg font-semibold text-ink">{result.emotion}</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ink/50">Intensity</p>
            <p className="mt-1 text-lg font-semibold text-ink">{result.intensity}/100</p>
          </div>
        </div>
        <div className="mt-4 h-3 overflow-hidden rounded-full bg-black/10">
          <div
            className="h-full rounded-full bg-moss transition-all"
            style={{ width: `${result.intensity}%` }}
          />
        </div>
        <p className="mt-4 text-sm leading-6 text-ink/70">{result.emotion_reason}</p>
      </div>

      <div className="rounded-lg border border-moss/20 bg-mint p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-moss">Recommended tone</p>
        <p className="mt-2 text-sm leading-6 text-ink">{result.tone_adjustment}</p>
      </div>

      <div className="rounded-lg border border-black/10 bg-white p-5 shadow-sm">
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="text-base font-semibold text-ink">Main empathetic reply</h2>
          <CopyButton text={result.main_reply} />
        </div>
        <p className="whitespace-pre-wrap text-sm leading-6 text-ink/75">{result.main_reply}</p>
      </div>

      <div className="grid gap-4">
        {alternatives.map(([title, text]) => (
          <ReplyBlock key={title} title={title} text={text} />
        ))}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-lg border border-black/10 bg-white p-4">
          <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-ink">
            <Check size={16} className="text-moss" aria-hidden="true" />
            Do
          </h3>
          <ul className="space-y-2 text-sm leading-6 text-ink/70">
            {result.agent_guidance.do.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border border-black/10 bg-white p-4">
          <h3 className="mb-3 text-sm font-semibold text-ink">Don't</h3>
          <ul className="space-y-2 text-sm leading-6 text-ink/70">
            {result.agent_guidance.dont.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <button
        type="button"
        onClick={onSave}
        disabled={!canSave || saveState === 'saving'}
        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-moss px-5 py-3 text-sm font-semibold text-white transition hover:bg-ink disabled:cursor-not-allowed disabled:opacity-60"
      >
        <Save size={18} aria-hidden="true" />
        {saveState === 'saving' ? 'Saving...' : saveState === 'saved' ? 'Saved' : 'Save generated case'}
      </button>
    </div>
  );
}

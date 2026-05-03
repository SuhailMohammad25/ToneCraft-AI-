import { RefreshCw, Trash2 } from 'lucide-react';

export default function SavedCases({ cases, isLoading, onRefresh, onSelect, onDelete }) {
  return (
    <section className="mt-8 rounded-lg border border-black/10 bg-white p-5 shadow-sm">
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Saved cases</h2>
          <p className="text-sm text-ink/60">Newest cases appear first.</p>
        </div>
        <button
          type="button"
          onClick={onRefresh}
          className="inline-flex items-center justify-center gap-2 rounded-lg border border-black/10 px-3 py-2 text-sm font-semibold text-ink transition hover:border-moss hover:text-moss"
        >
          <RefreshCw size={16} aria-hidden="true" />
          Refresh
        </button>
      </div>

      {isLoading ? (
        <p className="text-sm text-ink/60">Loading saved cases...</p>
      ) : cases.length === 0 ? (
        <p className="rounded-lg bg-black/[0.03] p-4 text-sm text-ink/60">No saved cases yet.</p>
      ) : (
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {cases.map((item) => (
            <article key={item.id} className="rounded-lg border border-black/10 bg-stone-50 p-4">
              <div className="mb-3 flex items-start justify-between gap-3">
                <button
                  type="button"
                  onClick={() => onSelect(item)}
                  className="text-left text-sm font-semibold text-ink transition hover:text-moss"
                >
                  {item.emotion} · {item.sentiment}
                </button>
                <button
                  type="button"
                  onClick={() => onDelete(item.id)}
                  className="rounded-md p-1 text-ink/45 transition hover:bg-red-50 hover:text-red-600"
                  title="Delete case"
                >
                  <Trash2 size={16} aria-hidden="true" />
                </button>
              </div>
              <p className="line-clamp-3 text-sm leading-6 text-ink/65">{item.customer_message}</p>
              <div className="mt-3 flex flex-wrap gap-2 text-xs font-medium text-ink/60">
                <span className="rounded-full bg-mint px-2 py-1">{item.brand_tone}</span>
                <span className="rounded-full bg-blush px-2 py-1">{item.channel}</span>
                <span className="rounded-full bg-white px-2 py-1">{item.intensity}/100</span>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

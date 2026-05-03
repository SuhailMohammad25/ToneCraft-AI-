import { WandSparkles } from 'lucide-react';

const brandTones = ['Professional', 'Warm', 'Apologetic', 'Friendly', 'Premium', 'Concise'];
const channels = ['Email', 'Chat', 'WhatsApp', 'Social Media'];

export default function AnalyzeForm({ form, onChange, onSubmit, isLoading }) {
  const update = (field) => (event) => onChange({ ...form, [field]: event.target.value });

  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <div>
        <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="customer_message">
          Customer message
        </label>
        <textarea
          id="customer_message"
          value={form.customer_message}
          onChange={update('customer_message')}
          rows={9}
          placeholder="Paste the customer's message here..."
          className="w-full resize-y rounded-lg border border-black/10 bg-white px-4 py-3 text-sm leading-6 text-ink shadow-sm outline-none transition focus:border-moss focus:ring-4 focus:ring-moss/10"
          required
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="brand_tone">
            Brand tone
          </label>
          <select
            id="brand_tone"
            value={form.brand_tone}
            onChange={update('brand_tone')}
            className="w-full rounded-lg border border-black/10 bg-white px-4 py-3 text-sm text-ink shadow-sm outline-none transition focus:border-moss focus:ring-4 focus:ring-moss/10"
          >
            {brandTones.map((tone) => (
              <option key={tone} value={tone}>
                {tone}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="channel">
            Channel
          </label>
          <select
            id="channel"
            value={form.channel}
            onChange={update('channel')}
            className="w-full rounded-lg border border-black/10 bg-white px-4 py-3 text-sm text-ink shadow-sm outline-none transition focus:border-moss focus:ring-4 focus:ring-moss/10"
          >
            {channels.map((channel) => (
              <option key={channel} value={channel}>
                {channel}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="company_context">
          Company context
        </label>
        <input
          id="company_context"
          value={form.company_context}
          onChange={update('company_context')}
          placeholder="Example: Premium skincare subscription brand"
          className="w-full rounded-lg border border-black/10 bg-white px-4 py-3 text-sm text-ink shadow-sm outline-none transition focus:border-moss focus:ring-4 focus:ring-moss/10"
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="agent_notes">
          Agent notes
        </label>
        <input
          id="agent_notes"
          value={form.agent_notes}
          onChange={update('agent_notes')}
          placeholder="Example: Customer has already shared order ID"
          className="w-full rounded-lg border border-black/10 bg-white px-4 py-3 text-sm text-ink shadow-sm outline-none transition focus:border-moss focus:ring-4 focus:ring-moss/10"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-5 py-3 text-sm font-semibold text-white shadow-soft transition hover:bg-moss disabled:cursor-not-allowed disabled:opacity-60"
      >
        <WandSparkles size={18} aria-hidden="true" />
        {isLoading ? 'Analyzing...' : 'Analyze & Generate'}
      </button>
    </form>
  );
}

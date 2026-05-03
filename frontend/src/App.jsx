import { useEffect, useMemo, useState } from 'react';
import { analyzeMessage, deleteCase, getCases, saveCase } from './api.js';
import AnalyzeForm from './components/AnalyzeForm.jsx';
import Header from './components/Header.jsx';
import ResultPanel from './components/ResultPanel.jsx';
import SavedCases from './components/SavedCases.jsx';

const initialForm = {
  customer_message:
    'I have contacted your team three times and nobody has solved my refund issue. This is extremely frustrating and I want an answer today.',
  brand_tone: 'Apologetic',
  channel: 'Email',
  company_context: '',
  agent_notes: '',
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [cases, setCases] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoadingCases, setIsLoadingCases] = useState(false);
  const [error, setError] = useState('');
  const [saveState, setSaveState] = useState('idle');

  const savePayload = useMemo(() => {
    if (!result) return null;
    return {
      ...form,
      company_context: form.company_context || null,
      agent_notes: form.agent_notes || null,
      ...result,
    };
  }, [form, result]);

  const loadCases = async () => {
    setIsLoadingCases(true);
    try {
      setCases(await getCases());
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoadingCases(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, []);

  const handleAnalyze = async (event) => {
    event.preventDefault();
    setError('');
    setSaveState('idle');
    setIsAnalyzing(true);
    try {
      const payload = {
        ...form,
        company_context: form.company_context || null,
        agent_notes: form.agent_notes || null,
      };
      setResult(await analyzeMessage(payload));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSave = async () => {
    if (!savePayload) return;
    setSaveState('saving');
    setError('');
    try {
      const created = await saveCase(savePayload);
      setCases((current) => [created, ...current.filter((item) => item.id !== created.id)]);
      setSaveState('saved');
    } catch (requestError) {
      setSaveState('idle');
      setError(requestError.message);
    }
  };

  const handleSelectCase = (item) => {
    setForm({
      customer_message: item.customer_message,
      brand_tone: item.brand_tone,
      channel: item.channel,
      company_context: item.company_context || '',
      agent_notes: item.agent_notes || '',
    });
    setResult({
      sentiment: item.sentiment,
      emotion: item.emotion,
      intensity: item.intensity,
      emotion_reason: item.emotion_reason,
      tone_adjustment: item.tone_adjustment,
      main_reply: item.main_reply,
      alternatives: item.alternatives,
      agent_guidance: item.agent_guidance,
    });
    setSaveState('saved');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDeleteCase = async (caseId) => {
    try {
      await deleteCase(caseId);
      setCases((current) => current.filter((item) => item.id !== caseId));
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  return (
    <div className="min-h-screen bg-[#f7f4ee]">
      <Header />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold tracking-normal text-ink">Compose with emotional precision</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-ink/65">
            Analyze customer sentiment, detect emotional cues, and draft empathetic responses that fit the brand and channel.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <section className="rounded-lg border border-black/10 bg-white p-5 shadow-sm">
            <AnalyzeForm
              form={form}
              onChange={setForm}
              onSubmit={handleAnalyze}
              isLoading={isAnalyzing}
            />
          </section>
          <section className="min-h-[480px]">
            <ResultPanel
              result={result}
              isLoading={isAnalyzing}
              error={error}
              onSave={handleSave}
              canSave={Boolean(savePayload)}
              saveState={saveState}
            />
          </section>
        </div>

        <SavedCases
          cases={cases}
          isLoading={isLoadingCases}
          onRefresh={loadCases}
          onSelect={handleSelectCase}
          onDelete={handleDeleteCase}
        />
      </main>
    </div>
  );
}

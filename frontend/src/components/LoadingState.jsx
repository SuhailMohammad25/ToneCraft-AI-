export default function LoadingState() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((item) => (
        <div key={item} className="animate-pulse rounded-lg border border-black/10 bg-white p-4">
          <div className="mb-3 h-4 w-1/3 rounded bg-black/10" />
          <div className="h-3 w-full rounded bg-black/10" />
          <div className="mt-2 h-3 w-5/6 rounded bg-black/10" />
        </div>
      ))}
    </div>
  );
}

import React from "react";

export default function SummaryPanel({ query, summary, meta }) {
  if (!summary) return null;

  return (
    <div className="glass rounded-xl p-5 mt-8">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-bold text-blue-300">Summary</h2>
        <span className="text-sm text-gray-400">
          "{query}" · {meta.took_ms}ms · {meta.doc_count} docs
        </span>
      </div>
      <p className="text-gray-200 leading-relaxed">{summary}</p>
    </div>
  );
}

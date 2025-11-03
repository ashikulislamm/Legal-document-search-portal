import React from "react";

export default function Results({ results }) {
  if (!results.length)
    return (
      <div className="text-center text-gray-400 py-10">
        No results found. Try a different keyword.
      </div>
    );

  return (
    <div className="grid gap-5 mt-6">
      {results.map((r) => (
        <div
          key={r.doc_id}
          className="glass rounded-xl p-5 hover:shadow-lg hover:scale-[1.02] transition-all duration-300"
        >
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-lg font-semibold text-white">{r.title}</h3>
            <span className="text-xs bg-primary/20 px-3 py-1 rounded-full text-blue-300">
              Score: {r.score}
            </span>
          </div>
          <div className="space-y-2">
            {r.snippets.map((s, i) => (
              <p
                key={i}
                className="bg-slate-800/60 border border-slate-700/40 rounded-lg p-3 text-gray-300 text-sm leading-relaxed"
              >
                {s}
              </p>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

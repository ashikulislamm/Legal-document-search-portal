import React from "react";

export default function ErrorBanner({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="bg-red-500/20 text-red-200 border border-red-400/40 rounded-lg px-4 py-3 flex justify-between items-center animate-fadeIn">
      <span>⚠️ {message}</span>
      <button
        onClick={onClose}
        className="hover:text-white text-red-300 font-bold"
      >
        ✖
      </button>
    </div>
  );
}

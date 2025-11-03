import React from "react";

import { useState } from "react";

export default function SearchBar({ onSearch, disabled }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-3 w-full max-w-2xl mx-auto"
    >
      <input
        type="text"
        placeholder="Search legal topics... (e.g., contract, tort, negligence)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 px-4 py-3 rounded-xl glass focus:outline-none focus:ring-2 focus:ring-primary text-gray-100 placeholder-gray-400"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled}
        className="px-5 py-3 bg-primary rounded-xl hover:bg-blue-600 transition-all text-white font-medium shadow-md disabled:opacity-60 cursor-pointer"
      >
        Search
      </button>
    </form>
  );
}

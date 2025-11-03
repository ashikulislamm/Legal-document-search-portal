import { useState } from "react";
import { generate } from "./lib/api";
import SearchBar from "./components/SearchBar";
import Results from "./components/Results";
import SummaryPanel from "./components/SummaryPanel";
import Loader from "./components/Loader";
import ErrorBanner from "./components/ErrorBanner";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  const handleSearch = async (q) => {
    setError("");
    setLoading(true);
    setData(null);

    try {
      const res = await generate(q);
      setData(res);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Something went wrong. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto px-6 py-10">
      <header className="text-center mb-10">
        <h1 className="text-4xl font-bold text-white mb-3">
          Legal Document Search Portal ⚖️
        </h1>
        <p className="text-gray-400">
          Explore key concepts in law — search through mock legal documents with
          instant summaries.
        </p>
      </header>

      <ErrorBanner message={error} onClose={() => setError("")} />
      <SearchBar onSearch={handleSearch} disabled={loading} />

      {loading && <Loader />}

      {data && (
        <>
          <SummaryPanel
            query={data.query}
            summary={data.summary}
            meta={data.meta}
          />
          <Results results={data.results} />
        </>
      )}

      <footer className="text-center text-gray-500 mt-10 text-sm">
        © 2025 Legal Search Portal · Mock Demo
      </footer>
    </main>
  );
}

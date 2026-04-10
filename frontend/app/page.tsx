"use client";

import { useState } from "react";
import QueryInput from "@/components/QueryInput";
import ResultsPanel from "@/components/ResultsPanel";

interface QueryResult {
  question: string;
  sql: string;
  explanation: string;
  confidence: number;
  columns: string[];
  results: Record<string, unknown>[];
  row_count: number;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: query, confidence_threshold: 0.4 }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Something went wrong.");
      }

      const data: QueryResult = await res.json();
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error occurred.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-wrapper">
      {/* Header */}
      <header className="app-header">
        <div className="logo-icon">🧠</div>
        <span className="logo-text">Talk2Data AI</span>
        <span className="logo-badge">Beta</span>
      </header>

      {/* Main */}
      <main className="app-main">
        {/* Hero */}
        <section className="hero">
          <h1>Ask your data anything</h1>
          <p>
            Type a question in plain English — Talk2Data AI converts it to SQL,
            runs it, and explains the results with visualizations.
          </p>
        </section>

        {/* Query Input */}
        <QueryInput
          query={query}
          loading={loading}
          onChange={setQuery}
          onSubmit={handleSubmit}
        />

        {/* Error */}
        {error && (
          <div className="error-card" role="alert">
            ⚠ {error}
          </div>
        )}

        {/* Results */}
        {result && <ResultsPanel data={result} />}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        Talk2Data AI · Powered by Gemini AI · Built for data accessibility
      </footer>
    </div>
  );
}

"use client";

interface QueryInputProps {
  query: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

const SUGGESTIONS = [
  "Show total sales by region",
  "What are the top 5 customers by revenue?",
  "Compare monthly orders this year vs last year",
  "Which products have the lowest stock?",
  "Summarize weekly signups for the past month",
];

export default function QueryInput({ query, loading, onChange, onSubmit }: QueryInputProps) {
  const handleKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="card">
      <div className="query-form">
        <div className="query-input-wrapper">
          <textarea
            id="query-input"
            className="query-input"
            placeholder="Ask anything about your data… e.g. 'Show total sales by region this quarter'"
            rows={3}
            value={query}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKey}
            disabled={loading}
          />
        </div>

        <div className="query-actions">
          <span className="query-hint">Press Ctrl+Enter to submit</span>
          <button
            id="submit-query-btn"
            className="btn-primary"
            onClick={onSubmit}
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <>
                <span className="spinner" />
                Analyzing…
              </>
            ) : (
              <>
                <span>✦</span>
                Ask AI
              </>
            )}
          </button>
        </div>

        {/* Suggestion Chips */}
        <div className="suggestions">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              className="suggestion-chip"
              onClick={() => onChange(s)}
              disabled={loading}
            >
              {s}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

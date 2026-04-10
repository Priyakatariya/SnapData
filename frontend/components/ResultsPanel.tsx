"use client";

import SqlDisplay from "./SqlDisplay";
import ConfidenceScore from "./ConfidenceScore";
import DataChart from "./Chart";

interface QueryResult {
  question: string;
  sql: string;
  explanation: string;
  confidence: number;
  columns: string[];
  results: Record<string, unknown>[];
  row_count: number;
}

interface ResultsPanelProps {
  data: QueryResult;
}

export default function ResultsPanel({ data }: ResultsPanelProps) {
  const { sql, explanation, confidence, columns, results, row_count } = data;

  return (
    <div className="results-section">

      {/* Explanation Card */}
      <div className="card">
        <div className="result-header">
          <span className="result-title">💡 Insight</span>
          <ConfidenceScore confidence={confidence} />
        </div>
        <p className="explanation-text">{explanation}</p>
        <div style={{ marginTop: "16px" }}>
          <SqlDisplay sql={sql} />
        </div>
      </div>

      {/* Chart Card */}
      {results.length > 0 && columns.length >= 2 && (
        <div className="card">
          <div className="result-header">
            <span className="result-title">📊 Visualization</span>
          </div>
          <DataChart columns={columns} results={results} />
        </div>
      )}

      {/* Table Card */}
      <div className="card">
        <div className="result-header">
          <span className="result-title">🗃 Data</span>
          <span className="row-count-badge">{row_count} row{row_count !== 1 ? "s" : ""}</span>
        </div>
        {results.length === 0 ? (
          <p style={{ color: "var(--text-muted)", fontSize: "0.88rem" }}>
            No rows returned for this query.
          </p>
        ) : (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  {columns.map((col) => (
                    <th key={col}>{col.replace(/_/g, " ")}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, i) => (
                  <tr key={i}>
                    {columns.map((col) => (
                      <td key={col}>{String(row[col] ?? "—")}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}

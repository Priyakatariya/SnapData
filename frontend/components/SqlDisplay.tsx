"use client";

import { useState } from "react";

interface SqlDisplayProps {
  sql: string;
}

function highlightSql(sql: string): string {
  const keywords = [
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "OUTER",
    "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET", "AS", "ON",
    "AND", "OR", "NOT", "IN", "LIKE", "BETWEEN", "IS", "NULL",
    "COUNT", "SUM", "AVG", "MAX", "MIN", "DISTINCT", "CASE", "WHEN",
    "THEN", "ELSE", "END", "WITH",
  ];
  let result = sql;
  keywords.forEach((kw) => {
    const re = new RegExp(`\\b(${kw})\\b`, "gi");
    result = result.replace(re, `<span class="sql-keyword">$1</span>`);
  });
  return result;
}

export default function SqlDisplay({ sql }: SqlDisplayProps) {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button className="sql-toggle" onClick={() => setOpen((v) => !v)} id="sql-toggle-btn">
        <span>{open ? "▲" : "▼"}</span>
        <span>View SQL Query</span>
        <span style={{ marginLeft: "auto", fontSize: "0.7rem", opacity: 0.6 }}>
          Transparency Layer
        </span>
      </button>

      {open && (
        <div className="sql-panel">
          <pre
            className="sql-code"
            dangerouslySetInnerHTML={{ __html: highlightSql(sql) }}
          />
        </div>
      )}
    </div>
  );
}

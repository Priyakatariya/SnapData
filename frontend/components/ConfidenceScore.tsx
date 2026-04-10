"use client";

interface ConfidenceScoreProps {
  confidence: number;
}

export default function ConfidenceScore({ confidence }: ConfidenceScoreProps) {
  const pct = Math.round(confidence * 100);

  let level: "high" | "medium" | "low";
  let icon: string;
  let label: string;

  if (pct >= 80) {
    level = "high";
    icon = "✓";
    label = "High Confidence";
  } else if (pct >= 50) {
    level = "medium";
    icon = "~";
    label = "Medium Confidence";
  } else {
    level = "low";
    icon = "!";
    label = "Low Confidence";
  }

  return (
    <span className={`confidence-badge confidence-${level}`}>
      <span>{icon}</span>
      {label} — {pct}%
    </span>
  );
}

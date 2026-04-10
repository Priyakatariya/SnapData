"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

interface ChartProps {
  columns: string[];
  results: Record<string, unknown>[];
}

function isNumeric(value: unknown): boolean {
  return typeof value === "number" || (typeof value === "string" && !isNaN(Number(value)) && value.trim() !== "");
}

export default function DataChart({ columns, results }: ChartProps) {
  if (results.length === 0 || columns.length < 2) return null;

  // Auto-detect: first non-numeric col = label, first numeric col = value
  const labelCol = columns.find((c) => !isNumeric(results[0]?.[c])) ?? columns[0];
  const valueCol = columns.find((c) => c !== labelCol && isNumeric(results[0]?.[c]));

  if (!valueCol) return null;

  const labels = results.map((r) => String(r[labelCol] ?? ""));
  const data = results.map((r) => Number(r[valueCol]) || 0);

  const chartData = {
    labels,
    datasets: [
      {
        label: valueCol.replace(/_/g, " "),
        data,
        backgroundColor: "rgba(92, 124, 250, 0.7)",
        borderColor: "rgba(92, 124, 250, 1)",
        borderWidth: 1,
        borderRadius: 6,
        hoverBackgroundColor: "rgba(124, 58, 237, 0.8)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#8b98c8", font: { size: 12 } },
      },
      tooltip: {
        backgroundColor: "#161b2e",
        titleColor: "#e9ecef",
        bodyColor: "#8b98c8",
        borderColor: "#232a42",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        ticks: { color: "#8b98c8", font: { size: 11 } },
        grid: { color: "rgba(35,42,66,0.6)" },
      },
      y: {
        ticks: { color: "#8b98c8", font: { size: 11 } },
        grid: { color: "rgba(35,42,66,0.6)" },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

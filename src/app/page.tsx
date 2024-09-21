"use client"; // Mark this file as a Client Component

import { useState } from "react";
import axios from "axios";

type ProblemCounts = {
  derivative: number;
  integral: number;
  u_substitution: number;
  integration_by_parts: number;
  trig_integral: number;
  trig_substitution: number;
  partial_fractions: number;
  improper_integral: number;
  limit: number;
  series: number;
};

export default function Home() {
  const [problemCounts, setProblemCounts] = useState<ProblemCounts>({
    derivative: 2,
    integral: 2,
    u_substitution: 1,
    integration_by_parts: 1,
    trig_integral: 1,
    trig_substitution: 1,
    partial_fractions: 1,
    improper_integral: 1,
    limit: 1,
    series: 0,
  });

  const [pdfUrls, setPdfUrls] = useState<{ problems: string; solutions: string } | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProblemCounts({
      ...problemCounts,
      [e.target.name as keyof ProblemCounts]: parseInt(e.target.value), // Type assertion here
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("/api/generate", problemCounts);
      setPdfUrls(response.data); // Set both PDF URLs returned from backend
    } catch (error) {
      console.error("Error generating PDFs:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Calculus Problem Generator</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.keys(problemCounts).map((problemType) => (
          <div key={problemType} className="flex items-center space-x-2">
            <label className="flex-1 text-lg font-semibold text-white-800">
              {problemType.replace(/_/g, " ")} {/* Replaces underscores with spaces */}
            </label>
            <input
              type="number"
              name={problemType}
              value={problemCounts[problemType as keyof ProblemCounts]} // Type assertion here
              onChange={handleChange}
              className="border p-2 rounded text-gray-900 font-semibold w-20"
            />
          </div>
        ))}
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Generate Problems
        </button>
      </form>

      {pdfUrls && (
        <div className="mt-4">
          <p className="text-green-600">Your PDFs are ready!</p>
          <div>
            <a
              href={pdfUrls.problems}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline mr-4"
            >
              Download Problems PDF
            </a>
            <a
              href={pdfUrls.solutions}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline"
            >
              Download Solutions PDF
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

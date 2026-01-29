/**
 * ResultCard Component
 * Displays the analysis results in a visually appealing format
 */

import React from 'react';
import { AnalysisResponse } from '@/types/analysis';

interface ResultCardProps {
  result: AnalysisResponse;
}

const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  const { score, matching_skills, missing_skills, recommendation, strengths, areas_for_improvement } = result;

  // Determine score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-fade-in">
      {/* Score Card */}
      <div className={`card ${getScoreBgColor(score)} border-2 border-opacity-50`}>
        <div className="text-center">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Match Score</h3>
          <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
            {score.toFixed(1)}%
          </div>
          <p className="mt-2 text-sm text-gray-600">
            {score >= 80 ? 'Excellent Match!' : score >= 60 ? 'Good Match' : 'Needs Improvement'}
          </p>
        </div>
      </div>

      {/* Matching Skills */}
      {matching_skills.length > 0 && (
        <div className="card bg-green-50 border border-green-200">
          <h3 className="text-lg font-semibold text-green-800 mb-3 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            Matching Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {matching_skills.map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-green-200 text-green-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Skills */}
      {missing_skills.length > 0 && (
        <div className="card bg-red-50 border border-red-200">
          <h3 className="text-lg font-semibold text-red-800 mb-3 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            Missing Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {missing_skills.map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-red-200 text-red-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Strengths */}
      {strengths && strengths.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Strengths</h3>
          <ul className="space-y-2">
            {strengths.map((strength, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2 mt-1">✓</span>
                <span className="text-gray-700">{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Areas for Improvement */}
      {areas_for_improvement && areas_for_improvement.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Areas for Improvement</h3>
          <ul className="space-y-2">
            {areas_for_improvement.map((area, index) => (
              <li key={index} className="flex items-start">
                <span className="text-yellow-500 mr-2 mt-1">→</span>
                <span className="text-gray-700">{area}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendation */}
      <div className="card bg-blue-50 border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-3">Detailed Recommendation</h3>
        <p className="text-gray-700 leading-relaxed whitespace-pre-line">{recommendation}</p>
      </div>
    </div>
  );
};

export default ResultCard;

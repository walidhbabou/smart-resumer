import React, { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import JobDescriptionInput from '@/components/JobDescriptionInput';
import ResultCard from '@/components/ResultCard';
import { useAnalyzeCV } from '@/hooks/useAnalyzeCV';

const Home: React.FC = () => {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');

  const { mutate: analyzeCV, data, isLoading, error, reset } = useAnalyzeCV();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!cvFile) {
      alert('Please upload a CV file');
      return;
    }

    if (jobDescription.length < 10) {
      alert('Please enter a job description (minimum 10 characters)');
      return;
    }

    // Reset previous results
    reset();

    // Submit analysis
    analyzeCV({
      cv_file: cvFile,
      job_description: jobDescription,
    });
  };

  const handleReset = () => {
    setCvFile(null);
    setJobDescription('');
    reset();
  };

  const isFormValid = cvFile !== null && jobDescription.length >= 10;

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            SmartResume Analyzer
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI-powered CV analysis platform that matches resumes with job descriptions
            and provides actionable insights
          </p>
        </header>

        {/* Main Content */}
        <div className="grid md:grid-cols-1 gap-8">
          {/* Form Section */}
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Analyze Your CV</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <FileUpload
                onFileSelect={setCvFile}
                selectedFile={cvFile}
                disabled={isLoading}
              />

              <JobDescriptionInput
                value={jobDescription}
                onChange={setJobDescription}
                disabled={isLoading}
              />

              {/* Error Display */}
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-start">
                    <svg
                      className="w-5 h-5 text-red-600 mt-0.5 mr-2"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <div>
                      <h3 className="text-sm font-medium text-red-800">Analysis Failed</h3>
                      <p className="text-sm text-red-700 mt-1">{error.message}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={!isFormValid || isLoading}
                  className="flex-1 btn-primary flex items-center justify-center"
                >
                  {isLoading ? (
                    <>
                      <svg
                        className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <svg
                        className="w-5 h-5 mr-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                        />
                      </svg>
                      Analyze CV
                    </>
                  )}
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  disabled={isLoading}
                  className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Reset
                </button>
              </div>
            </form>
          </div>

          {/* Results Section */}
          {data && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                Analysis Results
              </h2>
              <ResultCard result={data} />
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-600 text-sm">
          <p>
            Powered by AI • Built with FastAPI & React • &copy; 2026 SmartResume Analyzer
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Home;

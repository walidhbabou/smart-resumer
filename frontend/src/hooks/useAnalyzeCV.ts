/**
 * useAnalyzeCV Hook
 * React Query hook for CV analysis with loading and error states
 */

import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { api } from '@/services/api';
import { AnalysisRequest, AnalysisResponse } from '@/types/analysis';

export const useAnalyzeCV = () => {
  return useMutation<AnalysisResponse, Error, AnalysisRequest>({
    mutationFn: (data: AnalysisRequest) => api.analyzeCV(data),
    
    onSuccess: (data) => {
      console.log('Analysis successful:', data);
      toast.success('CV analyzed successfully!');
    },
    
    onError: (error: Error) => {
      console.error('Analysis failed:', error);
      toast.error(error.message || 'Failed to analyze CV. Please try again.');
    },
  });
};

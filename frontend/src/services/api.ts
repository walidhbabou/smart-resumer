/**
 * API Service
 * Centralized axios configuration and API calls
 */

import axios from 'axios';
import { AnalysisRequest, AnalysisResponse } from '@/types/analysis';

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for AI processing
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('[API Response Error]', error.response?.data || error.message);
    
    // Enhanced error message
    if (error.response) {
      const errorMessage = error.response.data?.detail || error.response.data?.error || error.message;
      throw new Error(errorMessage);
    } else if (error.request) {
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      throw new Error(error.message);
    }
  }
);

/**
 * API Methods
 */

export const api = {
  /**
   * Analyze CV against job description
   */
  analyzeCV: async (data: AnalysisRequest): Promise<AnalysisResponse> => {
    const formData = new FormData();
    formData.append('cv_file', data.cv_file);
    formData.append('job_description', data.job_description);

    const response = await apiClient.post<AnalysisResponse>('/api/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Health check
   */
  healthCheck: async (): Promise<{ status: string }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default api;

/**
 * JobDescriptionInput Component
 * Textarea for entering job description with character counter
 */

import React from 'react';

interface JobDescriptionInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const JobDescriptionInput: React.FC<JobDescriptionInputProps> = ({
  value,
  onChange,
  disabled = false,
}) => {
  const maxLength = 5000;
  const minLength = 10;

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  const isValid = value.length >= minLength && value.length <= maxLength;
  const charCount = value.length;
  const charRemaining = maxLength - charCount;

  return (
    <div className="w-full">
      <label htmlFor="job-description" className="block text-sm font-medium text-gray-700 mb-2">
        Job Description
      </label>
      
      <textarea
        id="job-description"
        value={value}
        onChange={handleChange}
        disabled={disabled}
        placeholder="Paste the job description here... (minimum 10 characters)"
        className={`
          w-full px-4 py-3 border rounded-lg outline-none transition-all resize-none
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
          ${
            charCount === 0
              ? 'border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent'
              : isValid
              ? 'border-green-400 focus:ring-2 focus:ring-green-500 focus:border-transparent'
              : 'border-red-400 focus:ring-2 focus:ring-red-500 focus:border-transparent'
          }
        `}
        rows={8}
        maxLength={maxLength}
      />

      <div className="mt-2 flex justify-between items-center text-xs">
        <div>
          {charCount > 0 && (
            <span className={charCount < minLength ? 'text-red-600' : 'text-green-600'}>
              {charCount < minLength
                ? `${minLength - charCount} more characters needed`
                : '✓ Valid length'}
            </span>
          )}
        </div>
        <div className={`${charRemaining < 100 ? 'text-red-600' : 'text-gray-500'}`}>
          {charCount} / {maxLength}
        </div>
      </div>

      {charCount >= maxLength && (
        <p className="mt-1 text-xs text-red-600">Maximum character limit reached</p>
      )}
    </div>
  );
};

export default JobDescriptionInput;

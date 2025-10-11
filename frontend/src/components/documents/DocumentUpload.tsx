/**
 * Document Upload Component with Drag-and-Drop
 * Story 1.1: Upload de Manuais Técnicos (PDF) - Task 9
 * AC1, AC2, AC3: File upload with validation and progress
 */
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadDocument } from '@/api/documents';

type UploadState = 'idle' | 'uploading' | 'success' | 'error';

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
  const [uploadState, setUploadState] = useState<UploadState>('idle');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);

  // Subtask 9.1: Client-side validation (AC2)
  const validateFile = (file: File): string | null => {
    // Check file type (PDF only)
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      return 'Only PDF files are allowed';
    }

    // Check file size (max 50MB)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    if (file.size > maxSize) {
      return 'File too large (max 50MB)';
    }

    return null;
  };

  // Subtask 9.3: Handle file upload with progress (AC3)
  const handleUpload = async (file: File) => {
    setUploadState('uploading');
    setUploadProgress(0);
    setErrorMessage(null);

    try {
      await uploadDocument(file, (progress) => {
        setUploadProgress(progress);
      });

      setUploadState('success');
      setUploadedFileName(file.name);

      // Call callback to refresh pending list
      if (onUploadSuccess) {
        onUploadSuccess();
      }

      // Reset after 3 seconds
      setTimeout(() => {
        setUploadState('idle');
        setUploadProgress(0);
        setUploadedFileName(null);
      }, 3000);
    } catch (error: any) {
      setUploadState('error');
      setErrorMessage(
        error.response?.data?.detail || 'Upload failed. Please try again.'
      );

      // Reset after 5 seconds
      setTimeout(() => {
        setUploadState('idle');
        setErrorMessage(null);
      }, 5000);
    }
  };

  // Subtask 9.1: Drag-and-drop with react-dropzone
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];

    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      setUploadState('error');
      setErrorMessage(validationError);

      setTimeout(() => {
        setUploadState('idle');
        setErrorMessage(null);
      }, 5000);
      return;
    }

    // Upload file
    handleUpload(file);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Upload de Manuais Técnicos</h2>

      {/* Subtask 9.4: Upload states (idle, uploading, success, error) */}
      <div
        {...getRootProps()}
        data-testid="upload-dropzone"
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${uploadState === 'uploading' ? 'pointer-events-none opacity-50' : ''}
        `}
      >
        <input {...getInputProps()} />

        {uploadState === 'idle' && (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p className="mt-2 text-sm text-gray-600">
              {isDragActive
                ? 'Solte o arquivo aqui'
                : 'Arraste um arquivo PDF ou clique para selecionar'}
            </p>
            <p className="mt-1 text-xs text-gray-500">PDF até 50MB</p>
          </div>
        )}

        {/* Subtask 9.3: Progress bar (AC3) */}
        {uploadState === 'uploading' && (
          <div>
            <p className="text-sm text-gray-600 mb-2">Enviando...</p>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="mt-2 text-sm text-gray-600">{uploadProgress}%</p>
          </div>
        )}

        {uploadState === 'success' && (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            <p className="mt-2 text-sm text-green-600">
              Upload concluído: {uploadedFileName}
            </p>
          </div>
        )}

        {uploadState === 'error' && (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-red-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
            <p className="mt-2 text-sm text-red-600">{errorMessage}</p>
          </div>
        )}
      </div>

      {/* Validation info */}
      <div className="mt-4 text-xs text-gray-500">
        <p>✓ Apenas arquivos PDF (.pdf)</p>
        <p>✓ Tamanho máximo: 50MB</p>
        <p>✓ Apenas administradores podem fazer upload</p>
      </div>
    </div>
  );
};

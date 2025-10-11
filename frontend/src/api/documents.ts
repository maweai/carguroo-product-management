/**
 * API Client for Documents
 * Story 1.1: Upload de Manuais Técnicos (PDF)
 */
import axios, { AxiosProgressEvent } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Document {
  id: string;
  name: string;
  size_bytes: number;
  status: 'pending' | 'processing' | 'completed' | 'error';
  uploaded_at: string;
  uploaded_by?: string;
}

export interface UploadResponse {
  document_id: string;
  name: string;
  size_bytes: number;
  status: string;
  uploaded_at: string;
  processing_eta_seconds: number;
}

export interface ListDocumentsResponse {
  documents: Document[];
  total: number;
  limit: number;
  offset: number;
}

/**
 * Upload PDF document with progress tracking
 * AC3: Progress bar implementation
 */
export const uploadDocument = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post<UploadResponse>(
    `${API_URL}/api/v1/documents/upload`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent: AxiosProgressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(progress);
        }
      },
    }
  );

  return response.data;
};

/**
 * List documents with optional status filter
 * AC4: Pending documents list
 */
export const listDocuments = async (
  status?: string,
  limit: number = 20,
  offset: number = 0
): Promise<ListDocumentsResponse> => {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());

  const response = await axios.get<ListDocumentsResponse>(
    `${API_URL}/api/v1/documents?${params.toString()}`
  );

  return response.data;
};

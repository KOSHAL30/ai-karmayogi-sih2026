// ==============================================================================
// AI KARMAYOGI — CENTRAL API CLIENT
// Typed Fetch Wrapper with Automatic JWT Token Injection, Retry Logic & Toasts
// ==============================================================================

import { notify } from '@/context/ToastContext';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export class APIClientError extends Error {
  constructor(
    public code: string,
    public message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIClientError';
  }
}

interface RequestOptions extends RequestInit {
  retries?: number;
  silent?: boolean;
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const token = null;
  const maxRetries = options.retries ?? (options.method === 'GET' || !options.method ? 2 : 0);

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  `;
  }

  // Handle FormData upload where Content-Type is automatically set by browser
  if (options.body instanceof FormData) {
    delete (headers as Record<string, string>)['Content-Type'];
  }

  const config: RequestInit = {
      credentials: 'include',
    ...options,
    headers,
  };

  let attempt = 0;
  while (attempt <= maxRetries) {
    try {
      // Check client network status
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        throw new APIClientError('OFFLINE', 'Network is currently offline. Please check connection.', 0);
      }

      const response = await fetch(url, config);
      const contentType = response.headers.get('content-type');
      let data: any = null;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      // Handle 401 Unauthorized Session Expiry
      if (response.status === 401) {
        const refreshToken = localStorage.getItem('karmayogi_refresh_token');
        if (refreshToken && attempt === 0) {
          try {
            // Attempt token refresh
            const refreshRes = await fetch(`${API_BASE}/auth/refresh`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ refresh_token: refreshToken }),
            });
            if (refreshRes.ok) {
              const refreshData = await refreshRes.json();
              const newToken = refreshData.access_token || refreshData.data?.access_token;
              if (newToken) {
                localStorage.setItem('karmayogi_token', newToken);
                (headers as Record<string, string>)['Authorization'] = `Bearer ${newToken}`;
                attempt++;
                continue;
              }
            }
          } catch {
            // Refresh failed, fall through to logout
          }
        }
      }

      if (!response.ok) {
        const errorCode = data?.error?.code || (data?.detail ? 'API_ERROR' : 'HTTP_ERROR');
        const errorMessage =
          data?.error?.message || data?.detail || response.statusText || 'An unexpected error occurred.';
        throw new APIClientError(errorCode, errorMessage, response.status, data?.error?.details);
      }

      // Return the inner 'data' payload if wrapped in standard APIResponse envelope
      if (data && typeof data === 'object' && 'data' in data && 'status' in data) {
        return data.data as T;
      }

      return data as T;
    } catch (err: any) {
      attempt++;
      if (attempt <= maxRetries && (err.status >= 500 || err.code === 'NETWORK_ERROR' || err.name === 'TypeError')) {
        // Exponential backoff retry
        await sleep(Math.min(1000 * Math.pow(2, attempt - 1), 3000));
        continue;
      }

      // If error occurs and not silent, notify user
      if (!options.silent && err instanceof APIClientError && err.status !== 401 && err.status !== 404) {
        notify({
          type: 'error',
          title: err.code === 'OFFLINE' ? 'Offline Mode' : 'Service Alert',
          description: err.message,
        });
      }

      if (err instanceof APIClientError) {
        throw err;
      }
      throw new APIClientError('NETWORK_ERROR', err.message || 'Network connection failed.', 0);
    }
  }

  throw new APIClientError('MAX_RETRIES_EXCEEDED', 'Service request exceeded maximum retry attempts.', 0);
}

export const api = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
    }),

  put: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: body instanceof FormData ? body : JSON.stringify(body),
    }),

  delete: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: 'DELETE' }),
};

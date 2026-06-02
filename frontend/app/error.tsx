'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('Page error:', error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-gray-50 p-8">
      <div className="rounded-full bg-red-100 p-6">
        <svg
          className="h-12 w-12 text-red-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
          />
        </svg>
      </div>
      <h2 className="text-2xl font-bold text-gray-800">Something went wrong</h2>
      <p className="max-w-md text-center text-gray-600">
        An unexpected error occurred. Please try again or contact us if the
        problem persists.
      </p>
      <button
        onClick={reset}
        className="rounded-md bg-orange-500 px-8 py-3 text-lg text-white transition hover:bg-orange-600"
      >
        Try Again
      </button>
    </div>
  );
}

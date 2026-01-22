/**
 * StatCard Component
 * Reusable card for displaying statistics with optional icon and trend indicator
 */

import type { ReactNode } from 'react';
import clsx from 'clsx';

export interface StatCardProps {
  label: string;
  value: string | number;
  icon?: ReactNode;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  color?: 'primary' | 'success' | 'warning' | 'danger';
  className?: string;
}

const colorClasses = {
  primary: 'text-primary-600 bg-primary-50',
  success: 'text-green-600 bg-green-50',
  warning: 'text-yellow-600 bg-yellow-50',
  danger: 'text-red-600 bg-red-50',
};

export function StatCard({
  label,
  value,
  icon,
  trend,
  color = 'primary',
  className,
}: StatCardProps) {
  return (
    <div
      className={clsx(
        'bg-white rounded-lg shadow p-6 border border-gray-200',
        className
      )}
    >
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-gray-600">{label}</p>
        {icon && (
          <div className={clsx('p-2 rounded-lg', colorClasses[color])}>
            {icon}
          </div>
        )}
      </div>

      <div className="flex items-baseline justify-between">
        <p className="text-3xl font-bold text-gray-900">{value}</p>

        {trend && (
          <div
            className={clsx(
              'flex items-center text-sm font-medium',
              trend.direction === 'up' ? 'text-green-600' : 'text-red-600'
            )}
          >
            {trend.direction === 'up' ? (
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
                />
              </svg>
            ) : (
              <svg
                className="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 14l-7 7m0 0l-7-7m7 7V3"
                />
              </svg>
            )}
            {trend.value}%
          </div>
        )}
      </div>
    </div>
  );
}

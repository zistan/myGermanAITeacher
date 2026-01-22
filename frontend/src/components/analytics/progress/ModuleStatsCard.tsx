/**
 * ModuleStatsCard Component
 * Displays statistics for a specific module (Conversation/Grammar/Vocabulary)
 */

import React from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';

export interface ModuleStatsCardProps {
  title: string;
  icon: React.ReactNode;
  stats: Array<{
    label: string;
    value: string | number;
  }>;
  progressPercentage?: number;
  linkTo: string;
  color: 'blue' | 'purple' | 'green';
}

const colorClasses = {
  blue: {
    bg: 'bg-blue-50',
    text: 'text-blue-600',
    border: 'border-blue-200',
    progressBg: 'bg-blue-200',
    progressFill: 'bg-blue-600',
  },
  purple: {
    bg: 'bg-purple-50',
    text: 'text-purple-600',
    border: 'border-purple-200',
    progressBg: 'bg-purple-200',
    progressFill: 'bg-purple-600',
  },
  green: {
    bg: 'bg-green-50',
    text: 'text-green-600',
    border: 'border-green-200',
    progressBg: 'bg-green-200',
    progressFill: 'bg-green-600',
  },
};

export function ModuleStatsCard({
  title,
  icon,
  stats,
  progressPercentage,
  linkTo,
  color,
}: ModuleStatsCardProps) {
  const colors = colorClasses[color];

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={clsx('p-2 rounded-lg', colors.bg, colors.text)}>
            {icon}
          </div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        {stats.map((stat, index) => (
          <div key={index}>
            <p className="text-sm text-gray-600">{stat.label}</p>
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Progress Bar */}
      {progressPercentage !== undefined && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm text-gray-600">Progress</span>
            <span className="text-sm font-medium text-gray-900">
              {progressPercentage}%
            </span>
          </div>
          <div className={clsx('w-full h-2 rounded-full', colors.progressBg)}>
            <div
              className={clsx('h-2 rounded-full transition-all', colors.progressFill)}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Link */}
      <Link
        to={linkTo}
        className={clsx(
          'inline-flex items-center text-sm font-medium hover:underline',
          colors.text
        )}
      >
        View Module
        <svg
          className="w-4 h-4 ml-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </Link>
    </div>
  );
}

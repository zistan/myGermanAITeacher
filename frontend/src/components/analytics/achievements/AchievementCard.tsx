/**
 * AchievementCard Component
 * Displays an achievement with 3 variants: earned, in-progress, locked
 */

import clsx from 'clsx';
import { format } from 'date-fns';
import type { AchievementResponse } from '../../../api/types/analytics.types';

export interface AchievementCardProps {
  achievement: AchievementResponse;
  variant: 'earned' | 'in-progress' | 'locked';
  earnedDate?: string | null;
  currentProgress?: number;
  targetValue?: number;
  progressPercentage?: number;
  isShowcased?: boolean;
  onToggleShowcase?: (achievementId: number, showcased: boolean) => void;
}

// Tier colors as specified in plan
const TIER_COLORS = {
  bronze: {
    bg: 'bg-slate-50',
    border: 'border-slate-400',
    text: 'text-slate-700',
    badge: '#94a3b8',
  },
  silver: {
    bg: 'bg-blue-50',
    border: 'border-blue-400',
    text: 'text-blue-700',
    badge: '#60a5fa',
  },
  gold: {
    bg: 'bg-amber-50',
    border: 'border-amber-400',
    text: 'text-amber-700',
    badge: '#fbbf24',
  },
  platinum: {
    bg: 'bg-purple-50',
    border: 'border-purple-400',
    text: 'text-purple-700',
    badge: '#a78bfa',
  },
};

export function AchievementCard({
  achievement,
  variant,
  earnedDate,
  currentProgress = 0,
  targetValue = achievement.criteria_value,
  progressPercentage = 0,
  isShowcased = false,
  onToggleShowcase,
}: AchievementCardProps) {
  const tierColors = TIER_COLORS[achievement.tier];

  // Variant-specific styling
  const isEarned = variant === 'earned';
  const isInProgress = variant === 'in-progress';
  const isLocked = variant === 'locked';

  return (
    <div
      className={clsx(
        'rounded-lg border-2 p-4 transition-all',
        tierColors.bg,
        tierColors.border,
        isLocked && 'opacity-60 grayscale',
        !isLocked && 'hover:shadow-lg'
      )}
    >
      {/* Header with icon and showcase toggle */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          {/* Badge Icon */}
          <div
            className={clsx(
              'w-12 h-12 rounded-full flex items-center justify-center text-2xl',
              isLocked ? 'bg-gray-200' : tierColors.bg
            )}
            style={{
              backgroundColor: isLocked ? '#e5e7eb' : tierColors.badge,
            }}
          >
            {isLocked ? '🔒' : achievement.badge_icon || '🏆'}
          </div>

          {/* Tier Badge */}
          <div>
            <h3 className={clsx('font-semibold text-sm', tierColors.text)}>
              {achievement.name}
            </h3>
            <span
              className={clsx(
                'inline-block px-2 py-0.5 text-xs font-medium rounded capitalize',
                tierColors.text,
                tierColors.bg
              )}
            >
              {achievement.tier}
            </span>
          </div>
        </div>

        {/* Showcase Toggle (only for earned) */}
        {isEarned && onToggleShowcase && (
          <button
            onClick={() => onToggleShowcase(achievement.id, !isShowcased)}
            className={clsx(
              'p-1 rounded transition-colors',
              isShowcased
                ? 'text-yellow-500 hover:text-yellow-600'
                : 'text-gray-400 hover:text-gray-600'
            )}
            title={isShowcased ? 'Remove from showcase' : 'Add to showcase'}
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        )}
      </div>

      {/* Description */}
      <p className="text-sm text-gray-700 mb-3">{achievement.description}</p>

      {/* Progress Section */}
      {isEarned && earnedDate && (
        <div className="flex items-center justify-between text-xs text-gray-600">
          <span>Earned: {format(new Date(earnedDate), 'MMM d, yyyy')}</span>
          <span className="font-medium">{achievement.points} pts</span>
        </div>
      )}

      {isInProgress && (
        <div>
          <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
            <span>
              {currentProgress} / {targetValue}
            </span>
            <span className="font-medium">{progressPercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={clsx('h-2 rounded-full transition-all', tierColors.text)}
              style={{
                width: `${progressPercentage}%`,
                backgroundColor: tierColors.badge,
              }}
            />
          </div>
        </div>
      )}

      {isLocked && (
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span className="italic">Locked</span>
          <span>{achievement.points} pts</span>
        </div>
      )}
    </div>
  );
}

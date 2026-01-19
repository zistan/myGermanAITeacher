import { type HTMLAttributes } from 'react';
import clsx from 'clsx';
import type { MasteryLevel } from '../../api/types/common.types';

export interface MasteryIndicatorProps extends HTMLAttributes<HTMLDivElement> {
  level: MasteryLevel | null;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  testId?: string;
}

const masteryConfig: Record<
  number,
  { label: string; color: string; bgColor: string; description: string }
> = {
  0: {
    label: 'New',
    color: 'text-gray-600',
    bgColor: 'bg-gray-200',
    description: 'Not yet reviewed',
  },
  1: {
    label: 'Learning',
    color: 'text-red-600',
    bgColor: 'bg-red-500',
    description: 'Just started learning',
  },
  2: {
    label: 'Familiar',
    color: 'text-orange-600',
    bgColor: 'bg-orange-500',
    description: 'Recognized but needs practice',
  },
  3: {
    label: 'Comfortable',
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-500',
    description: 'Can recall with some effort',
  },
  4: {
    label: 'Confident',
    color: 'text-blue-600',
    bgColor: 'bg-blue-500',
    description: 'Quick and accurate recall',
  },
  5: {
    label: 'Mastered',
    color: 'text-green-600',
    bgColor: 'bg-green-500',
    description: 'Fully learned',
  },
};

export function MasteryIndicator({
  level,
  size = 'md',
  showLabel = true,
  className,
  testId,
  ...props
}: MasteryIndicatorProps) {
  const effectiveLevel = level ?? 0;
  const config = masteryConfig[effectiveLevel];

  const sizeStyles = {
    sm: {
      container: 'gap-1',
      bar: 'h-1.5 w-16',
      segment: 'h-1.5',
      text: 'text-xs',
    },
    md: {
      container: 'gap-2',
      bar: 'h-2 w-24',
      segment: 'h-2',
      text: 'text-sm',
    },
    lg: {
      container: 'gap-2',
      bar: 'h-2.5 w-32',
      segment: 'h-2.5',
      text: 'text-base',
    },
  };

  const styles = sizeStyles[size];

  return (
    <div
      className={clsx('flex items-center', styles.container, className)}
      data-testid={testId}
      title={config.description}
      {...props}
    >
      {/* Progress bar */}
      <div className={clsx('flex rounded-full overflow-hidden bg-gray-200', styles.bar)}>
        {[1, 2, 3, 4, 5].map((segment) => (
          <div
            key={segment}
            className={clsx(
              'flex-1 transition-colors duration-200',
              segment <= effectiveLevel ? config.bgColor : 'bg-gray-200',
              segment > 1 && 'border-l border-white/30'
            )}
          />
        ))}
      </div>

      {/* Label */}
      {showLabel && (
        <span className={clsx('font-medium', config.color, styles.text)}>{config.label}</span>
      )}
    </div>
  );
}

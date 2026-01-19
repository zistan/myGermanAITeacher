import { type HTMLAttributes } from 'react';
import clsx from 'clsx';
import type { DifficultyLevel } from '../../api/types/common.types';

export interface DifficultyBadgeProps extends HTMLAttributes<HTMLSpanElement> {
  level: DifficultyLevel;
  size?: 'sm' | 'md' | 'lg';
  showDescription?: boolean;
  testId?: string;
}

const difficultyConfig: Record<
  DifficultyLevel,
  { label: string; color: string; bgColor: string; description: string }
> = {
  A1: {
    label: 'A1',
    color: 'text-green-800',
    bgColor: 'bg-green-100',
    description: 'Anfänger',
  },
  A2: {
    label: 'A2',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    description: 'Grundkenntnisse',
  },
  B1: {
    label: 'B1',
    color: 'text-yellow-800',
    bgColor: 'bg-yellow-100',
    description: 'Mittelstufe',
  },
  B2: {
    label: 'B2',
    color: 'text-orange-800',
    bgColor: 'bg-orange-100',
    description: 'Obere Mittelstufe',
  },
  C1: {
    label: 'C1',
    color: 'text-red-800',
    bgColor: 'bg-red-100',
    description: 'Fortgeschritten',
  },
  C2: {
    label: 'C2',
    color: 'text-purple-800',
    bgColor: 'bg-purple-100',
    description: 'Proficient',
  },
};

export function DifficultyBadge({
  level,
  size = 'md',
  showDescription = false,
  className,
  testId,
  ...props
}: DifficultyBadgeProps) {
  const config = difficultyConfig[level];

  const sizeStyles = {
    sm: 'px-1.5 py-0.5 text-xs',
    md: 'px-2 py-1 text-sm',
    lg: 'px-2.5 py-1.5 text-base',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center justify-center font-semibold rounded-md',
        config.bgColor,
        config.color,
        sizeStyles[size],
        className
      )}
      data-testid={testId}
      title={config.description}
      {...props}
    >
      {config.label}
      {showDescription && (
        <span className="ml-1 font-normal opacity-80">({config.description})</span>
      )}
    </span>
  );
}

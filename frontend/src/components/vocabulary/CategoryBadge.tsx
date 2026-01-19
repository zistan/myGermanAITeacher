import { type HTMLAttributes } from 'react';
import clsx from 'clsx';

export interface CategoryBadgeProps extends HTMLAttributes<HTMLSpanElement> {
  category: string;
  size?: 'sm' | 'md' | 'lg';
  testId?: string;
}

// Predefined categories with icons and colors
const categoryConfig: Record<string, { icon: string; color: string; bgColor: string }> = {
  business: {
    icon: '💼',
    color: 'text-blue-800',
    bgColor: 'bg-blue-100',
  },
  daily: {
    icon: '🏠',
    color: 'text-green-800',
    bgColor: 'bg-green-100',
  },
  verbs: {
    icon: '🔄',
    color: 'text-purple-800',
    bgColor: 'bg-purple-100',
  },
  nouns: {
    icon: '📦',
    color: 'text-yellow-800',
    bgColor: 'bg-yellow-100',
  },
  adjectives: {
    icon: '✨',
    color: 'text-pink-800',
    bgColor: 'bg-pink-100',
  },
  finance: {
    icon: '💰',
    color: 'text-emerald-800',
    bgColor: 'bg-emerald-100',
  },
  technology: {
    icon: '💻',
    color: 'text-cyan-800',
    bgColor: 'bg-cyan-100',
  },
  travel: {
    icon: '✈️',
    color: 'text-indigo-800',
    bgColor: 'bg-indigo-100',
  },
  food: {
    icon: '🍽️',
    color: 'text-orange-800',
    bgColor: 'bg-orange-100',
  },
  health: {
    icon: '🏥',
    color: 'text-red-800',
    bgColor: 'bg-red-100',
  },
  culture: {
    icon: '🎭',
    color: 'text-violet-800',
    bgColor: 'bg-violet-100',
  },
  idioms: {
    icon: '💬',
    color: 'text-teal-800',
    bgColor: 'bg-teal-100',
  },
};

// Default config for unknown categories
const defaultConfig = {
  icon: '📝',
  color: 'text-gray-800',
  bgColor: 'bg-gray-100',
};

export function CategoryBadge({
  category,
  size = 'md',
  className,
  testId,
  ...props
}: CategoryBadgeProps) {
  const normalizedCategory = category.toLowerCase();
  const config = categoryConfig[normalizedCategory] || defaultConfig;

  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-2.5 py-1 text-sm gap-1.5',
    lg: 'px-3 py-1.5 text-base gap-2',
  };

  // Capitalize first letter of category for display
  const displayCategory = category.charAt(0).toUpperCase() + category.slice(1).toLowerCase();

  return (
    <span
      className={clsx(
        'inline-flex items-center font-medium rounded-full',
        config.bgColor,
        config.color,
        sizeStyles[size],
        className
      )}
      data-testid={testId}
      {...props}
    >
      <span className="flex-shrink-0">{config.icon}</span>
      <span>{displayCategory}</span>
    </span>
  );
}

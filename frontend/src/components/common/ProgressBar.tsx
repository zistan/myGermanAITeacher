import clsx from 'clsx';

export interface ProgressBarProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'success' | 'danger' | 'warning';
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export function ProgressBar({
  value,
  max = 100,
  size = 'md',
  color = 'primary',
  showLabel = false,
  label,
  className,
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const sizeStyles = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  const colorStyles = {
    primary: 'bg-primary-500',
    success: 'bg-green-500',
    danger: 'bg-danger-500',
    warning: 'bg-yellow-500',
  };

  return (
    <div className={className}>
      {(showLabel || label) && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-sm font-medium text-gray-700">
            {label || `${Math.round(percentage)}%`}
          </span>
          {showLabel && !label && (
            <span className="text-sm text-gray-500">
              {value} / {max}
            </span>
          )}
        </div>
      )}
      <div className={clsx('w-full bg-gray-200 rounded-full overflow-hidden', sizeStyles[size])}>
        <div
          className={clsx('h-full rounded-full transition-all duration-300', colorStyles[color])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

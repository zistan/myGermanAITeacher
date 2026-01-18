import clsx from 'clsx';

export interface SkeletonProps {
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  className?: string;
}

export function Skeleton({
  variant = 'text',
  width,
  height,
  className,
}: SkeletonProps) {
  const baseStyles = 'animate-pulse bg-gray-300';

  const variantStyles = {
    text: 'rounded h-4',
    circular: 'rounded-full',
    rectangular: 'rounded',
  };

  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === 'number' ? `${width}px` : width;
  if (height) style.height = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={clsx(baseStyles, variantStyles[variant], className)}
      style={style}
    />
  );
}

export interface SkeletonGroupProps {
  count?: number;
  spacing?: string;
  children?: React.ReactNode;
}

export function SkeletonGroup({
  count = 3,
  spacing = 'space-y-2',
  children,
}: SkeletonGroupProps) {
  if (children) {
    return <div className={spacing}>{children}</div>;
  }

  return (
    <div className={spacing}>
      {Array.from({ length: count }).map((_, index) => (
        <Skeleton key={index} />
      ))}
    </div>
  );
}

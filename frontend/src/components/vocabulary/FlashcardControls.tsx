import clsx from 'clsx';

export interface FlashcardControlsProps {
  onRate: (confidence: 1 | 2 | 3 | 4 | 5) => void;
  disabled?: boolean;
}

interface RatingOption {
  value: 1 | 2 | 3 | 4 | 5;
  label: string;
  description: string;
  color: string;
  bgColor: string;
  hoverColor: string;
}

const ratingOptions: RatingOption[] = [
  {
    value: 1,
    label: 'Again',
    description: "Didn't know it",
    color: 'text-red-700',
    bgColor: 'bg-red-50',
    hoverColor: 'hover:bg-red-100',
  },
  {
    value: 2,
    label: 'Hard',
    description: 'Struggled to recall',
    color: 'text-orange-700',
    bgColor: 'bg-orange-50',
    hoverColor: 'hover:bg-orange-100',
  },
  {
    value: 3,
    label: 'Good',
    description: 'Recalled with effort',
    color: 'text-yellow-700',
    bgColor: 'bg-yellow-50',
    hoverColor: 'hover:bg-yellow-100',
  },
  {
    value: 4,
    label: 'Easy',
    description: 'Recalled quickly',
    color: 'text-blue-700',
    bgColor: 'bg-blue-50',
    hoverColor: 'hover:bg-blue-100',
  },
  {
    value: 5,
    label: 'Perfect',
    description: 'Instant recall',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    hoverColor: 'hover:bg-green-100',
  },
];

export function FlashcardControls({ onRate, disabled = false }: FlashcardControlsProps) {
  return (
    <div className="space-y-3">
      <p className="text-center text-sm text-gray-600 font-medium">
        Rate your recall
      </p>
      <div className="flex flex-wrap justify-center gap-2 md:gap-3">
        {ratingOptions.map((option) => (
          <button
            key={option.value}
            onClick={() => onRate(option.value)}
            disabled={disabled}
            className={clsx(
              'flex flex-col items-center px-4 py-3 rounded-lg border-2 transition-all min-w-[80px]',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              option.bgColor,
              option.hoverColor,
              option.color,
              'border-transparent hover:border-current',
              'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
            )}
            data-testid={`rate-${option.value}-btn`}
          >
            <span className="text-lg font-bold">{option.label}</span>
            <span className="text-xs opacity-75">{option.description}</span>
          </button>
        ))}
      </div>
      <div className="text-center text-xs text-gray-400 mt-2">
        Press <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded">1</kbd>-
        <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded">5</kbd> to rate
      </div>
    </div>
  );
}

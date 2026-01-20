interface GermanKeyboardHelperProps {
  onInsertChar: (char: string) => void;
}

const GERMAN_CHARS = [
  { char: 'ä', shortcut: 'Alt+A' },
  { char: 'ö', shortcut: 'Alt+O' },
  { char: 'ü', shortcut: 'Alt+U' },
  { char: 'ß', shortcut: 'Alt+S' },
];

export function GermanKeyboardHelper({ onInsertChar }: GermanKeyboardHelperProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500 font-medium">German Characters:</span>
      <div className="flex gap-1">
        {GERMAN_CHARS.map(({ char, shortcut }) => (
          <button
            key={char}
            onClick={() => onInsertChar(char)}
            className="px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded border border-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            title={`Insert ${char} (${shortcut})`}
          >
            {char}
          </button>
        ))}
      </div>
    </div>
  );
}

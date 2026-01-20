import { useState } from 'react';
import type { VocabularyItem } from '../../api/types/conversation.types';

interface VocabularyHighlightProps {
  text: string;
  vocabulary: VocabularyItem[];
  enabled: boolean;
  onWordClick?: (wordId: number) => void;
}

export function VocabularyHighlight({
  text,
  vocabulary,
  enabled,
  onWordClick,
}: VocabularyHighlightProps) {
  const [hoveredWord, setHoveredWord] = useState<VocabularyItem | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  if (!enabled || vocabulary.length === 0) {
    return <span>{text}</span>;
  }

  /**
   * Split text and highlight vocabulary words
   */
  const renderHighlightedText = () => {
    const parts: JSX.Element[] = [];
    let lastIndex = 0;

    // Sort vocabulary by position in text (longest first to avoid partial matches)
    const sortedVocab = [...vocabulary].sort(
      (a, b) => b.word.length - a.word.length
    );

    // Create a map of word positions
    const wordPositions: Array<{
      start: number;
      end: number;
      vocab: VocabularyItem;
    }> = [];

    sortedVocab.forEach((vocab) => {
      const regex = new RegExp(`\\b${escapeRegex(vocab.word)}\\b`, 'gi');
      let match;

      while ((match = regex.exec(text)) !== null) {
        // Check if this position overlaps with existing highlights
        const overlaps = wordPositions.some(
          (pos) =>
            (match!.index >= pos.start && match!.index < pos.end) ||
            (match!.index + match![0].length > pos.start &&
              match!.index + match![0].length <= pos.end)
        );

        if (!overlaps) {
          wordPositions.push({
            start: match.index,
            end: match.index + match[0].length,
            vocab,
          });
        }
      }
    });

    // Sort positions by start index
    wordPositions.sort((a, b) => a.start - b.start);

    // Build highlighted text
    wordPositions.forEach((pos, index) => {
      // Add text before highlight
      if (pos.start > lastIndex) {
        parts.push(
          <span key={`text-${index}`}>{text.substring(lastIndex, pos.start)}</span>
        );
      }

      // Add highlighted word
      const word = text.substring(pos.start, pos.end);
      parts.push(
        <span
          key={`vocab-${index}`}
          className="relative inline-block cursor-pointer border-b-2 border-blue-400 border-dotted hover:bg-blue-50 transition-colors"
          onMouseEnter={(e) => {
            setHoveredWord(pos.vocab);
            const rect = e.currentTarget.getBoundingClientRect();
            setTooltipPosition({ x: rect.left, y: rect.bottom });
          }}
          onMouseLeave={() => setHoveredWord(null)}
          onClick={() => onWordClick?.(pos.vocab.word_id)}
        >
          {word}
        </span>
      );

      lastIndex = pos.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(<span key="text-end">{text.substring(lastIndex)}</span>);
    }

    return parts;
  };

  /**
   * Escape special regex characters
   */
  function escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Get difficulty badge color
   */
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'A1':
      case 'A2':
        return 'bg-green-100 text-green-700';
      case 'B1':
      case 'B2':
        return 'bg-blue-100 text-blue-700';
      case 'C1':
      case 'C2':
        return 'bg-purple-100 text-purple-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <>
      <span>{renderHighlightedText()}</span>

      {/* Tooltip */}
      {hoveredWord && (
        <div
          className="fixed z-50 bg-white border border-gray-200 rounded-lg shadow-lg p-3 max-w-xs"
          style={{
            left: `${tooltipPosition.x}px`,
            top: `${tooltipPosition.y + 8}px`,
          }}
        >
          <div className="space-y-2 text-sm">
            <div className="flex items-start justify-between gap-2">
              <span className="font-semibold text-gray-900">{hoveredWord.word}</span>
              <div className="flex items-center gap-1">
                <span
                  className={`px-2 py-0.5 text-xs font-medium rounded ${getDifficultyColor(
                    hoveredWord.difficulty
                  )}`}
                >
                  {hoveredWord.difficulty}
                </span>
                {hoveredWord.is_new && (
                  <span className="px-2 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700 rounded">
                    New
                  </span>
                )}
              </div>
            </div>
            <div className="text-gray-700">
              <span className="text-gray-500">Translation:</span>{' '}
              {hoveredWord.translation_it}
            </div>
            {hoveredWord.category && (
              <div className="text-xs text-gray-500">
                Category: {hoveredWord.category}
              </div>
            )}
            <div className="pt-2 border-t border-gray-200 text-xs text-blue-600">
              Click to add to vocabulary list
            </div>
          </div>
        </div>
      )}
    </>
  );
}

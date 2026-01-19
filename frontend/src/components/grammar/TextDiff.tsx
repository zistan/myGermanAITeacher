import { useMemo } from 'react';
import { diff_match_patch, DIFF_DELETE, DIFF_INSERT, DIFF_EQUAL } from 'diff-match-patch';
import clsx from 'clsx';

// ========== TYPES ==========

export interface TextDiffProps {
  /** The original/expected text (correct answer) */
  original: string;
  /** The modified/user text (user's answer) */
  modified: string;
  /** Display mode: 'inline' shows both in one line, 'side-by-side' shows them separately */
  mode?: 'inline' | 'side-by-side';
  /** Whether to show a legend explaining the colors */
  showLegend?: boolean;
  /** Additional class names */
  className?: string;
  /** Whether to use word-by-word diff instead of character-by-character */
  wordLevel?: boolean;
  /** Whether to ignore case when comparing */
  ignoreCase?: boolean;
  /** Whether to trim whitespace when comparing */
  trimWhitespace?: boolean;
}

// ========== HELPER FUNCTIONS ==========

const dmp = new diff_match_patch();

function computeDiff(
  original: string,
  modified: string,
  options: {
    wordLevel?: boolean;
    ignoreCase?: boolean;
    trimWhitespace?: boolean;
  }
): Array<[number, string]> {
  let originalText = original;
  let modifiedText = modified;

  // Apply preprocessing
  if (options.trimWhitespace) {
    originalText = originalText.trim();
    modifiedText = modifiedText.trim();
  }

  if (options.ignoreCase) {
    // For case-insensitive comparison, we'll compare lowercase but preserve original case
    const lowerOriginal = originalText.toLowerCase();
    const lowerModified = modifiedText.toLowerCase();
    const diffs = dmp.diff_main(lowerOriginal, lowerModified);
    dmp.diff_cleanupSemantic(diffs);
    return diffs;
  }

  // Compute diff
  const diffs = dmp.diff_main(originalText, modifiedText);
  dmp.diff_cleanupSemantic(diffs);

  // For word-level diff, post-process to align on word boundaries
  if (options.wordLevel) {
    return cleanupToWordBoundaries(diffs);
  }

  return diffs;
}

function cleanupToWordBoundaries(
  diffs: Array<[number, string]>
): Array<[number, string]> {
  // This is a simplified word-boundary cleanup
  // In a real implementation, you might want more sophisticated logic
  const result: Array<[number, string]> = [];

  for (const [operation, text] of diffs) {
    // Split on word boundaries but keep the delimiters
    const parts = text.split(/(\s+)/);
    for (const part of parts) {
      if (part.length > 0) {
        result.push([operation, part]);
      }
    }
  }

  // Merge consecutive operations of the same type
  const merged: Array<[number, string]> = [];
  for (const [operation, text] of result) {
    if (merged.length > 0 && merged[merged.length - 1][0] === operation) {
      merged[merged.length - 1][1] += text;
    } else {
      merged.push([operation, text]);
    }
  }

  return merged;
}

// ========== COMPONENT ==========

export function TextDiff({
  original,
  modified,
  mode = 'inline',
  showLegend = true,
  className,
  wordLevel = false,
  ignoreCase = false,
  trimWhitespace = true,
}: TextDiffProps) {
  const diffs = useMemo(
    () =>
      computeDiff(original, modified, {
        wordLevel,
        ignoreCase,
        trimWhitespace,
      }),
    [original, modified, wordLevel, ignoreCase, trimWhitespace]
  );

  // Check if the texts are identical
  const isIdentical = useMemo(() => {
    const processedOriginal = trimWhitespace ? original.trim() : original;
    const processedModified = trimWhitespace ? modified.trim() : modified;
    return ignoreCase
      ? processedOriginal.toLowerCase() === processedModified.toLowerCase()
      : processedOriginal === processedModified;
  }, [original, modified, ignoreCase, trimWhitespace]);

  if (isIdentical) {
    return (
      <div className={clsx('font-mono', className)}>
        <div className="text-green-700 bg-green-50 p-2 rounded">
          {trimWhitespace ? original.trim() : original}
        </div>
      </div>
    );
  }

  if (mode === 'side-by-side') {
    return (
      <div className={clsx('space-y-4', className)}>
        {/* Your Answer */}
        <div>
          <div className="text-xs font-medium text-gray-600 mb-1">Your Answer:</div>
          <div className="font-mono text-lg p-3 bg-gray-50 rounded-lg border">
            {diffs.map(([operation, text], index) => {
              // Show inserted (user's additions) and equal parts
              if (operation === DIFF_INSERT) {
                return (
                  <span
                    key={index}
                    className="bg-red-200 text-red-800 px-0.5 rounded"
                    title="Incorrect addition"
                  >
                    {text}
                  </span>
                );
              }
              if (operation === DIFF_EQUAL) {
                return <span key={index}>{text}</span>;
              }
              // Show deleted (missing from user's answer) as strikethrough
              if (operation === DIFF_DELETE) {
                return (
                  <span
                    key={index}
                    className="text-gray-400 line-through"
                    title="Missing"
                  >
                    {text}
                  </span>
                );
              }
              return null;
            })}
          </div>
        </div>

        {/* Correct Answer */}
        <div>
          <div className="text-xs font-medium text-gray-600 mb-1">Correct Answer:</div>
          <div className="font-mono text-lg p-3 bg-green-50 rounded-lg border border-green-200">
            {diffs.map(([operation, text], index) => {
              // Show deleted (what should be there) and equal parts
              if (operation === DIFF_DELETE) {
                return (
                  <span
                    key={index}
                    className="bg-green-200 text-green-800 px-0.5 rounded"
                    title="Should be here"
                  >
                    {text}
                  </span>
                );
              }
              if (operation === DIFF_EQUAL) {
                return <span key={index}>{text}</span>;
              }
              // Don't show inserted parts in correct answer
              return null;
            })}
          </div>
        </div>

        {showLegend && <DiffLegend />}
      </div>
    );
  }

  // Inline mode
  return (
    <div className={clsx('space-y-3', className)}>
      <div className="font-mono text-lg p-3 bg-gray-50 rounded-lg border">
        {diffs.map(([operation, text], index) => {
          if (operation === DIFF_DELETE) {
            // Text that should be there but was deleted (show what's missing)
            return (
              <span
                key={index}
                className="bg-green-200 text-green-800 px-0.5 rounded"
                title="Missing from your answer"
              >
                {text}
              </span>
            );
          }
          if (operation === DIFF_INSERT) {
            // Text that was added incorrectly
            return (
              <span
                key={index}
                className="bg-red-200 text-red-800 px-0.5 rounded line-through"
                title="Should not be here"
              >
                {text}
              </span>
            );
          }
          // Equal text
          return <span key={index}>{text}</span>;
        })}
      </div>

      {showLegend && <DiffLegend compact />}
    </div>
  );
}

// ========== LEGEND COMPONENT ==========

interface DiffLegendProps {
  compact?: boolean;
}

function DiffLegend({ compact = false }: DiffLegendProps) {
  if (compact) {
    return (
      <div className="flex items-center gap-4 text-xs text-gray-600">
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 bg-green-200 rounded"></span>
          <span>Missing</span>
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 bg-red-200 rounded"></span>
          <span>Extra</span>
        </span>
      </div>
    );
  }

  return (
    <div className="p-3 bg-gray-100 rounded-lg">
      <div className="text-xs font-medium text-gray-700 mb-2">Legend:</div>
      <div className="flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <span className="px-2 py-1 bg-green-200 text-green-800 rounded text-xs">
            example
          </span>
          <span className="text-gray-600">Missing from your answer</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-1 bg-red-200 text-red-800 rounded text-xs line-through">
            example
          </span>
          <span className="text-gray-600">Extra in your answer</span>
        </div>
      </div>
    </div>
  );
}

// ========== COMPACT INLINE DIFF ==========

export interface CompactDiffProps {
  original: string;
  modified: string;
  className?: string;
}

/**
 * A compact inline diff for displaying in lists or small spaces.
 */
export function CompactDiff({ original, modified, className }: CompactDiffProps) {
  return (
    <TextDiff
      original={original}
      modified={modified}
      mode="inline"
      showLegend={false}
      className={className}
      trimWhitespace
    />
  );
}

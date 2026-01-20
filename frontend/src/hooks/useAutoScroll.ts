import { useRef, useEffect, useState } from 'react';

/**
 * useAutoScroll Hook
 *
 * Automatically scrolls to the bottom of a scrollable container when new content is added,
 * with smart detection of user scroll position to prevent interrupting manual scrolling.
 *
 * Features:
 * - Auto-scroll to bottom on new messages
 * - Disable auto-scroll when user scrolls up
 * - Re-enable auto-scroll when user scrolls near bottom
 * - Smooth scroll behavior
 *
 * @param dependencies - Array of dependencies that trigger auto-scroll (e.g., messages array)
 * @param threshold - Distance from bottom (px) to re-enable auto-scroll (default: 100)
 */
export function useAutoScroll<T extends HTMLElement = HTMLDivElement>(
  dependencies: any[] = [],
  threshold: number = 100
) {
  const containerRef = useRef<T>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  /**
   * Check if user is near the bottom of the scroll container
   */
  const isNearBottom = (): boolean => {
    if (!containerRef.current) return true;

    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;

    return distanceFromBottom <= threshold;
  };

  /**
   * Scroll to the bottom of the container
   */
  const scrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
    messagesEndRef.current?.scrollIntoView({ behavior, block: 'end' });
  };

  /**
   * Handle scroll events
   */
  const handleScroll = () => {
    const nearBottom = isNearBottom();

    // Re-enable auto-scroll if user scrolls near bottom
    if (!autoScroll && nearBottom) {
      setAutoScroll(true);
    }
    // Disable auto-scroll if user scrolls up
    else if (autoScroll && !nearBottom) {
      setAutoScroll(false);
    }
  };

  /**
   * Auto-scroll when dependencies change (new messages)
   */
  useEffect(() => {
    if (autoScroll && dependencies.length > 0) {
      // Use instant scroll for first message, smooth for subsequent
      const behavior = dependencies.length === 1 ? 'auto' : 'smooth';
      scrollToBottom(behavior as ScrollBehavior);
    }
  }, dependencies);

  /**
   * Always scroll to bottom on initial mount
   */
  useEffect(() => {
    scrollToBottom('auto');
  }, []);

  return {
    /**
     * Ref to attach to the scrollable container
     */
    containerRef,

    /**
     * Ref to attach to an element at the end of the scrollable content
     * (this element will be scrolled into view)
     */
    messagesEndRef,

    /**
     * Scroll event handler to attach to the container
     */
    handleScroll,

    /**
     * Current auto-scroll state
     */
    autoScroll,

    /**
     * Manually scroll to bottom
     */
    scrollToBottom,

    /**
     * Manually set auto-scroll state
     */
    setAutoScroll,
  };
}

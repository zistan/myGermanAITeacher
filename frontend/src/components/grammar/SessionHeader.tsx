import { useEffect, useState } from 'react';
import type { PracticeSessionResponse, SessionProgress } from '../../api/types/grammar.types';
import { Card, Badge, Button, ProgressBar } from '../common';

interface SessionHeaderProps {
  sessionInfo: PracticeSessionResponse;
  progress: SessionProgress;
  currentStreak: number;
  onEndSession: () => void;
}

export function SessionHeader({
  sessionInfo,
  progress,
  currentStreak,
  onEndSession,
}: SessionHeaderProps) {
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progressPercentage =
    (progress.exercises_completed / sessionInfo.total_exercises) * 100;

  return (
    <Card>
      <div className="space-y-4">
        {/* Top Row: Progress and Timer */}
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Question {progress.exercises_completed + 1} of {sessionInfo.total_exercises}
              </span>
              <span className="text-sm text-gray-600">{formatTime(elapsedTime)}</span>
            </div>
            <ProgressBar
              value={progressPercentage}
              color="primary"
              showLabel={false}
              size="md"
            />
          </div>

          <Button
            onClick={onEndSession}
            variant="secondary"
            size="sm"
            className="ml-4"
            data-testid="end-session-button"
          >
            End Session
          </Button>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-4 gap-4">
          {/* Accuracy */}
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">
              {progress.accuracy_percentage.toFixed(0)}%
            </div>
            <div className="text-xs text-gray-600">Accuracy</div>
          </div>

          {/* Correct Answers */}
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {progress.exercises_correct}
            </div>
            <div className="text-xs text-gray-600">Correct</div>
          </div>

          {/* Points */}
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{progress.total_points}</div>
            <div className="text-xs text-gray-600">Points</div>
          </div>

          {/* Streak */}
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {currentStreak > 0 ? `🔥 ${currentStreak}` : currentStreak}
            </div>
            <div className="text-xs text-gray-600">Streak</div>
          </div>
        </div>

        {/* Topics Included */}
        {sessionInfo.topics_included.length > 0 && (
          <div className="pt-3 border-t border-gray-200">
            <div className="text-xs text-gray-600 mb-2">Topics in this session:</div>
            <div className="flex flex-wrap gap-2">
              {sessionInfo.topics_included.map((topic, index) => (
                <Badge key={index} variant="gray" size="sm">
                  {topic}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}

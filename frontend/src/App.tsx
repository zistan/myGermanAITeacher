import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from './components/common';
import { Layout } from './components/layout';
import { useAuthStore } from './store/authStore';
import { useNotificationStore } from './store/notificationStore';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { GrammarTopicsPage } from './pages/grammar/GrammarTopicsPage';
import { PracticeSessionPage } from './pages/grammar/PracticeSessionPage';
import { ProgressPage as GrammarProgressPage } from './pages/grammar/ProgressPage';
import { ReviewQueuePage } from './pages/grammar/ReviewQueuePage';
import { ResultsPage } from './pages/grammar/ResultsPage';
import {
  VocabularyBrowserPage,
  FlashcardSessionPage,
  VocabularyListsPage,
  VocabularyListDetailPage,
  VocabularyQuizPage,
  VocabularyProgressPage,
} from './pages/vocabulary';
import {
  ContextsPage,
  PracticePage,
  HistoryPage,
  SessionDetailPage,
} from './pages/conversation';
import {
  ProgressOverviewPage,
  AchievementsPage,
  HeatmapPage,
  LeaderboardPage,
  ErrorAnalysisPage,
} from './pages/analytics';

function App() {
  const initialize = useAuthStore((state) => state.initialize);
  const toasts = useNotificationStore((state) => state.toasts);

  useEffect(() => {
    // Initialize auth state from localStorage
    initialize();
  }, [initialize]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <DashboardPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Grammar routes */}
          <Route
            path="/grammar"
            element={
              <ProtectedRoute>
                <Layout>
                  <GrammarTopicsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/grammar/practice"
            element={
              <ProtectedRoute>
                <Layout>
                  <PracticeSessionPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/grammar/progress"
            element={
              <ProtectedRoute>
                <Layout>
                  <GrammarProgressPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/grammar/review-queue"
            element={
              <ProtectedRoute>
                <Layout>
                  <ReviewQueuePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/grammar/results"
            element={
              <ProtectedRoute>
                <Layout>
                  <ResultsPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Vocabulary routes */}
          <Route
            path="/vocabulary"
            element={
              <ProtectedRoute>
                <Layout>
                  <VocabularyBrowserPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/vocabulary/flashcards"
            element={
              <ProtectedRoute>
                <Layout>
                  <FlashcardSessionPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/vocabulary/lists"
            element={
              <ProtectedRoute>
                <Layout>
                  <VocabularyListsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/vocabulary/lists/:id"
            element={
              <ProtectedRoute>
                <Layout>
                  <VocabularyListDetailPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/vocabulary/quiz"
            element={
              <ProtectedRoute>
                <Layout>
                  <VocabularyQuizPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/vocabulary/progress"
            element={
              <ProtectedRoute>
                <Layout>
                  <VocabularyProgressPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Conversation routes */}
          <Route
            path="/conversation"
            element={
              <ProtectedRoute>
                <Layout>
                  <ContextsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/conversation/practice"
            element={
              <ProtectedRoute>
                <Layout>
                  <PracticePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/conversation/history"
            element={
              <ProtectedRoute>
                <Layout>
                  <HistoryPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/conversation/session/:id"
            element={
              <ProtectedRoute>
                <Layout>
                  <SessionDetailPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Analytics routes */}
          <Route
            path="/analytics/progress"
            element={
              <ProtectedRoute>
                <Layout>
                  <ProgressOverviewPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/analytics/achievements"
            element={
              <ProtectedRoute>
                <Layout>
                  <AchievementsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/analytics/heatmaps"
            element={
              <ProtectedRoute>
                <Layout>
                  <HeatmapPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/analytics/leaderboards"
            element={
              <ProtectedRoute>
                <Layout>
                  <LeaderboardPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/analytics/errors"
            element={
              <ProtectedRoute>
                <Layout>
                  <ErrorAnalysisPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Backward compatibility redirects */}
          <Route path="/progress" element={<Navigate to="/analytics/progress" replace />} />
          <Route path="/achievements" element={<Navigate to="/analytics/achievements" replace />} />

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* 404 */}
          <Route
            path="*"
            element={
              <div className="flex items-center justify-center h-screen">
                <h1 className="text-2xl font-bold text-gray-900">404 - Page Not Found</h1>
              </div>
            }
          />
        </Routes>

        {/* Toast notifications */}
        <ToastContainer toasts={toasts} />
      </div>
    </BrowserRouter>
  );
}

export default App;

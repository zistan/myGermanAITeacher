import { useAuthStore } from '../store/authStore';
import { Card } from '../components/common';

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.username}!
          </h1>
          <p className="mt-2 text-gray-600">Proficiency Level: {user?.proficiency_level}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Quick Actions</h2>
            <p className="text-gray-600">Coming soon - Start a conversation, practice grammar, or review vocabulary</p>
          </Card>

          <Card>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Your Progress</h2>
            <p className="text-gray-600">Coming soon - View your learning progress and achievements</p>
          </Card>

          <Card>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Due Items</h2>
            <p className="text-gray-600">Coming soon - Grammar topics and vocabulary words to review</p>
          </Card>
        </div>

        <div className="mt-8">
          <Card>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <p className="text-gray-600">No activity yet. Start learning to see your progress here!</p>
          </Card>
        </div>
      </div>
    </div>
  );
}

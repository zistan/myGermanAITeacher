import { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import clsx from 'clsx';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation();
  const [expandedItems, setExpandedItems] = useState<string[]>(['/vocabulary', '/grammar', '/conversation', '/analytics']);
  const navItems = [
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
          />
        </svg>
      ),
    },
    {
      name: 'Conversation',
      path: '/conversation',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
      ),
      subItems: [
        { name: 'Start Conversation', path: '/conversation' },
        { name: 'Practice', path: '/conversation/practice' },
        { name: 'History', path: '/conversation/history' },
      ],
    },
    {
      name: 'Grammar',
      path: '/grammar',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
      ),
      subItems: [
        { name: 'Browse Topics', path: '/grammar' },
        { name: 'Practice', path: '/grammar/practice' },
        { name: 'Progress', path: '/grammar/progress' },
        { name: 'Review Queue', path: '/grammar/review-queue' },
      ],
    },
    {
      name: 'Vocabulary',
      path: '/vocabulary',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
          />
        </svg>
      ),
      subItems: [
        { name: 'Browse Words', path: '/vocabulary' },
        { name: 'Flashcards', path: '/vocabulary/flashcards' },
        { name: 'My Lists', path: '/vocabulary/lists' },
        { name: 'Quiz', path: '/vocabulary/quiz' },
        { name: 'Progress', path: '/vocabulary/progress' },
      ],
    },
    {
      name: 'Analytics',
      path: '/analytics',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
      ),
      subItems: [
        { name: 'Overview', path: '/analytics/progress' },
        { name: 'Achievements', path: '/analytics/achievements' },
        { name: 'Heatmaps', path: '/analytics/heatmaps' },
        { name: 'Leaderboards', path: '/analytics/leaderboards' },
        { name: 'Error Analysis', path: '/analytics/errors' },
      ],
    },
    {
      name: 'Learning Path',
      path: '/learning-path',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
          />
        </svg>
      ),
    },
  ];

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed top-0 left-0 z-50 h-full w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:z-auto',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo/Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-br from-german-black via-german-red to-primary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">DE</span>
              </div>
              <span className="ml-3 text-lg font-bold text-gray-900">German Learning</span>
            </div>
            {/* Mobile close button */}
            <button
              onClick={onClose}
              className="lg:hidden text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 overflow-y-auto">
            <ul className="space-y-1">
              {navItems.map((item) => {
                const hasSubItems = item.subItems && item.subItems.length > 0;
                const isExpanded = expandedItems.includes(item.path);
                const isActive = location.pathname === item.path ||
                  (hasSubItems && item.subItems!.some(sub => location.pathname === sub.path));

                const toggleExpand = () => {
                  if (hasSubItems) {
                    setExpandedItems(prev =>
                      prev.includes(item.path)
                        ? prev.filter(p => p !== item.path)
                        : [...prev, item.path]
                    );
                  }
                };

                return (
                  <li key={item.path}>
                    {hasSubItems ? (
                      <>
                        <button
                          onClick={toggleExpand}
                          className={clsx(
                            'w-full flex items-center justify-between px-4 py-3 rounded-lg transition-colors',
                            isActive
                              ? 'bg-primary-50 text-primary-700 font-medium'
                              : 'text-gray-700 hover:bg-gray-100'
                          )}
                        >
                          <span className="flex items-center">
                            <span className="flex-shrink-0">{item.icon}</span>
                            <span className="ml-3">{item.name}</span>
                          </span>
                          <svg
                            className={clsx(
                              'w-4 h-4 transition-transform',
                              isExpanded && 'transform rotate-180'
                            )}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </button>
                        {isExpanded && (
                          <ul className="mt-1 ml-6 space-y-1">
                            {item.subItems!.map((subItem) => (
                              <li key={subItem.path}>
                                <NavLink
                                  to={subItem.path}
                                  onClick={() => onClose?.()}
                                  className={({ isActive }) =>
                                    clsx(
                                      'block px-4 py-2 text-sm rounded-lg transition-colors',
                                      isActive
                                        ? 'bg-primary-100 text-primary-700 font-medium'
                                        : 'text-gray-600 hover:bg-gray-100'
                                    )
                                  }
                                >
                                  {subItem.name}
                                </NavLink>
                              </li>
                            ))}
                          </ul>
                        )}
                      </>
                    ) : (
                      <NavLink
                        to={item.path}
                        onClick={() => onClose?.()}
                        className={({ isActive }) =>
                          clsx(
                            'flex items-center px-4 py-3 rounded-lg transition-colors',
                            isActive
                              ? 'bg-primary-50 text-primary-700 font-medium'
                              : 'text-gray-700 hover:bg-gray-100'
                          )
                        }
                      >
                        <span className="flex-shrink-0">{item.icon}</span>
                        <span className="ml-3">{item.name}</span>
                      </NavLink>
                    )}
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-200">
            <div className="flex items-center text-sm text-gray-600">
              <svg
                className="w-4 h-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>v1.0.0 - Phase 7</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

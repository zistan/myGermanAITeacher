import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from './components/common';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          {/* Temporary placeholder route */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<div className="flex items-center justify-center h-screen"><h1 className="text-2xl font-bold text-gray-900">Login Page - Coming Soon</h1></div>} />
          <Route path="*" element={<div className="flex items-center justify-center h-screen"><h1 className="text-2xl font-bold text-gray-900">404 - Page Not Found</h1></div>} />
        </Routes>

        {/* Toast notifications container */}
        <ToastContainer toasts={[]} />
      </div>
    </BrowserRouter>
  );
}

export default App;

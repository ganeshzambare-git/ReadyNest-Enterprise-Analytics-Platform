import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import PipelineCards from './components/PipelineCards';
import DashboardLayout from './layouts/DashboardLayout';
import Login from './pages/Login';
import ExecutiveHome from './pages/ExecutiveHome';
import DataLoading from './pages/DataLoading';

import type { ReactNode } from 'react';

// The original landing page
const LandingPage = () => (
  <div className="app-container">
    <Navbar />
    <main>
      <Hero />
      <PipelineCards />
    </main>
  </div>
);

// Protected route wrapper
const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          
          <Route path="/dashboard" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
            <Route index element={<ExecutiveHome />} />
            <Route path="data-loading" element={<DataLoading />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;


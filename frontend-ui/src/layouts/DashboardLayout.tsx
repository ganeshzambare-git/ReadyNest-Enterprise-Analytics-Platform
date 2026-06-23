import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Home, Database, BarChart2, LogOut } from 'lucide-react';
import './DashboardLayout.css';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <span className="logo-icon text-cyan glow-cyan-text">⬡</span>
          <span className="font-orbitron text-white font-bold">ReadyNest</span>
        </div>
        
        <nav className="sidebar-nav">
          <Link to="/dashboard" className="nav-item">
            <Home size={18} /> Executive Home
          </Link>
          <Link to="/dashboard/data-loading" className="nav-item">
            <Database size={18} /> Data Loading
          </Link>
          {/* Add more links for Phase 2 here */}
          <Link to="#" className="nav-item disabled">
            <BarChart2 size={18} /> Analytics (Coming Soon)
          </Link>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-name">{user?.name || 'Guest'}</div>
            <div className="user-role">{user?.role || 'User'}</div>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={16} /> Logout
          </button>
        </div>
      </aside>

      <main className="dashboard-content">
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardLayout;

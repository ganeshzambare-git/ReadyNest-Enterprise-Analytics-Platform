import './Navbar.css';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <span className="logo-icon text-cyan glow-cyan-text">⬡</span>
        <span className="logo-text font-orbitron">DarkStore <span className="logo-sub text-cyan">Data Platform</span></span>
      </div>
      
      <div className="navbar-links">
        <a href="#platform" className="nav-link">Platform</a>
        <a href="#solutions" className="nav-link">Solutions</a>
        <a href="#resources" className="nav-link">Resources</a>
        <a href="#pricing" className="nav-link">Pricing</a>
        <a href="#docs" className="nav-link">Docs</a>
        <a href="#about" className="nav-link">About</a>
      </div>

      <div className="navbar-actions">
        <button className="btn-get-started bg-green glow-green-box">Get Started</button>
      </div>
    </nav>
  );
};

export default Navbar;

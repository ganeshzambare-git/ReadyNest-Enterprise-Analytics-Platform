import { Database, CloudUpload, Server, Network, HardDrive } from 'lucide-react';
import './Hero.css';

const Hero: React.FC = () => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h3 className="hero-eyebrow text-green font-orbitron">DARK STORE DATA ARCHITECTURE PIPELINE</h3>
        <h1 className="hero-title font-orbitron">
          From Raw Data to <br />
          <span className="text-cyan glow-cyan-text">Strategic Decisions</span>
        </h1>
        <p className="hero-subtitle">
          A 4-Stage Blueprint for Data Excellence and Business Impact
        </p>
        
        <div className="hero-features">
          <span className="feature-badge text-green glow-green-text"><Database size={16}/> SECURE</span>
          <span className="feature-badge text-green glow-green-text"><Network size={16}/> SCALABLE</span>
          <span className="feature-badge text-green glow-green-text"><Server size={16}/> RELIABLE</span>
        </div>

        <p className="hero-desc">Built for modern retail. Engineered for growth.</p>

        <div className="hero-actions">
          <button className="btn-primary bg-green glow-green-box">Explore Platform</button>
          <button className="btn-secondary">View Demo</button>
        </div>
      </div>

      <div className="hero-graphic">
        <div className="isometric-container">
          <div className="matrix-grid"></div>
          
          <div className="cpu-core glow-cyan-box">
            <div className="cpu-inner glow-cyan-box"></div>
          </div>
          
          <div className="floating-icons">
            <div className="float-icon icon-1 glow-cyan-box glass-panel"><CloudUpload color="#00EEFF" size={24} /></div>
            <div className="float-icon icon-2 glow-cyan-box glass-panel"><Server color="#00EEFF" size={24} /></div>
            <div className="float-icon icon-3 glow-cyan-box glass-panel"><Database color="#00EEFF" size={24} /></div>
            <div className="float-icon icon-4 glow-cyan-box glass-panel"><Network color="#00EEFF" size={24} /></div>
            <div className="float-icon icon-5 glow-cyan-box glass-panel"><HardDrive color="#00EEFF" size={24} /></div>
          </div>
          
          <svg className="connection-lines" viewBox="0 0 400 400">
             <path d="M200 200 L80 80 M200 200 L320 80 M200 200 L80 320 M200 200 L320 320 M200 200 L200 40" stroke="#00EEFF" strokeWidth="2" fill="none" opacity="0.4" strokeDasharray="5,5"/>
          </svg>
        </div>
      </div>
    </section>
  );
};

export default Hero;

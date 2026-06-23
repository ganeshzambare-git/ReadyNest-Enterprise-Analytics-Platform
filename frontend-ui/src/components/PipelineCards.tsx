import { CloudLightning, LayoutDashboard, Network, BarChart2, ArrowRight } from 'lucide-react';
import './PipelineCards.css';

interface CardProps {
  number: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  colorClass: 'cyan' | 'green';
}

const PipelineCard: React.FC<CardProps> = ({ number, title, description, icon, colorClass }) => {
  return (
    <div className={`pipeline-card glass-panel ${colorClass}`}>
      <div className="card-header">
        <span className={`card-number font-orbitron glow-${colorClass}-text text-${colorClass}`}>{number}</span>
        <div className={`card-icon text-${colorClass} glow-${colorClass}-text isometric-icon`}>
          {icon}
        </div>
      </div>
      <div className="card-body">
        <h4 className="card-title font-orbitron">{title}</h4>
        <p className="card-desc">{description}</p>
      </div>
      <div className="card-footer">
        <a href="#" className={`card-link glow-${colorClass}-text text-${colorClass}`}>Learn more <ArrowRight size={14} className="link-arrow"/></a>
      </div>
    </div>
  );
};

const PipelineCards: React.FC = () => {
  const cards: CardProps[] = [
    {
      number: '01',
      title: 'DATA INGESTION',
      description: 'Collect. Connect. Consolidate.',
      icon: <CloudLightning size={32} />,
      colorClass: 'cyan'
    },
    {
      number: '02',
      title: 'QUALITY DATA CLEANING',
      description: 'Clean. Validate. Enrich.',
      icon: <LayoutDashboard size={32} />,
      colorClass: 'green'
    },
    {
      number: '03',
      title: 'MACHINE LEARNING LAYER',
      description: 'Predict. Learn. Optimize.',
      icon: <Network size={32} />,
      colorClass: 'cyan'
    },
    {
      number: '04',
      title: 'EXECUTIVE DASHBOARD REPORTING',
      description: 'Visualize. Decide. Drive Impact.',
      icon: <BarChart2 size={32} />,
      colorClass: 'green'
    }
  ];

  return (
    <section className="pipeline-section">
      <div className="pipeline-grid">
        {cards.map((card, index) => (
          <PipelineCard key={index} {...card} />
        ))}
      </div>
    </section>
  );
};

export default PipelineCards;

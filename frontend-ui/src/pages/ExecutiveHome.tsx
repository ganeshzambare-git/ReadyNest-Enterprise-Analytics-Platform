import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import Plot from 'react-plotly.js';
import { AlertCircle, TrendingUp } from 'lucide-react';
import './Pages.css';

const ExecutiveHome = () => {
  const [kpis, setKpis] = useState<any>(null);
  const [insights, setInsights] = useState<any[]>([]);

  useEffect(() => {
    const fetchExecutiveData = async () => {
      try {
        const [kpiRes, insightsRes] = await Promise.all([
          apiClient.get('/executive/kpis'),
          apiClient.get('/executive/insights')
        ]);
        setKpis(kpiRes.data);
        setInsights(insightsRes.data.insights);
      } catch (error) {
        console.error("Failed to fetch executive data", error);
      }
    };
    fetchExecutiveData();
  }, []);

  return (
    <div className="page-container">
      <h1 className="font-orbitron text-3xl mb-8 border-b border-gray-800 pb-4">Executive Command Center</h1>

      {kpis && (
        <div className="kpi-grid mb-8">
          <div className="kpi-card">
            <div className="kpi-label">Total Revenue</div>
            <div className="kpi-value text-cyan glow-cyan-text">{kpis.revenue.formatted}</div>
            <div className="kpi-trend text-green">{kpis.revenue.trend}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Avg Order Value</div>
            <div className="kpi-value text-cyan glow-cyan-text">{kpis.aov.formatted}</div>
            <div className="kpi-trend text-green">{kpis.aov.trend}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Gross Margin</div>
            <div className="kpi-value text-cyan glow-cyan-text">{kpis.margin.formatted}</div>
            <div className="kpi-trend text-green">{kpis.margin.trend}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">On-Time Delivery</div>
            <div className="kpi-value text-cyan glow-cyan-text">{kpis.delivery.formatted}</div>
            <div className="kpi-trend text-green">{kpis.delivery.trend}</div>
          </div>
        </div>
      )}

      <div className="grid-2-col mb-8">
        <div className="panel chart-panel">
          <h3 className="panel-title">Monthly Revenue Trend</h3>
          <Plot
            data={[
              {
                x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y: [2.5, 3.8, 5.2, 4.8, 6.1, 8.4],
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: '#00EEFF' },
                line: { shape: 'spline', smoothing: 1.3 }
              }
            ]}
            layout={{ 
              paper_bgcolor: 'transparent',
              plot_bgcolor: 'transparent',
              font: { color: '#94A3B8' },
              margin: { t: 20, r: 20, b: 40, l: 40 },
              xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
              yaxis: { gridcolor: 'rgba(255,255,255,0.05)' }
            }}
            useResizeHandler={true}
            style={{ width: "100%", height: "300px" }}
          />
        </div>

        <div className="panel">
          <h3 className="panel-title mb-4">AI Business Insights</h3>
          <div className="insights-list">
            {insights.map((insight, idx) => (
              <div key={idx} className={`insight-card ${insight.type}`}>
                <div className="insight-icon">
                  {insight.type === 'negative' ? <AlertCircle size={20} /> : <TrendingUp size={20} />}
                </div>
                <div>
                  <h4 className="font-bold text-white">{insight.title}</h4>
                  <p className="text-sm text-gray-400 mt-1">{insight.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExecutiveHome;

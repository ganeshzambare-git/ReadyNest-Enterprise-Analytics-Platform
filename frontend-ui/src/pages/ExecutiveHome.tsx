import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import Plot from 'react-plotly.js';
import { AlertCircle, TrendingUp } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card';
import KpiCard from '../components/KpiCard';
import { Button } from '../components/Button';

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
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex items-center justify-between pb-6 border-b border-border">
        <h1 className="text-4xl font-bold font-orbitron">Executive Command Center</h1>
        <Button>
          <TrendingUp className="mr-2 h-4 w-4" />
          Generate Report
        </Button>
      </div>

      {kpis && (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <KpiCard 
            title="Total Revenue" 
            value={kpis.revenue.formatted} 
            trend="up" 
            changePercent={12.5} 
            comparisonPeriod="Last Quarter" 
          />
          <KpiCard 
            title="Avg Order Value" 
            value={kpis.aov.formatted} 
            trend="up" 
            changePercent={5.2} 
            comparisonPeriod="Last Month" 
          />
          <KpiCard 
            title="Gross Margin" 
            value={kpis.margin.formatted} 
            trend="neutral" 
            changePercent={0.0} 
            comparisonPeriod="Last Year" 
          />
          <KpiCard 
            title="On-Time Delivery" 
            value={kpis.delivery.formatted} 
            trend="down" 
            changePercent={-2.1} 
            comparisonPeriod="Last Month" 
          />
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Monthly Revenue Trend</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <Plot
              data={[
                {
                  x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                  y: [2.5, 3.8, 5.2, 4.8, 6.1, 8.4],
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: { color: 'hsl(181, 100%, 50%)' }, // cyan
                  line: { shape: 'spline', smoothing: 1.3, color: 'hsl(181, 100%, 50%)' }
                }
              ]}
              layout={{ 
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                font: { color: 'hsl(215, 20%, 65%)' }, // muted-foreground
                margin: { t: 10, r: 10, b: 30, l: 40 },
                xaxis: { gridcolor: 'hsl(215, 28%, 17%)' },
                yaxis: { gridcolor: 'hsl(215, 28%, 17%)' }
              }}
              useResizeHandler={true}
              style={{ width: "100%", height: "350px" }}
            />
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>AI Business Insights</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {insights.map((insight, idx) => (
              <div key={idx} className="flex items-start gap-4 p-4 rounded-lg bg-muted/50">
                <div className={insight.type === 'negative' ? 'text-destructive' : 'text-accent'}>
                  {insight.type === 'negative' ? <AlertCircle className="h-5 w-5" /> : <TrendingUp className="h-5 w-5" />}
                </div>
                <div className="space-y-1">
                  <h4 className="text-sm font-medium leading-none">{insight.title}</h4>
                  <p className="text-sm text-muted-foreground">{insight.description}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ExecutiveHome;

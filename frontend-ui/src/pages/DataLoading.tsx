import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { Upload, Database } from 'lucide-react';
import './Pages.css';

const DataLoading = () => {
  const [status, setStatus] = useState<any>(null);
  const [sample, setSample] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statusRes, sampleRes] = await Promise.all([
          apiClient.get('/data/status'),
          apiClient.get('/data/sample')
        ]);
        setStatus(statusRes.data);
        setSample(sampleRes.data.data);
      } catch (error) {
        console.error("Failed to fetch data status", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="page-container">
      <h1 className="font-orbitron text-3xl mb-8 border-b border-gray-800 pb-4">Data Loading Module</h1>
      
      <div className="grid-2-col">
        <div className="panel">
          <h3 className="panel-title"><Upload size={18}/> Upload New Dataset</h3>
          <div className="upload-zone">
            <p className="text-gray-400 mb-4">Drag and drop your CSV or Excel file here</p>
            <button className="btn-secondary">Browse Files</button>
          </div>
        </div>

        <div className="panel">
          <h3 className="panel-title"><Database size={18}/> Current Dataset Status</h3>
          {loading ? <p>Loading status...</p> : (
            status ? (
              <div className="status-grid">
                <div className="status-item">
                  <label>Filename</label>
                  <span>{status.filename}</span>
                </div>
                <div className="status-item">
                  <label>Total Rows</label>
                  <span>{status.rows.toLocaleString()}</span>
                </div>
                <div className="status-item">
                  <label>Total Columns</label>
                  <span>{status.columns}</span>
                </div>
                <div className="status-item">
                  <label>Last Updated</label>
                  <span>{new Date(status.last_updated).toLocaleString()}</span>
                </div>
              </div>
            ) : <p>No active dataset loaded.</p>
          )}
        </div>
      </div>

      <div className="panel mt-8">
        <h3 className="panel-title">Data Preview (Sample)</h3>
        {sample.length > 0 && (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  {Object.keys(sample[0]).map(k => <th key={k}>{k}</th>)}
                </tr>
              </thead>
              <tbody>
                {sample.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val: any, j) => <td key={j}>{val}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataLoading;

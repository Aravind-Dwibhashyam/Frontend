import React, { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import api from '../services/api';

export default function IntegrationLog() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const res = await api.get('/integrations');
      setLogs(res.data);
    } catch(err) { }
  };

  const cols = [
    { header: 'Timestamp', accessor: 'timestamp', render: (row) => new Date(row.timestamp).toLocaleString() },
    { header: 'Target', accessor: 'target_module' },
    { header: 'Payload Summary', accessor: 'payload_summary' },
    { header: 'HTTP', accessor: 'http_status' },
    { 
      header: 'Result', 
      render: (row) => (
        <span className={`px-2 py-1 rounded text-xs font-bold ${
          row.result === 'success' ? 'bg-teal-100 text-teal-700' :
          row.result === 'failed' ? 'bg-red-100 text-red-700' :
          'bg-amber-100 text-amber-700'
        }`}>
          {row.result.toUpperCase()}
        </span>
      )
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Integration Logs</h1>
        <p className="mt-1 text-sm text-slate-500">History of communication with external health modules.</p>
      </div>
      <DataTable columns={cols} data={logs} />
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DataTable from '../components/DataTable';
import api from '../services/api';
import { showToast } from '../components/ToastNotification';
import { DownloadCloud, Plus } from 'lucide-react';

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [module1Id, setModule1Id] = useState('');
  const navigate = useNavigate();

  const loadPatients = async () => {
    try {
      const res = await api.get('/patients');
      setPatients(res.data);
    } catch (err) {
      showToast('Failed to load patients', 'error');
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const handlePullModule1 = async () => {
    if (!module1Id) return;
    setIsLoading(true);
    try {
      // Mocking fetch flow since we don't really have the module1 running
      // and it will likely return a timeout or 500 error since network is not mocked there
      // We will rely on real fetch logic, but if fails gracefully, we show error toast.
      const res = await api.get(`/module1/patient/${module1Id}`);
      showToast(res.data.message || 'Patient successfully imported', 'success');
      setModule1Id('');
      loadPatients();
    } catch (err) {
      showToast('Failed to fetch from Module-1', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const columns = [
    { header: 'Patient ID', accessor: 'patient_id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Age', accessor: 'age' },
    { header: 'Gender', accessor: 'gender' },
    { header: 'DOB', accessor: 'dob' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Patient Registry</h1>
          <p className="mt-1 text-sm text-slate-500">Manage chronic disease patients imported from Module 1.</p>
        </div>
        
        <div className="flex items-center space-x-3 bg-white p-2 rounded-lg border border-slate-200 shadow-sm">
          <input 
            type="text" 
            placeholder="M1 Patient ID" 
            value={module1Id}
            onChange={(e) => setModule1Id(e.target.value)}
            className="w-32 px-3 py-1.5 text-sm border border-slate-200 rounded outline-none focus:border-teal-500"
          />
          <button 
            onClick={handlePullModule1}
            disabled={isLoading}
            className="flex items-center px-3 py-1.5 bg-teal-600 text-white text-sm font-medium rounded hover:bg-teal-700 transition"
          >
            <DownloadCloud size={16} className="mr-2" />
            Pull from M1
          </button>
        </div>
      </div>

      <DataTable 
        columns={columns} 
        data={patients} 
        onRowClick={(row) => navigate(`/patients/${row.patient_id}`)} 
      />
    </div>
  );
}

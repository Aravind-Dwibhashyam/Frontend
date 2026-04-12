import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DataTable from '../components/DataTable';
import api from '../services/api';
import { showToast } from '../components/ToastNotification';

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const loadPatients = async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/patients');
      // Format data for table display
      const formatted = res.data.map(p => ({
        ...p,
        name: `${p.first_name} ${p.last_name}`,
        dob: p.date_of_birth ? new Date(p.date_of_birth).toLocaleDateString() : 'N/A'
      }));
      setPatients(formatted);
    } catch (err) {
      showToast('Failed to load patients from Demographics API', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

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
          <p className="mt-1 text-sm text-slate-500">Live feed from Patient Demographics Module.</p>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-10 text-slate-500">Loading patients from Module 1...</div>
      ) : (
        <DataTable 
          columns={columns} 
          data={patients} 
          onRowClick={(row) => navigate(`/patients/${row.patient_id}`)} 
        />
      )}
    </div>
  );
}

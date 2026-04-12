import React, { useState, useEffect } from 'react';
import DataTable from '../components/DataTable';
import api from '../services/api';
import { showToast } from '../components/ToastNotification';

export default function Diagnoses() {
  const [diseases, setDiseases] = useState([]);
  const [form, setForm] = useState({ disease_id: '', name: '', type: '', description: '' });

  useEffect(() => {
    loadDiseases();
  }, []);

  const loadDiseases = async () => {
    try {
      const res = await api.get('/diseases');
      setDiseases(res.data);
    } catch (err) { }
  };

  const handleInputChange = (e) => setForm({...form, [e.target.name]: e.target.value});

  const submitForm = async (e) => {
    e.preventDefault();
    try {
      await api.post('/diseases', form);
      showToast('Chronic disease catalog added', 'success');
      loadDiseases();
      setForm({ disease_id: '', name: '', type: '', description: '' });
    } catch (err) {
      showToast('Error saving disease', 'error');
    }
  };

  const cols = [
    { header: 'ID', accessor: 'disease_id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Type', accessor: 'type' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Chronic Disease Catalog</h1>
        <p className="mt-1 text-sm text-slate-500">Manage the global list of chronic diseases and linked diagnoses.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-lg font-semibold mb-4">Add Disease Type</h2>
        <form onSubmit={submitForm} className="flex gap-4 mb-4 flex-wrap">
          <input name="disease_id" value={form.disease_id} placeholder="ID" onChange={handleInputChange} className="border p-2 rounded" required />
          <input name="name" value={form.name} placeholder="Name" onChange={handleInputChange} className="border p-2 rounded" required />
          <input name="type" value={form.type} placeholder="Type" onChange={handleInputChange} className="border p-2 rounded" required />
          <input name="description" value={form.description} placeholder="Description" onChange={handleInputChange} className="border p-2 rounded flex-1" />
          <button className="px-4 py-2 bg-teal-600 text-white rounded">Add</button>
        </form>
      </div>

      <DataTable columns={cols} data={diseases} />
    </div>
  );
}

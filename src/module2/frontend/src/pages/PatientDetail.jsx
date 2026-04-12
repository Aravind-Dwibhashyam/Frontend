import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import TabPanel from '../components/TabPanel';
import DataTable from '../components/DataTable';
import api from '../services/api';
import { showToast } from '../components/ToastNotification';

export default function PatientDetail() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const [activeTab, setActiveTab] = useState('diagnoses');
  const [data, setData] = useState({});
  const [form, setForm] = useState({});

  useEffect(() => {
    loadPatientData();
  }, [id]);

  const loadPatientData = async () => {
    try {
      const res = await api.get(`/patients/${id}`);
      setPatient(res.data.patient);
      
      const visitsRes = await api.get(`/patients/${id}/visits`);
      
      setData({ 
        diagnoses: res.data.diagnoses || [], 
        metrics: res.data.metrics || [],
        episodes: res.data.episodes || [],
        risks: res.data.risks || [],
        plans: res.data.plans || [],
        adherence: res.data.adherence || [],
        visits: visitsRes.data || []
      });
    } catch (err) {
      showToast('Error loading patient data', 'error');
    }
  };

  const tabs = [
    { id: 'diagnoses', label: 'Diagnosis' },
    { id: 'metrics', label: 'Clinical Metrics' },
    { id: 'episodes', label: 'Disease Episodes' },
    { id: 'risks', label: 'Risk Assessment' },
    { id: 'plans', label: 'Treatment Plan' },
    { id: 'adherence', label: 'Medication Adherence' },
    { id: 'visits', label: 'Visits (M1)' },
  ];

  const handleInputChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const submitForm = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...form };
      Object.keys(payload).forEach(key => {
        if (payload[key] === '') delete payload[key];
      });

      if (activeTab === 'plans') {
        await api.post('/plans/', { ...payload, patient_id: id, doctor_id: "doc123" });
        showToast('Treatment Plan saved. Modules 19 & 33 notified via Background Tasks', 'success');
      } else if (activeTab === 'metrics') {
        await api.post('/metrics/', { ...payload, value: parseFloat(payload.value), doctor_id: "doc123" });
        showToast('Clinical Metric saved. Module 25 notified via Background Tasks', 'success');
      } else if (activeTab === 'diagnoses') {
        await api.post('/diagnoses/', { ...payload, patient_id: id, doctor_id: "doc123" });
        showToast('Diagnosis saved', 'success');
      } else if (activeTab === 'episodes') {
        await api.post('/episodes/', { ...payload, doctor_id: "doc123", triggers: payload.triggers ? payload.triggers.split(',') : [] });
        showToast('Disease Episode saved', 'success');
      } else if (activeTab === 'risks') {
        await api.post('/risks/', { ...payload, patient_id: id, risk_score: parseFloat(payload.risk_score) });
        showToast('Risk Assessment saved', 'success');
      } else if (activeTab === 'adherence') {
        await api.post('/adherence/', payload);
        showToast('Medication Adherence saved', 'success');
      }
      setForm({});
      e.target.reset();
      loadPatientData(); 
    } catch (err) {
      showToast('Error saving data', 'error');
    }
  };

  const getTabColumns = () => {
    switch(activeTab) {
      case 'diagnoses': return [
        { header: 'Diagnosis ID', accessor: 'diagnosis_id' },
        { header: 'Disease ID', accessor: 'disease_id' },
        { header: 'Date', accessor: 'date_diagnosed' },
        { header: 'Severity', accessor: 'severity_stage' },
        { header: 'Status', accessor: 'current_status' },
      ];
      case 'metrics': return [
        { header: 'Metric ID', accessor: 'metric_id' },
        { header: 'Type', accessor: 'metric_type' },
        { header: 'Value', accessor: 'value' },
        { header: 'Unit', accessor: 'unit' },
        { header: 'Recorded', accessor: 'recorded_at' },
      ];
      case 'episodes': return [
        { header: 'Episode ID', accessor: 'episode_id' },
        { header: 'Diagnosis ID', accessor: 'diagnosis_id' },
        { header: 'Start Date', accessor: 'start_date' },
        { header: 'Severity', accessor: 'severity_levels' },
      ];
      case 'risks': return [
        { header: 'Assessment ID', accessor: 'assessment_id' },
        { header: 'Score', accessor: 'risk_score' },
        { header: 'Category', accessor: 'category' },
      ];
      case 'plans': return [
        { header: 'Plan ID', accessor: 'plan_id' },
        { header: 'Goal', accessor: 'goal' },
        { header: 'Start Date', accessor: 'start_date' },
      ];
      case 'adherence': return [
        { header: 'Adherence ID', accessor: 'adherence_id' },
        { header: 'Date', accessor: 'log_date' },
        { header: 'Status', accessor: 'status' },
      ];
      case 'visits': return [
        { header: 'Visit ID', accessor: 'visit_id' },
        { header: 'Date', accessor: 'visit_date' },
        { header: 'Department', accessor: 'department_id' },
        { header: 'Physician', accessor: 'physician_id' },
        { header: 'Status', accessor: 'status' },
      ];
      default: return [];
    }
  };

  if (!patient) return <div className="p-6 text-slate-500">Loading patient details...</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h1 className="text-2xl font-bold text-slate-800">{patient.first_name} {patient.last_name}</h1>
        <div className="mt-2 flex space-x-6 text-sm text-slate-500">
          <p>ID: <span className="font-medium text-slate-700">{patient.patient_id}</span></p>
          <p>Age: <span className="font-medium text-slate-700">{patient.age}</span></p>
          <p>Gender: <span className="font-medium text-slate-700">{patient.gender}</span></p>
          <p>DOB: <span className="font-medium text-slate-700">{patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : 'N/A'}</span></p>
          <p>Blood Group: <span className="font-medium text-slate-700">{patient.blood_group}</span></p>
          <p>Phone: <span className="font-medium text-slate-700">{patient.phone}</span></p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200">
        <TabPanel tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
        <div className="p-6">
          {activeTab !== 'visits' && (
            <h2 className="text-lg font-semibold text-slate-800 mb-4 capitalize">Add New {activeTab.replace('s', '')}</h2>
          )}
          {activeTab !== 'visits' && (
          <form onSubmit={submitForm} className="mb-8 flex items-end gap-4 flex-wrap">
            {activeTab === 'diagnoses' && (
               <>
                 <input name="diagnosis_id" placeholder="Diagnosis ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <input name="disease_id" placeholder="Disease ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <input type="date" name="date_diagnosed" onChange={handleInputChange} className="border p-2 rounded" required />
                 <select name="severity_stage" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                    <option value="">Severity</option>
                    <option value="Mild">Mild</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Severe">Severe</option>
                 </select>
                 <select name="current_status" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                    <option value="">Status</option>
                    <option value="Active">Active</option>
                    <option value="Resolved">Resolved</option>
                 </select>
               </>
            )}
            {activeTab === 'metrics' && (
               <>
                 <input name="metric_id" placeholder="Metric ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <select name="diagnosis_id" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                   <option value="">Select Diagnosis...</option>
                   {data.diagnoses?.map(d => <option key={d.diagnosis_id} value={d.diagnosis_id}>{d.diagnosis_id} ({d.disease_id})</option>)}
                 </select>
                 <input name="metric_type" placeholder="Type (e.g. HbA1c)" onChange={handleInputChange} className="border p-2 rounded w-36" required />
                 <input type="number" step="0.1" name="value" placeholder="Value" onChange={handleInputChange} className="border p-2 rounded w-24" required />
                 <input name="unit" placeholder="Unit (%, mmHg)" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <input type="datetime-local" name="recorded_at" onChange={handleInputChange} className="border p-2 rounded" required />
               </>
            )}
            {activeTab === 'episodes' && (
               <>
                 <input name="episode_id" placeholder="Episode ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <select name="diagnosis_id" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                   <option value="">Select Diagnosis...</option>
                   {data.diagnoses?.map(d => <option key={d.diagnosis_id} value={d.diagnosis_id}>{d.diagnosis_id} ({d.disease_id})</option>)}
                 </select>
                 <input type="date" name="start_date" onChange={handleInputChange} className="border p-2 rounded" required />
                 <input type="date" name="end_date" onChange={handleInputChange} className="border p-2 rounded" />
                 <input name="severity_levels" placeholder="Severity" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <input name="triggers" placeholder="Triggers (comma separated)" onChange={handleInputChange} className="border p-2 rounded w-48" />
               </>
            )}
            {activeTab === 'risks' && (
               <>
                 <input name="assessment_id" placeholder="Risk ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <input type="number" step="0.1" name="risk_score" placeholder="Score (0-100)" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <select name="category" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                    <option value="">Category</option>
                    <option value="Low">Low</option>
                    <option value="Moderate">Moderate</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                 </select>
               </>
            )}
            {activeTab === 'plans' && (
               <>
                 <input name="plan_id" placeholder="Plan ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <select name="diagnosis_id" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                   <option value="">Select Diagnosis...</option>
                   {data.diagnoses?.map(d => <option key={d.diagnosis_id} value={d.diagnosis_id}>{d.diagnosis_id} ({d.disease_id})</option>)}
                 </select>
                 <input name="goal" placeholder="Treatment Goal" onChange={handleInputChange} className="border p-2 rounded w-48" required />
                 <input type="date" name="start_date" onChange={handleInputChange} className="border p-2 rounded" required />
               </>
            )}
            {activeTab === 'adherence' && (
               <>
                 <input name="adherence_id" placeholder="Adherence ID" onChange={handleInputChange} className="border p-2 rounded w-32" required />
                 <select name="plan_id" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                   <option value="">Select Plan...</option>
                   {data.plans?.map(p => <option key={p.plan_id} value={p.plan_id}>{p.plan_id} ({p.goal})</option>)}
                 </select>
                 <input type="date" name="log_date" onChange={handleInputChange} className="border p-2 rounded" required />
                 <select name="status" onChange={handleInputChange} className="border p-2 rounded w-32" required>
                    <option value="">Status</option>
                    <option value="Taken">Taken</option>
                    <option value="Skipped">Skipped</option>
                 </select>
                 <input name="reason_skipped" placeholder="Reason (if skipped)" onChange={handleInputChange} className="border p-2 rounded w-48" />
               </>
            )}
            <button type="submit" className="px-4 py-2 bg-teal-600 text-white rounded font-medium hover:bg-teal-700">Submit</button>
          </form>
          )}

          <div>
             <h3 className="text-md font-medium text-slate-700 mb-3">Records</h3>
             <DataTable 
               columns={getTabColumns()}
               data={data[activeTab] || []} 
             />
          </div>
        </div>
      </div>
    </div>
  );
}

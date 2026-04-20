import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import StatCard from '../components/StatCard';
import ModuleStatusBadge from '../components/ModuleStatusBadge';
import api from '../services/api';
import { Users, FileBarChart, AlertTriangle, Activity } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState({
    patients: 0,
    diagnoses: 0,
    risks: 0,
    episodes: 0
  });
  const [recentPatients, setRecentPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadDashboardData() {
      setIsLoading(true);
      try {
        // Fetch patients
        const patientsRes = await api.get('/patients');
        const patients = patientsRes.data || [];
        const patientCount = patients.length;

        // Take the most recent 8 patients for the table
        const recent = patients.slice(0, 8).map(p => ({
          ...p,
          name: `${p.first_name || ''} ${p.last_name || ''}`.trim() || p.patient_id,
          dob: p.date_of_birth ? new Date(p.date_of_birth).toLocaleDateString() : 'N/A'
        }));
        setRecentPatients(recent);

        // Fetch diagnoses count
        let diagnosesCount = 0;
        try {
          const diagRes = await api.get('/diagnoses');
          diagnosesCount = (diagRes.data || []).length;
        } catch { /* API may not exist yet */ }

        // Fetch risks count (high risk = score >= 70)
        let highRiskCount = 0;
        try {
          const risksRes = await api.get('/risks');
          const risks = risksRes.data || [];
          highRiskCount = risks.filter(r => (r.risk_score || 0) >= 70).length;
        } catch { /* API may not exist yet */ }

        // Fetch episodes count (this month)
        let episodesThisMonth = 0;
        try {
          const epRes = await api.get('/episodes');
          const episodes = epRes.data || [];
          const now = new Date();
          episodesThisMonth = episodes.filter(e => {
            const d = new Date(e.start_date || e.created_at);
            return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
          }).length;
        } catch { /* API may not exist yet */ }

        setStats({
          patients: patientCount,
          diagnoses: diagnosesCount,
          risks: highRiskCount,
          episodes: episodesThisMonth
        });
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Dashboard overview</h1>
        <p className="mt-1 text-sm text-slate-500">Summary of chronic care operations and module connectivity.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Patients" value={stats.patients} icon={Users} />
        <StatCard title="Active Diagnoses" value={stats.diagnoses} icon={FileBarChart} />
        <StatCard title="High Risk Patients" value={stats.risks} icon={AlertTriangle} />
        <StatCard title="Episodes This Month" value={stats.episodes} icon={Activity} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Patients Table */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-800">Recent Patients</h2>
            <button
              onClick={() => navigate('/patients')}
              className="text-sm text-teal-600 hover:text-teal-700 font-medium transition-colors"
            >
              View all →
            </button>
          </div>
          {isLoading ? (
            <div className="px-6 py-12 text-center text-slate-400 text-sm">Loading patients…</div>
          ) : recentPatients.length === 0 ? (
            <div className="px-6 py-12 text-center text-slate-400 text-sm">No patients found</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-medium tracking-wide">
                  <tr>
                    <th className="px-6 py-3">Patient ID</th>
                    <th className="px-6 py-3">Name</th>
                    <th className="px-6 py-3">Age</th>
                    <th className="px-6 py-3">Gender</th>
                    <th className="px-6 py-3">DOB</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {recentPatients.map((p, i) => (
                    <tr
                      key={p.patient_id || i}
                      onClick={() => navigate(`/patients/${p.patient_id}`)}
                      className="cursor-pointer hover:bg-slate-50 transition-colors"
                    >
                      <td className="px-6 py-3 text-teal-600 font-medium">{p.patient_id}</td>
                      <td className="px-6 py-3 text-slate-700">{p.name}</td>
                      <td className="px-6 py-3 text-slate-700">{p.age ?? '-'}</td>
                      <td className="px-6 py-3 text-slate-700">{p.gender || '-'}</td>
                      <td className="px-6 py-3 text-slate-700">{p.dob}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Integration Status</h2>
          <div className="space-y-4">
            <ModuleStatusBadge moduleName="Module-1 Demographics" isMock={false} statusText="LIVE" />
            <ModuleStatusBadge moduleName="Module-19 Pharmacy" isMock={true} statusText="MOCKED" />
            <ModuleStatusBadge moduleName="Module-25 Vitals" isMock={true} statusText="MOCKED" />
            <ModuleStatusBadge moduleName="Module-33 Data Models" isMock={true} statusText="MOCKED" />
          </div>
        </div>
      </div>
    </div>
  );
}

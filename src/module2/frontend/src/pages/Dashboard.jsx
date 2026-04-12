import React, { useEffect, useState } from 'react';
import StatCard from '../components/StatCard';
import ModuleStatusBadge from '../components/ModuleStatusBadge';
import DataTable from '../components/DataTable';
import api from '../services/api';
import { Users, FileBarChart, AlertTriangle, Activity } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState({
    patients: 0,
    diagnoses: 0,
    risks: 0,
    episodes: 0
  });
  
  // Real app would fetch this dynamically from API overviews
  useEffect(() => {
    async function loadStats() {
      try {
        const patients = await api.get('/patients');
        setStats(prev => ({ ...prev, patients: patients.data.length }));
      } catch (err) {
        console.error("Failed to load dashboard stats", err);
      }
    }
    loadStats();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Dashboard overview</h1>
        <p className="mt-1 text-sm text-slate-500">Summary of chronic care operations and module connectivity.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Patients" value={stats.patients} icon={Users} />
        <StatCard title="Active Diagnoses" value="-" icon={FileBarChart} />
        <StatCard title="High Risk Patients" value="-" icon={AlertTriangle} />
        <StatCard title="Episodes This Month" value="-" icon={Activity} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col items-center justify-center min-h-64 text-slate-500">
          <p>Recent Patients table will be integrated here</p>
          <span className="text-xs mt-2">Connecting to module data...</span>
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

import React from 'react';

export default function RiskDashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Risk Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">Patients sorted by risk score. (Mock UI to show layout intent)</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-100">
            <div><span className="font-semibold text-slate-800">PT-101</span> - Critical</div>
            <div className="flex items-center"><div className="w-48 bg-slate-200 h-2 rounded"><div className="bg-red-500 h-2 rounded w-[90%]"></div></div><span className="ml-3 font-semibold text-red-600 border border-red-200 bg-white px-2 py-1 rounded">Score: 92</span></div>
          </div>
          <div className="flex items-center justify-between p-4 bg-amber-50 rounded-lg border border-amber-100">
            <div><span className="font-semibold text-slate-800">PT-103</span> - High</div>
            <div className="flex items-center"><div className="w-48 bg-slate-200 h-2 rounded"><div className="bg-amber-500 h-2 rounded w-[75%]"></div></div><span className="ml-3 font-semibold text-amber-600 border border-amber-200 bg-white px-2 py-1 rounded">Score: 75</span></div>
          </div>
        </div>
      </div>
    </div>
  );
}

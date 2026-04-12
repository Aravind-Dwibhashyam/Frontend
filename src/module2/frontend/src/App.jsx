import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import PatientDetail from './pages/PatientDetail';
import Diagnoses from './pages/Diagnoses';
import RiskDashboard from './pages/RiskDashboard';
import IntegrationLog from './pages/IntegrationLog';
import ToastContainer from './components/ToastNotification';

function App() {
  return (
    <BrowserRouter>
      <ToastContainer />
      <div className="flex h-screen bg-slate-50 text-slate-800">
        <Sidebar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-slate-50 p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/patients" element={<Patients />} />
            <Route path="/patients/:id" element={<PatientDetail />} />
            <Route path="/diagnoses" element={<Diagnoses />} />
            <Route path="/risks" element={<RiskDashboard />} />
            <Route path="/integrations" element={<IntegrationLog />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, FileBarChart, AlertTriangle, Activity } from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Users, label: 'Patients', path: '/patients' },
  { icon: FileBarChart, label: 'Diagnoses', path: '/diagnoses' },
  { icon: AlertTriangle, label: 'Risk Dashboard', path: '/risks' },
  { icon: Activity, label: 'Integration Logs', path: '/integrations' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-navy-900 text-slate-100 flex flex-col h-full shadow-xl">
      <div className="p-6 border-b border-navy-800 flex items-center space-x-3">
        <div className="w-8 h-8 rounded bg-teal-500 flex items-center justify-center font-bold text-white text-xl shadow-lg">C</div>
        <h1 className="text-xl font-semibold tracking-wide">ChronicCare</h1>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${
                isActive
                  ? 'bg-teal-600 text-white shadow-md'
                  : 'text-slate-400 hover:bg-navy-800 hover:text-slate-100'
              }`
            }
          >
            <item.icon size={20} />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-navy-800 text-xs text-slate-500 text-center">
        Module 2 &bull; Management System
      </div>
    </aside>
  );
}

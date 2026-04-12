import React from 'react';
import { Activity } from 'lucide-react';

export default function ModuleStatusBadge({ moduleName, isMock, statusText }) {
  const isHealthy = statusText.toLowerCase() === 'live' || statusText.toLowerCase() === 'mocked';
  
  return (
    <div className={`inline-flex flex-col items-start px-4 py-3 rounded-lg border ${
      isHealthy ? 'bg-teal-50 border-teal-100' : 'bg-red-50 border-red-100'
    }`}>
      <div className="flex items-center space-x-2">
        <Activity size={16} className={isHealthy ? 'text-teal-600' : 'text-red-500'} />
        <span className="font-semibold text-slate-800 text-sm">{moduleName}</span>
      </div>
      <div className="mt-1 flex items-center space-x-2 text-xs">
        <span className={`px-2 py-0.5 rounded-full font-medium ${
          isMock ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'
        }`}>
          {isMock ? 'MOCK' : 'REAL'}
        </span>
        <span className={isHealthy ? 'text-teal-600 font-medium' : 'text-red-600 font-medium'}>
          {statusText.toUpperCase()}
        </span>
      </div>
    </div>
  );
}

import React from 'react';

export default function TabPanel({ tabs, activeTab, onTabChange }) {
  return (
    <div className="border-b border-slate-200 mb-6 flex overflow-x-auto hide-scrollbar">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`flex-shrink-0 px-6 py-3 font-medium text-sm transition-all border-b-2 outline-none ${
            activeTab === tab.id
              ? 'border-teal-500 text-teal-600 bg-teal-50/50'
              : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

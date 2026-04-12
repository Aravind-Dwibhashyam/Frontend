import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

// A simple global toast event system could be used, but since we are keeping it simple, 
// this component will manage its own state, exposed via a global function.

export const toastEvent = new EventTarget();

export function showToast(message, type = 'info') {
  toastEvent.dispatchEvent(new CustomEvent('show', { detail: { message, type } }));
}

export default function ToastContainer() {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const handleShow = (e) => {
      const id = Date.now();
      setToasts((prev) => [...prev, { ...e.detail, id }]);
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, 4000);
    };

    toastEvent.addEventListener('show', handleShow);
    return () => toastEvent.removeEventListener('show', handleShow);
  }, []);

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col space-y-3">
      {toasts.map((toast) => (
        <div 
          key={toast.id} 
          className="flex items-center space-x-3 bg-navy-900 border border-navy-800 text-white px-4 py-3 rounded-lg shadow-xl min-w-80 animate-in fade-in slide-in-from-bottom flex-shrink-0"
        >
          {toast.type === 'success' && <CheckCircle className="text-teal-400 shrink-0" size={20} />}
          {toast.type === 'error' && <AlertCircle className="text-red-400 shrink-0" size={20} />}
          {toast.type === 'info' && <Info className="text-blue-400 shrink-0" size={20} />}
          <p className="flex-1 text-sm font-medium">{toast.message}</p>
        </div>
      ))}
    </div>
  );
}

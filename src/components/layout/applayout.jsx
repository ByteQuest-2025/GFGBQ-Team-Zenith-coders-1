import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './navbar';
import Footer from './Footer';
import { useToast } from '../../context/toastcontext';
import Toast from '../ui/toast';

const AppLayout = () => {
  const { toasts, removeToast } = useToast();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
      
      {/* Toast Container */}
      <div className="fixed top-4 right-4 space-y-2 z-50">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default AppLayout;
import React from 'react';
import { AuthProvider } from '../context/authcontext';
import { ToastProvider } from '../context/toastcontext';
import AppRoutes from './routes';

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <AppRoutes />
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
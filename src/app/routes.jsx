import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/authcontext';
import AppLayout from '../components/layout/applayout';
import LandingPage from '../pages/landingpage';
import LoginPage from '../pages/loginpage';
import SubmitComplaintPage from '../pages/submitcomplaintpage';
import MyComplaintsPage from '../pages/mycomplaintspage';
import ComplaintDetailPage from '../pages/complaintdetailpage';
import AboutImpactPage from '../pages/aboutimpactpage';

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/about" element={<AboutImpactPage />} />
        
        <Route path="/submit" element={
          <ProtectedRoute>
            <SubmitComplaintPage />
          </ProtectedRoute>
        } />
        
        <Route path="/my" element={
          <ProtectedRoute>
            <MyComplaintsPage />
          </ProtectedRoute>
        } />
        
        <Route path="/complaints/:id" element={
          <ProtectedRoute>
            <ComplaintDetailPage />
          </ProtectedRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
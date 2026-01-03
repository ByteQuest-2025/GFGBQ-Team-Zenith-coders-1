import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Bell, User, LogOut } from 'lucide-react';
import { useAuth } from '../../context/authcontext';
import Button from '../ui/button';

const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  
  return (
    <nav className="bg-white shadow-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center justify-center">
                <Bell className="text-white" size={24} />
              </div>
              <span className="font-bold text-xl">GrievanceAI</span>
            </Link>
            <div className="hidden md:flex gap-6">
              <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">Home</Link>
              <Link to="/submit" className="text-gray-700 hover:text-blue-600 font-medium">Submit</Link>
              <Link to="/my" className="text-gray-700 hover:text-blue-600 font-medium">My Complaints</Link>
              <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium">About</Link>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <div className="hidden md:flex items-center gap-3 px-4 py-2 bg-gray-100 rounded-lg">
                  <User size={20} className="text-gray-600" />
                  <span className="font-medium">{user.name}</span>
                </div>
                <button onClick={logout} className="text-gray-600 hover:text-red-600 transition-colors" title="Logout">
                  <LogOut size={20} />
                </button>
              </>
            ) : (
              <Link to="/login">
                <Button variant="primary" size="sm">
                  Login
                </Button>
              </Link>
            )}
            <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-4 py-4 space-y-3">
            <Link to="/" className="block text-gray-700 hover:text-blue-600 font-medium">Home</Link>
            <Link to="/submit" className="block text-gray-700 hover:text-blue-600 font-medium">Submit</Link>
            <Link to="/my" className="block text-gray-700 hover:text-blue-600 font-medium">My Complaints</Link>
            <Link to="/about" className="block text-gray-700 hover:text-blue-600 font-medium">About</Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
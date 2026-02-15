import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, BarChart3 } from 'lucide-react';

function Navbar() {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="glass-effect shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
            <span className="ml-2 text-xl font-bold text-gray-800 dark:text-slate-100">
              AI Data Leakage Detection
            </span>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`flex items-center px-4 py-2 rounded-lg transition-all ${
                isActive('/')
                  ? 'bg-indigo-600 dark:bg-indigo-500 text-white shadow-md'
                  : 'text-gray-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-700/50'
              }`}
            >
              <Shield className="h-5 w-5 mr-2" />
              Detection
            </Link>
            
            <Link
              to="/dashboard"
              className={`flex items-center px-4 py-2 rounded-lg transition-all ${
                isActive('/dashboard')
                  ? 'bg-indigo-600 dark:bg-indigo-500 text-white shadow-md'
                  : 'text-gray-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-700/50'
              }`}
            >
              <BarChart3 className="h-5 w-5 mr-2" />
              Dashboard
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

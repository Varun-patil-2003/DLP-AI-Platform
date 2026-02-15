import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertTriangle, Activity, TrendingUp, Shield, RefreshCw, Download } from 'lucide-react';
import DarkModeToggle from '../components/DarkModeToggle';

function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [alertsRes, statsRes] = await Promise.all([
        axios.get('/api/alerts'),
        axios.get('/api/stats')
      ]);
      
      setAlerts(alertsRes.data.alerts || []);
      setStats(statsRes.data);
    } catch (err) {
      setError('Failed to fetch dashboard data. Make sure the backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getRiskBadge = (riskLevel) => {
    const badges = {
      LOW: 'risk-low',
      MEDIUM: 'risk-medium',
      HIGH: 'risk-high',
      CRITICAL: 'risk-critical',
    };
    return badges[riskLevel] || 'risk-low';
  };

  const exportAlerts = () => {
    if (alerts.length === 0) {
      alert('No alerts to export');
      return;
    }

    const csv = [
      ['Timestamp', 'Risk Level', 'Confidence', 'User', 'Message'].join(','),
      ...alerts.map(alert => [
        alert.timestamp || new Date().toISOString(),
        alert.risk_level,
        alert.confidence,
        alert.user || 'N/A',
        `"${alert.message || ''}"`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `alerts_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  if (loading && !stats) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <RefreshCw className="h-12 w-12 text-white animate-spin mx-auto mb-4" />
            <p className="text-white dark:text-slate-200 text-lg">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="glass-effect rounded-2xl p-6 shadow-2xl border-2 border-red-300">
          <div className="flex items-start">
            <AlertTriangle className="h-6 w-6 text-red-600 mr-3 flex-shrink-0" />
            <div>
              <h3 className="text-lg font-semibold text-red-800 dark:text-red-400 mb-1">Error</h3>
              <p className="text-red-700 dark:text-red-300">{error}</p>
              <p className="text-sm text-red-600 mt-2">
                Start the Flask backend:
                <code className="block mt-1 bg-red-50 px-2 py-1 rounded">
                  python app/app.py
                </code>
              </p>
              <button
                onClick={fetchData}
                className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-all"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <DarkModeToggle />
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white dark:text-slate-50 mb-2">
              Security Dashboard
            </h1>
            <p className="text-white dark:text-slate-200 text-lg opacity-90">
              Real-time monitoring and alerts
            </p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={fetchData}
              disabled={loading}
              className="glass-effect px-4 py-2 rounded-lg text-gray-700 dark:text-slate-200 hover:bg-white/80 transition-all flex items-center disabled:opacity-50"
            >
              <RefreshCw className={`h-5 w-5 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={exportAlerts}
              className="glass-effect px-4 py-2 rounded-lg text-gray-700 dark:text-slate-200 hover:bg-white/80 transition-all flex items-center"
            >
              <Download className="h-5 w-5 mr-2" />
              Export
            </button>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="glass-effect rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-slate-400 text-sm font-medium">Total Predictions</p>
                <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                  {stats?.total_predictions || 0}
                </p>
              </div>
              <Activity className="h-12 w-12 text-indigo-600 opacity-80" />
            </div>
          </div>

          <div className="glass-effect rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-slate-400 text-sm font-medium">Alerts Generated</p>
                <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                  {stats?.alerts_count || 0}
                </p>
              </div>
              <AlertTriangle className="h-12 w-12 text-red-600 opacity-80" />
            </div>
          </div>

          <div className="glass-effect rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-slate-400 text-sm font-medium">Detection Rate</p>
                <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                  {stats?.detection_rate || '0'}%
                </p>
              </div>
              <TrendingUp className="h-12 w-12 text-green-600 opacity-80" />
            </div>
          </div>

          <div className="glass-effect rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-slate-400 text-sm font-medium">System Status</p>
                <p className="text-lg font-bold text-green-600 dark:text-green-400 mt-1">ACTIVE</p>
              </div>
              <Shield className="h-12 w-12 text-blue-600 opacity-80" />
            </div>
          </div>
        </div>

        {/* Alerts Table */}
        <div className="glass-effect rounded-2xl p-6 shadow-2xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-slate-100">Recent Alerts</h2>
            <span className="text-sm text-gray-600 dark:text-slate-400">
              Last updated: {new Date().toLocaleTimeString()}
            </span>
          </div>

          {alerts.length === 0 ? (
            <div className="text-center py-12">
              <Shield className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-800 dark:text-slate-100 mb-1">
                No Alerts Yet
              </h3>
              <p className="text-gray-500 dark:text-slate-400">
                Make some predictions on the Detection page to see alerts here.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-gray-200 dark:border-gray-600">
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                      Time
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                      Risk Level
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                      Confidence
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                      User
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                      Message
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {alerts.map((alert, index) => (
                    <tr
                      key={index}
                      className="border-b border-gray-100 dark:border-gray-700 hover:bg-white/50 dark:hover:bg-gray-700/50 transition-colors"
                    >
                      <td className="py-3 px-4 text-gray-600 dark:text-slate-300 text-sm">
                        {alert.timestamp
                          ? new Date(alert.timestamp).toLocaleString()
                          : new Date().toLocaleString()}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`risk-badge ${getRiskBadge(alert.risk_level)}`}>
                          {alert.risk_level}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-700 dark:text-slate-300 font-medium">
                        {(alert.confidence * 100).toFixed(1)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-slate-200">
                        {alert.user || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-slate-200">
                        {alert.message || 'Data leakage detected'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="mt-6 glass-effect rounded-xl p-4 shadow-lg">
          <div className="flex items-start">
            <Shield className="h-5 w-5 text-indigo-600 dark:text-indigo-400 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-gray-700 dark:text-slate-300">
                <strong className="text-gray-900 dark:text-slate-100">Auto-refresh enabled:</strong> Dashboard updates every 30 seconds.
                Click "Refresh" for immediate update.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

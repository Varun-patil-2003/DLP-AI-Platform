import React, { useState } from 'react';
import axios from 'axios';
import { Shield, AlertTriangle, CheckCircle, Loader } from 'lucide-react';
import DarkModeToggle from '../components/DarkModeToggle';

function Home() {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    user: 'USER_1234',
    pc: 'PC_001',
    Authority: 'admin',
    Through_pwd: 1,
    Through_pin: 0,
    Through_MFA: 1,
    'Data Modification': 0,
    'Confidential Data Access': 1,
    'Confidential File Transfer': 0,
    'External Destination': 'no',
    'File Operation': 'read',
    'Data Sensitivity Level': 'confidential',
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Numeric fields that need conversion
    const numericFields = [
      'Through_pwd', 'Through_pin', 'Through_MFA',
      'Data Modification', 'Confidential Data Access', 'Confidential File Transfer'
    ];
    
    setFormData({
      ...formData,
      [name]: numericFields.includes(name) ? parseFloat(value) : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert numeric fields from strings to numbers
      const payload = {
        ...formData,
        Through_pwd: parseFloat(formData.Through_pwd),
        Through_pin: parseFloat(formData.Through_pin),
        Through_MFA: parseFloat(formData.Through_MFA),
        'Data Modification': parseFloat(formData['Data Modification']),
        'Confidential Data Access': parseFloat(formData['Confidential Data Access']),
        'Confidential File Transfer': parseFloat(formData['Confidential File Transfer']),
      };
      
      const response = await axios.post('/api/predict', payload);
      console.log('API Response:', response.data); // Debug log
      setResult(response.data);
    } catch (err) {
      console.error('Prediction error:', err); // Debug log
      setError(err.response?.data?.error || 'Failed to get prediction. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadge = (riskLevel) => {
    const badges = {
      LOW: 'risk-low',
      MEDIUM: 'risk-medium',
      HIGH: 'risk-high',
      CRITICAL: 'risk-critical',
    };
    return badges[riskLevel] || 'risk-low';
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <DarkModeToggle />
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Shield className="h-16 w-16 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-white dark:text-slate-50 mb-2">
            AI Data Leakage Detection
          </h1>
          <p className="text-white dark:text-slate-200 text-lg opacity-90">
            Real-time behavioral analysis and anomaly detection
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="glass-effect rounded-2xl p-6 shadow-2xl">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-slate-100 mb-6">
              Activity Parameters
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* User Info */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  User ID
                </label>
                <input
                  type="text"
                  name="user"
                  value={formData.user}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-slate-800/50 text-gray-900 dark:text-slate-100"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  PC ID
                </label>
                <input
                  type="text"
                  name="pc"
                  value={formData.pc}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-slate-800/50 text-gray-900 dark:text-slate-100"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  Authority Level
                </label>
                <select
                  name="Authority"
                  value={formData.Authority}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-slate-800/50 text-gray-900 dark:text-slate-100"
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                  <option value="superadmin">Super Admin</option>
                  <option value="guest">Guest</option>
                </select>
              </div>

              {/* Authentication Methods */}
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    Password
                  </label>
                  <select
                    name="Through_pwd"
                    value={formData.Through_pwd}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    PIN
                  </label>
                  <select
                    name="Through_pin"
                    value={formData.Through_pin}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    MFA
                  </label>
                  <select
                    name="Through_MFA"
                    value={formData.Through_MFA}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
              </div>

              {/* Data Operations */}
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    Data Mod
                  </label>
                  <select
                    name="Data Modification"
                    value={formData['Data Modification']}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    Conf. Access
                  </label>
                  <select
                    name="Confidential Data Access"
                    value={formData['Confidential Data Access']}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                    File Transfer
                  </label>
                  <select
                    name="Confidential File Transfer"
                    value={formData['Confidential File Transfer']}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  External Destination
                </label>
                <select
                  name="External Destination"
                  value={formData['External Destination']}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="no">No</option>
                  <option value="yes">Yes</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  File Operation
                </label>
                <select
                  name="File Operation"
                  value={formData['File Operation']}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="read">Read</option>
                  <option value="write">Write</option>
                  <option value="delete">Delete</option>
                  <option value="move">Move</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                  Data Sensitivity Level
                </label>
                <select
                  name="Data Sensitivity Level"
                  value={formData['Data Sensitivity Level']}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="confidential">Confidential</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <Loader className="animate-spin h-5 w-5 mr-2" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Shield className="h-5 w-5 mr-2" />
                    Analyze Activity
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {error && (
              <div className="glass-effect rounded-2xl p-6 shadow-2xl border-2 border-red-300">
                <div className="flex items-start">
                  <AlertTriangle className="h-6 w-6 text-red-600 mr-3 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-semibold text-red-800 mb-1">
                      Error
                    </h3>
                    <p className="text-red-700">{error}</p>
                    <p className="text-sm text-red-600 mt-2">
                      Make sure the Flask backend is running on port 5000:
                      <code className="block mt-1 bg-red-50 px-2 py-1 rounded">
                        python app/app.py
                      </code>
                    </p>
                  </div>
                </div>
              </div>
            )}

            {result && (
              <>
                {/* Prediction Result */}
                <div className="glass-effect rounded-2xl p-6 shadow-2xl">
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-4">
                    Detection Result
                  </h3>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-700 dark:text-slate-300 font-medium">Status:</span>
                      {result.prediction === 1 ? (
                        <div className="flex items-center text-red-600">
                          <AlertTriangle className="h-5 w-5 mr-2" />
                          <span className="font-bold">LEAKAGE DETECTED</span>
                        </div>
                      ) : (
                        <div className="flex items-center text-green-600">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          <span className="font-bold">NORMAL ACTIVITY</span>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-700 dark:text-slate-300 font-medium">Risk Level:</span>
                      <span className={`risk-badge ${getRiskBadge(result.risk_level)}`}>
                        {result.risk_level}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-slate-700 dark:text-slate-300 font-medium">Confidence:</span>
                      <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                        {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Model Scores */}
                <div className="glass-effect rounded-2xl p-6 shadow-2xl">
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-4">
                    Model Analysis
                  </h3>
                  
                  <div className="space-y-3">
                    {result.models && Object.keys(result.models).length > 0 ? (
                      Object.entries(result.models).map(([model, score]) => (
                        score !== null && (
                          <div key={model}>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-700 dark:text-slate-200 font-medium capitalize">
                                {model.replace('_', ' ')}
                              </span>
                              <span className="text-gray-600 dark:text-slate-400">
                                {(score * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-indigo-600 dark:bg-indigo-400 h-2 rounded-full transition-all"
                                style={{ width: `${score * 100}%` }}
                              />
                            </div>
                          </div>
                        )
                      ))
                    ) : (
                      <div className="text-center py-4">
                        <p className="text-gray-600 dark:text-slate-400">
                          Model scores available after analysis
                        </p>
                      </div>
                    )}
                  </div>
                  
                  {/* Additional Details */}
                  <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-xs text-gray-500 dark:text-slate-400 mb-1">Risk Score</p>
                        <p className="text-lg font-bold text-gray-800 dark:text-slate-100">
                          {result.risk_score ? (result.risk_score * 100).toFixed(1) + '%' : 'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 dark:text-slate-400 mb-1">Timestamp</p>
                        <p className="text-sm text-gray-700 dark:text-slate-300">
                          {result.timestamp ? new Date(result.timestamp).toLocaleTimeString() : 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Alert Message */}
                {result.message && (
                  <div className="glass-effect rounded-2xl p-6 shadow-2xl">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">
                        {result.ai_powered && (
                          <span className="text-xs bg-gradient-to-r from-purple-500 to-pink-500 text-white px-2 py-1 rounded-full mr-2">
                            AI-POWERED
                          </span>
                        )}
                        Alert Analysis
                      </h3>
                    </div>
                    <p className="text-gray-700 dark:text-slate-300 leading-relaxed">{result.message}</p>
                  </div>
                )}

                {/* AI Recommendations */}
                {result.recommendations && result.recommendations.length > 0 && (
                  <div className="glass-effect rounded-2xl p-6 shadow-2xl">
                    <div className="flex items-center mb-4">
                      <span className="text-xs bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-2 py-1 rounded-full mr-2">
                        AI RECOMMENDATIONS
                      </span>
                      <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">
                        Suggested Actions
                      </h3>
                    </div>
                    <div className="space-y-3">
                      {result.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-start">
                          <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-300 text-sm font-semibold mr-3 flex-shrink-0 mt-0.5">
                            {index + 1}
                          </span>
                          <p className="text-gray-700 dark:text-slate-300 flex-1">{rec}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {!result && !error && (
              <div className="glass-effect rounded-2xl p-12 shadow-2xl text-center">
                <Shield className="h-20 w-20 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-600 dark:text-slate-300 mb-2">
                  Ready to Analyze
                </h3>
                <p className="text-gray-500 dark:text-slate-400">
                  Fill in the activity parameters and click "Analyze Activity" to detect potential data leakage.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;

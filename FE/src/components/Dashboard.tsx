import React, { useState } from 'react';
import { DashboardLayout } from './layout/DashboardLayout';
import TwoFactorSetup from './auth/TwoFactorSetup';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [show2FASetup, setShow2FASetup] = useState(false);

  const handle2FASetupComplete = () => {
    setShow2FASetup(false);
    window.location.reload();
  };

  if (show2FASetup) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
        <TwoFactorSetup 
          onSetupComplete={handle2FASetupComplete}
          onCancel={() => setShow2FASetup(false)}
        />
      </div>
    );
  }

  return (
    <DashboardLayout>
      {/* Welcome Card */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl p-6 lg:p-8 text-white mb-6 lg:mb-8 shadow-xl"
      >
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h2 className="text-2xl lg:text-3xl font-bold mb-2">Welcome back, {user?.first_name}! 👋</h2>
            <p className="text-blue-100">Here's what's happening with your ChamaNexus account today.</p>
          </div>
          <div className="mt-4 md:mt-0 bg-white/20 backdrop-blur-sm rounded-xl p-4">
            <p className="text-sm">Account Status</p>
            <div className="flex items-center mt-2">
              <div className={`w-3 h-3 rounded-full ${user?.is_verified ? 'bg-green-400' : 'bg-yellow-400'} mr-2`}></div>
              <span className="font-semibold">{user?.is_verified ? 'Verified' : 'Pending Verification'}</span>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        {/* Left Column - Profile & Security */}
        <div className="lg:col-span-2 space-y-6 lg:space-y-8">
          {/* Profile Card */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl p-4 lg:p-6 shadow-soft border border-gray-200/50"
          >
            <h3 className="text-xl font-bold text-gray-900 mb-4 lg:mb-6">Profile Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">
              <div>
                <label className="text-sm font-medium text-gray-500">Full Name</label>
                <p className="mt-1 text-lg font-semibold text-gray-900">{user?.first_name} {user?.last_name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Email Address</label>
                <p className="mt-1 text-lg font-semibold text-gray-900">{user?.email}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Phone Number</label>
                <p className="mt-1 text-lg font-semibold text-gray-900">{user?.phone_number || 'Not provided'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Member Since</label>
                <p className="mt-1 text-lg font-semibold text-gray-900">
                  {new Date(user?.created_at || '').toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Security Card */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl p-4 lg:p-6 shadow-soft border border-gray-200/50"
          >
            <div className="flex justify-between items-center mb-4 lg:mb-6">
              <h3 className="text-xl font-bold text-gray-900">Security Settings</h3>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${user?.two_factor_enabled ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                {user?.two_factor_enabled ? 'Protected' : 'At Risk'}
              </div>
            </div>
            
            <div className="space-y-4 lg:space-y-6">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                <div className="flex items-center">
                  <div className="bg-blue-100 p-3 rounded-lg mr-4">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Two-Factor Authentication</h4>
                    <p className="text-sm text-gray-500">Add an extra layer of security to your account</p>
                  </div>
                </div>
                <button
                  onClick={() => setShow2FASetup(true)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${user?.two_factor_enabled 
                    ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                    : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 shadow-md hover:shadow-lg'}`}
                >
                  {user?.two_factor_enabled ? '✓ Enabled' : 'Enable 2FA'}
                </button>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Right Column - Quick Stats */}
        <div className="space-y-6 lg:space-y-8">
          {/* Account Stats */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-2xl p-4 lg:p-6 shadow-soft border border-gray-200/50"
          >
            <h3 className="text-xl font-bold text-gray-900 mb-4 lg:mb-6">Account Overview</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl">
                <div>
                  <p className="text-sm text-gray-600">Account Status</p>
                  <p className="text-lg font-bold text-gray-900">{user?.is_verified ? 'Active' : 'Pending'}</p>
                </div>
                <div className={`p-3 rounded-lg ${user?.is_verified ? 'bg-green-100' : 'bg-yellow-100'}`}>
                  <svg className={`w-6 h-6 ${user?.is_verified ? 'text-green-600' : 'text-yellow-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={user?.is_verified ? "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" : "M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"} />
                  </svg>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
                <div>
                  <p className="text-sm text-gray-600">Security Level</p>
                  <p className="text-lg font-bold text-gray-900">
                    {user?.two_factor_enabled ? 'High' : 'Medium'}
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-purple-100">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl">
                <div>
                  <p className="text-sm text-gray-600">Last Login</p>
                  <p className="text-lg font-bold text-gray-900">
                    {user?.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                  </p>
                </div>
                <div className="p-3 rounded-lg bg-green-100">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-2xl p-4 lg:p-6 shadow-soft border border-gray-200/50"
          >
            <h3 className="text-xl font-bold text-gray-900 mb-4 lg:mb-6">Quick Actions</h3>
            
            <div className="space-y-3">
              <button className="w-full flex items-center justify-between p-4 bg-blue-50 hover:bg-blue-100 rounded-xl transition-colors duration-200 group">
                <span className="font-medium text-gray-900">Create New Chama</span>
                <svg className="w-5 h-5 text-blue-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
              
              <button className="w-full flex items-center justify-between p-4 bg-purple-50 hover:bg-purple-100 rounded-xl transition-colors duration-200 group">
                <span className="font-medium text-gray-900">Invite Members</span>
                <svg className="w-5 h-5 text-purple-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </button>
              
              <button className="w-full flex items-center justify-between p-4 bg-green-50 hover:bg-green-100 rounded-xl transition-colors duration-200 group">
                <span className="font-medium text-gray-900">View Reports</span>
                <svg className="w-5 h-5 text-green-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;

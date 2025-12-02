import React from 'react';
import { DashboardLayout } from '../layout/DashboardLayout';

const DashboardProfile: React.FC = () => {
  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Profile Settings</h1>
        <div className="bg-white rounded-2xl p-6 shadow-soft border border-gray-200/50">
          <p className="text-gray-600">Profile settings page coming soon...</p>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DashboardProfile;

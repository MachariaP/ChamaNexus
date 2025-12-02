import React from 'react';
import { DashboardLayout } from './layout/DashboardLayout';
import MemberDashboard from './dashboard/MemberDashboard';
import TreasurerDashboard from './dashboard/TreasurerDashboard';
import { useAuth } from '../hooks/useAuth';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  // Determine which dashboard to show based on user role
  const isTreasurer = user?.is_staff || false; // Adjust based on your user model

  return (
    <DashboardLayout>
      {isTreasurer ? <TreasurerDashboard /> : <MemberDashboard />}
    </DashboardLayout>
  );
};

export default Dashboard;

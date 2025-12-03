import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import BalanceCard from './widgets/BalanceCard';
import MeetingCard from './widgets/MeetingCard';
import LoanStatusCard from './widgets/LoanStatusCard';
import TransactionList from './widgets/TransactionList';
import QuickActions from './widgets/QuickActions';

interface DashboardData {
  personal_balance: number;
  group_balance: number;
  next_meeting: {
    date: string;
    time: string;
    location: string;
    agenda: string;
    my_position: number;
    total_positions: number;
  } | null;
  loan_status: {
    active: boolean;
    amount_borrowed: number;
    amount_paid: number;
    remaining_balance: number;
    next_payment_date: string;
    next_payment_amount: number;
  } | null;
  recent_transactions: Array<{
    id: string;
    date: string;
    type: 'contribution' | 'loan_payment' | 'loan_disbursement' | 'payout' | 'fine';
    amount: number;
    description: string;
    status: 'completed' | 'pending' | 'failed';
  }>;
  contribution_summary: {
    this_month: number;
    total: number;
    last_contribution_date: string;
  };
}

const MemberDashboard: React.FC = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/accounts/dashboard/summary/');
      setDashboardData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load dashboard data');
      console.error('Dashboard data error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4">
        <p className="text-red-700">{error}</p>
        <button
          onClick={fetchDashboardData}
          className="mt-2 text-sm text-red-600 hover:text-red-800"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No dashboard data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl p-6 text-white shadow-lg"
      >
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 className="text-2xl font-bold mb-2">Karibu, {user?.first_name}! 👋</h1>
            <p className="text-blue-100 opacity-90">
              Here's your ChamaNexus summary as of {new Date().toLocaleDateString('en-KE')}
            </p>
          </div>
          <div className="mt-4 md:mt-0 bg-white/20 backdrop-blur-sm rounded-xl p-4">
            <p className="text-sm font-medium">Member Since</p>
            <p className="text-lg font-bold">
              {new Date(user?.created_at || '').toLocaleDateString('en-KE', {
                year: 'numeric',
                month: 'long'
              })}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <BalanceCard
          title="Personal Balance"
          amount={dashboardData.personal_balance}
          currency="KES"
          trend="+2.5% this month"
          icon="wallet"
        />
        
        <BalanceCard
          title="Group Pot"
          amount={dashboardData.group_balance}
          currency="KES"
          subtitle={`${dashboardData.contribution_summary.this_month.toLocaleString()} KES this month`}
          icon="users"
        />
        
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-green-100 p-3 rounded-lg mr-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">Contributions This Month</p>
              <p className="text-xl font-bold text-gray-900">
                {dashboardData.contribution_summary.this_month.toLocaleString()} KES
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-blue-100 p-3 rounded-lg mr-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">Last Contribution</p>
              <p className="text-xl font-bold text-gray-900">
                {new Date(dashboardData.contribution_summary.last_contribution_date).toLocaleDateString('en-KE')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Primary Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Meeting Card */}
          {dashboardData.next_meeting && (
            <MeetingCard meeting={dashboardData.next_meeting} />
          )}

          {/* Loan Status */}
          {dashboardData.loan_status?.active && (
            <LoanStatusCard loan={dashboardData.loan_status} />
          )}

          {/* Recent Transactions */}
          <TransactionList transactions={dashboardData.recent_transactions} />
        </div>

        {/* Right Column - Actions & Info */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <QuickActions userRole="member" />

          {/* Merry-go-round Position */}
          {dashboardData.next_meeting && (
            <div className="bg-white rounded-2xl p-6 shadow border border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Merry-go-round Position</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Your Position</span>
                  <span className="text-xl font-bold text-blue-600">
                    {dashboardData.next_meeting.my_position} of {dashboardData.next_meeting.total_positions}
                  </span>
                </div>
                <div className="relative pt-1">
                  <div className="flex mb-2 items-center justify-between">
                    <div>
                      <span className="text-xs font-semibold inline-block text-blue-600">
                        Progress
                      </span>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-semibold inline-block text-blue-600">
                        {Math.round((dashboardData.next_meeting.my_position / dashboardData.next_meeting.total_positions) * 100)}%
                      </span>
                    </div>
                  </div>
                  <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-blue-100">
                    <div
                      style={{ width: `${(dashboardData.next_meeting.my_position / dashboardData.next_meeting.total_positions) * 100}%` }}
                      className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-500"
                    ></div>
                  </div>
                </div>
                <p className="text-sm text-gray-500">
                  {dashboardData.next_meeting.my_position === 1 
                    ? "You're next in line! 🎉"
                    : `Estimated wait: ${dashboardData.next_meeting.my_position - 1} more cycle(s)`}
                </p>
              </div>
            </div>
          )}

          {/* Contribution Summary */}
          <div className="bg-white rounded-2xl p-6 shadow border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Contribution Summary</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">This Month</span>
                <span className="font-bold">{dashboardData.contribution_summary.this_month.toLocaleString()} KES</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total Contributed</span>
                <span className="font-bold">{dashboardData.contribution_summary.total.toLocaleString()} KES</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Last Contribution</span>
                <span className="font-medium">
                  {new Date(dashboardData.contribution_summary.last_contribution_date).toLocaleDateString('en-KE')}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MemberDashboard;

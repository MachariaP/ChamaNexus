import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, AlertCircle, TrendingUp, FileText, Clock, CheckCircle } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import BalanceCard from './widgets/BalanceCard';
import TransactionList from './widgets/TransactionList';
import QuickActions from './widgets/QuickActions';
import DefaultersList from './widgets/DefaultersList';

interface TreasurerDashboardData {
  group_summary: {
    total_balance: number;
    total_collected_today: number;
    outstanding_loans: number;
    defaulters_count: number;
    total_members: number;
    attendance_rate: number;
  };
  defaulters: Array<{
    id: string;
    name: string;
    phone: string;
    amount: number;
    days_overdue: number;
    last_contribution: string;
  }>;
  pending_actions: {
    pending_loans: number;
    pending_approvals: number;
    upcoming_meetings: number;
    overdue_fines: number;
  };
  recent_group_transactions: Array<{
    id: string;
    date: string;
    type: string;
    member_name: string;
    amount: number;
    description: string;
    status: string;
  }>;
}

const TreasurerDashboard: React.FC = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState<TreasurerDashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTreasurerData();
  }, []);

  const fetchTreasurerData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/v1/dashboard/treasurer/');
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to load treasurer data:', error);
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

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No treasurer data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white shadow-lg"
      >
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 className="text-2xl font-bold mb-2">Treasurer Dashboard 👑</h1>
            <p className="text-blue-100 opacity-90">
              Group management for {user?.first_name} - Last updated {new Date().toLocaleTimeString('en-KE')}
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex space-x-4">
            <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
              <p className="text-sm font-medium">Members</p>
              <p className="text-lg font-bold">{dashboardData.group_summary.total_members}</p>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
              <p className="text-sm font-medium">Attendance</p>
              <p className="text-lg font-bold">{dashboardData.group_summary.attendance_rate}%</p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Pending Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-yellow-100 p-3 rounded-lg mr-4">
              <FileText className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Pending Loans</p>
              <p className="text-xl font-bold text-gray-900">
                {dashboardData.pending_actions.pending_loans}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-blue-100 p-3 rounded-lg mr-4">
              <CheckCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Approvals</p>
              <p className="text-xl font-bold text-gray-900">
                {dashboardData.pending_actions.pending_approvals}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-red-100 p-3 rounded-lg mr-4">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Defaulters</p>
              <p className="text-xl font-bold text-gray-900">
                {dashboardData.group_summary.defaulters_count}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl p-4 shadow border border-gray-200">
          <div className="flex items-center">
            <div className="bg-green-100 p-3 rounded-lg mr-4">
              <Clock className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Upcoming</p>
              <p className="text-xl font-bold text-gray-900">
                {dashboardData.pending_actions.upcoming_meetings}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Group Overview */}
        <div className="lg:col-span-2 space-y-6">
          {/* Group Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <BalanceCard
              title="Total Collected Today"
              amount={dashboardData.group_summary.total_collected_today}
              currency="KES"
              icon="coins"
            />
            
            <BalanceCard
              title="Outstanding Loans"
              amount={dashboardData.group_summary.outstanding_loans}
              currency="KES"
              trend="15% overdue"
              icon="bank"
            />
          </div>

          {/* Defaulters List */}
          <DefaultersList defaulters={dashboardData.defaulters} />

          {/* Group Transactions */}
          <TransactionList 
            transactions={dashboardData.recent_group_transactions.map(t => ({
              id: t.id,
              date: t.date,
              type: t.type as any,
              amount: t.amount,
              description: `${t.member_name} - ${t.description}`,
              status: t.status as any
            }))}
            limit={8}
          />
        </div>

        {/* Right Column - Actions & Tools */}
        <div className="space-y-6">
          <QuickActions userRole="treasurer" />

          {/* Group Health */}
          <div className="bg-white rounded-2xl p-6 shadow border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Group Health</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-600">Attendance Rate</span>
                  <span className="text-sm font-bold text-gray-900">{dashboardData.group_summary.attendance_rate}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${dashboardData.group_summary.attendance_rate}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-gray-600">Collection Efficiency</span>
                  <span className="text-sm font-bold text-gray-900">
                    {Math.round((dashboardData.group_summary.total_members - dashboardData.group_summary.defaulters_count) / dashboardData.group_summary.total_members * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${Math.round((dashboardData.group_summary.total_members - dashboardData.group_summary.defaulters_count) / dashboardData.group_summary.total_members * 100)}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="pt-4 border-t border-gray-200">
                <div className="flex items-center space-x-2 text-gray-600">
                  <TrendingUp className="w-4 h-4" />
                  <span className="text-sm">Overall group health: Good</span>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  {dashboardData.group_summary.defaulters_count === 0 
                    ? "All members are up to date!" 
                    : `${dashboardData.group_summary.defaulters_count} member(s) need attention`}
                </p>
              </div>
            </div>
          </div>

          {/* Meeting Tools */}
          <div className="bg-white rounded-2xl p-6 shadow border border-gray-200">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Meeting Tools</h3>
            <div className="space-y-3">
              <button className="w-full bg-blue-50 text-blue-700 py-3 rounded-lg font-medium hover:bg-blue-100 transition-colors">
                Generate Meeting Report
              </button>
              <button className="w-full bg-green-50 text-green-700 py-3 rounded-lg font-medium hover:bg-green-100 transition-colors">
                Record Bulk Contributions
              </button>
              <button className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors">
                Download Member List
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TreasurerDashboard;

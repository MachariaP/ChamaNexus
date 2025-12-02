import React from 'react';
import { motion } from 'framer-motion';
import { 
  PlusCircle, 
  FileText, 
  Download, 
  Users, 
  Clock, 
  MessageSquare,
  CreditCard,
  CheckCircle,
  BarChart
} from 'lucide-react';

interface QuickActionsProps {
  userRole: 'member' | 'treasurer' | 'admin';
}

const QuickActions: React.FC<QuickActionsProps> = ({ userRole }) => {
  const memberActions = [
    {
      icon: <PlusCircle className="w-5 h-5" />,
      label: 'Make Contribution',
      description: 'Record your contribution',
      color: 'bg-blue-100 text-blue-600',
      path: '/dashboard/contribute'
    },
    {
      icon: <FileText className="w-5 h-5" />,
      label: 'Apply for Loan',
      description: 'Submit loan request',
      color: 'bg-green-100 text-green-600',
      path: '/dashboard/loans/apply'
    },
    {
      icon: <CreditCard className="w-5 h-5" />,
      label: 'Pay Fine',
      description: 'Settle overdue fines',
      color: 'bg-yellow-100 text-yellow-600',
      path: '/dashboard/fines'
    },
    {
      icon: <Download className="w-5 h-5" />,
      label: 'Download Statement',
      description: 'Get your statement',
      color: 'bg-purple-100 text-purple-600',
      path: '/dashboard/statement'
    }
  ];

  const treasurerActions = [
    {
      icon: <Users className="w-5 h-5" />,
      label: 'Record Contributions',
      description: 'Bulk record from meeting',
      color: 'bg-blue-100 text-blue-600',
      path: '/treasurer/contributions'
    },
    {
      icon: <CheckCircle className="w-5 h-5" />,
      label: 'Approve Loans',
      description: 'Review pending requests',
      color: 'bg-green-100 text-green-600',
      path: '/treasurer/loans'
    },
    {
      icon: <BarChart className="w-5 h-5" />,
      label: 'View Reports',
      description: 'Financial analytics',
      color: 'bg-purple-100 text-purple-600',
      path: '/treasurer/reports'
    },
    {
      icon: <MessageSquare className="w-5 h-5" />,
      label: 'Send Reminders',
      description: 'Notify defaulters',
      color: 'bg-red-100 text-red-600',
      path: '/treasurer/reminders'
    }
  ];

  const actions = userRole === 'member' ? memberActions : treasurerActions;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-6 shadow border border-gray-200"
    >
      <h3 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {actions.map((action, index) => (
          <motion.button
            key={index}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors text-left`}
          >
            <div className={`p-2 rounded-lg ${action.color}`}>
              {action.icon}
            </div>
            <div>
              <p className="font-medium text-gray-900">{action.label}</p>
              <p className="text-sm text-gray-500">{action.description}</p>
            </div>
          </motion.button>
        ))}
      </div>

      {userRole === 'member' && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm font-medium text-gray-900">Need Help?</p>
                <p className="text-xs text-gray-500">Contact your group treasurer</p>
              </div>
            </div>
            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
              Contact →
            </button>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default QuickActions;

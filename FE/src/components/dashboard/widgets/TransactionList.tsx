import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, ArrowDownRight, CheckCircle, Clock, XCircle } from 'lucide-react';

interface Transaction {
  id: string;
  date: string;
  type: 'contribution' | 'loan_payment' | 'loan_disbursement' | 'payout' | 'fine';
  amount: number;
  description: string;
  status: 'completed' | 'pending' | 'failed';
}

interface TransactionListProps {
  transactions: Transaction[];
  limit?: number;
}

const TransactionList: React.FC<TransactionListProps> = ({ transactions, limit = 10 }) => {
  const getTransactionIcon = (type: string) => {
    switch (type) {
      case 'contribution':
        return <ArrowDownRight className="w-5 h-5 text-green-600" />;
      case 'loan_payment':
        return <ArrowUpRight className="w-5 h-5 text-blue-600" />;
      case 'loan_disbursement':
        return <ArrowDownRight className="w-5 h-5 text-purple-600" />;
      case 'payout':
        return <ArrowUpRight className="w-5 h-5 text-yellow-600" />;
      case 'fine':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <ArrowUpRight className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString('en-KE', { day: 'numeric', month: 'short' });
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'contribution': return 'Contribution';
      case 'loan_payment': return 'Loan Payment';
      case 'loan_disbursement': return 'Loan Received';
      case 'payout': return 'Payout';
      case 'fine': return 'Fine';
      default: return type;
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-6 shadow border border-gray-200"
    >
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-gray-900">Recent Transactions</h3>
        <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
          View All →
        </button>
      </div>

      <div className="space-y-3">
        {transactions.slice(0, limit).map((transaction) => (
          <div
            key={transaction.id}
            className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gray-100 rounded-lg">
                {getTransactionIcon(transaction.type)}
              </div>
              <div>
                <p className="font-medium text-gray-900">
                  {getTypeLabel(transaction.type)}
                </p>
                <p className="text-sm text-gray-500">{transaction.description}</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className={`font-bold ${
                  transaction.type === 'payout' || transaction.type === 'loan_disbursement'
                    ? 'text-green-600'
                    : transaction.type === 'fine'
                    ? 'text-red-600'
                    : 'text-gray-900'
                }`}>
                  {transaction.type === 'payout' || transaction.type === 'loan_disbursement' ? '+' : '-'}
                  KES {transaction.amount.toLocaleString()}
                </p>
                <div className="flex items-center space-x-1 text-sm text-gray-500">
                  <span>{formatDate(transaction.date)}</span>
                  {getStatusIcon(transaction.status)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {transactions.length === 0 && (
        <div className="text-center py-8">
          <div className="text-gray-400 mb-2">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p className="text-gray-500">No transactions yet</p>
          <p className="text-sm text-gray-400 mt-1">Your transactions will appear here</p>
        </div>
      )}
    </motion.div>
  );
};

export default TransactionList;

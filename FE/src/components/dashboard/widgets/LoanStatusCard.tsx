import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Calendar, CheckCircle } from 'lucide-react';

interface LoanStatusCardProps {
  loan: {
    amount_borrowed: number;
    amount_paid: number;
    remaining_balance: number;
    next_payment_date: string;
    next_payment_amount: number;
  };
}

const LoanStatusCard: React.FC<LoanStatusCardProps> = ({ loan }) => {
  const progress = (loan.amount_paid / loan.amount_borrowed) * 100;
  const nextPaymentDate = new Date(loan.next_payment_date);
  const today = new Date();
  const daysUntilPayment = Math.ceil((nextPaymentDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-200"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-green-100 rounded-lg">
            <TrendingUp className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">Loan Status</h3>
            <p className="text-sm text-gray-600">Active loan repayment</p>
          </div>
        </div>
        
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          daysUntilPayment <= 3 
            ? 'bg-red-100 text-red-800' 
            : 'bg-green-100 text-green-800'
        }`}>
          {daysUntilPayment <= 0 ? 'Due Now' : `${daysUntilPayment} days to payment`}
        </div>
      </div>

      <div className="space-y-6">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Repayment Progress</span>
            <span className="text-sm font-bold text-green-700">{progress.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className="bg-green-600 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm text-gray-500 mt-2">
            <span>KES {loan.amount_paid.toLocaleString()} paid</span>
            <span>KES {loan.amount_borrowed.toLocaleString()} total</span>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <p className="text-sm text-gray-600 mb-1">Remaining Balance</p>
            <p className="text-2xl font-bold text-gray-900">
              KES {loan.remaining_balance.toLocaleString()}
            </p>
          </div>
          
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <div className="flex items-center space-x-2 mb-1">
              <Calendar className="w-4 h-4 text-blue-600" />
              <p className="text-sm text-gray-600">Next Payment</p>
            </div>
            <p className="text-lg font-bold text-gray-900">
              {nextPaymentDate.toLocaleDateString('en-KE', { day: 'numeric', month: 'short' })}
            </p>
            <p className="text-sm text-gray-500">KES {loan.next_payment_amount.toLocaleString()}</p>
          </div>
          
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <div className="flex items-center space-x-2 mb-1">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <p className="text-sm text-gray-600">Completion</p>
            </div>
            <p className="text-lg font-bold text-gray-900">
              {Math.ceil((loan.remaining_balance / loan.next_payment_amount))} payments left
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button className="flex-1 bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition-colors">
            Make Payment
          </button>
          <button className="flex-1 border border-green-600 text-green-600 py-3 rounded-lg font-medium hover:bg-green-50 transition-colors">
            View Schedule
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default LoanStatusCard;

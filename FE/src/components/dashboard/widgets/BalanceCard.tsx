import React from 'react';
import { motion } from 'framer-motion';

interface BalanceCardProps {
  title: string;
  amount: number;
  currency: string;
  trend?: string;
  subtitle?: string;
  icon?: 'wallet' | 'users' | 'bank' | 'coins';
}

const BalanceCard: React.FC<BalanceCardProps> = ({
  title,
  amount,
  currency,
  trend,
  subtitle,
  icon = 'wallet'
}) => {
  const iconMap = {
    wallet: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
    ),
    users: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5 3.75l-3.75 3.75-1.5-1.5" />
      </svg>
    ),
    bank: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
      </svg>
    ),
    coins: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    )
  };

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-xl p-6 shadow border border-gray-200 hover:shadow-md transition-shadow"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-900">{title}</h3>
        <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
          {iconMap[icon]}
        </div>
      </div>
      
      <div className="mb-2">
        <p className="text-3xl font-bold text-gray-900">
          {currency} {amount.toLocaleString()}
        </p>
        {subtitle && (
          <p className="text-sm text-gray-600 mt-1">{subtitle}</p>
        )}
      </div>
      
      {trend && (
        <div className="flex items-center">
          <svg className="w-4 h-4 text-green-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
          <span className="text-sm text-green-600 font-medium">{trend}</span>
        </div>
      )}
    </motion.div>
  );
};

export default BalanceCard;

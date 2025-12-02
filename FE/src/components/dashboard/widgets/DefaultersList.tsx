import React from 'react';
import { motion } from 'framer-motion';
import { Phone, AlertCircle, Clock } from 'lucide-react';

interface Defaulter {
  id: string;
  name: string;
  phone: string;
  amount: number;
  days_overdue: number;
  last_contribution: string;
}

interface DefaultersListProps {
  defaulters: Defaulter[];
}

const DefaultersList: React.FC<DefaultersListProps> = ({ defaulters }) => {
  const formatPhone = (phone: string) => {
    return phone.replace(/(\d{3})(\d{3})(\d{4})/, '$1 $2 $3');
  };

  const getSeverityColor = (days: number) => {
    if (days >= 30) return 'text-red-600 bg-red-50 border-red-200';
    if (days >= 15) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-yellow-600 bg-yellow-50 border-yellow-200';
  };

  const getSeverityLabel = (days: number) => {
    if (days >= 30) return 'Critical';
    if (days >= 15) return 'High';
    return 'Moderate';
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-6 shadow border border-gray-200"
    >
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-red-100 rounded-lg">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">Defaulters ({defaulters.length})</h3>
            <p className="text-sm text-gray-600">Members with overdue contributions</p>
          </div>
        </div>
        <button className="text-red-600 hover:text-red-800 text-sm font-medium">
          Send Reminders
        </button>
      </div>

      <div className="space-y-4">
        {defaulters.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-green-400 mb-2">
              <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-gray-700 font-medium">All members are up to date! 🎉</p>
            <p className="text-sm text-gray-500 mt-1">No defaulters at the moment</p>
          </div>
        ) : (
          defaulters.map((defaulter) => (
            <div
              key={defaulter.id}
              className={`flex flex-col md:flex-row md:items-center justify-between p-4 rounded-lg border ${getSeverityColor(defaulter.days_overdue)}`}
            >
              <div className="mb-3 md:mb-0">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-700 font-bold">
                    {defaulter.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{defaulter.name}</p>
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Phone className="w-3 h-3" />
                      <span>{formatPhone(defaulter.phone)}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-col md:items-end space-y-2">
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-lg font-bold text-gray-900">
                      KES {defaulter.amount.toLocaleString()}
                    </p>
                    <div className="flex items-center space-x-1 text-sm text-gray-500">
                      <Clock className="w-3 h-3" />
                      <span>{defaulter.days_overdue} days overdue</span>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-bold ${getSeverityColor(defaulter.days_overdue)}`}>
                    {getSeverityLabel(defaulter.days_overdue)}
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                    Call
                  </button>
                  <button className="text-sm text-green-600 hover:text-green-800 font-medium">
                    Message
                  </button>
                  <button className="text-sm text-red-600 hover:text-red-800 font-medium">
                    Mark Paid
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {defaulters.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex justify-between items-center text-sm text-gray-600">
            <span>Last updated: {new Date().toLocaleTimeString('en-KE')}</span>
            <span>Total overdue: KES {defaulters.reduce((sum, d) => sum + d.amount, 0).toLocaleString()}</span>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default DefaultersList;

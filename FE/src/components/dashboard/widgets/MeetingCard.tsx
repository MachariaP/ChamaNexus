import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, MapPin, Clock, Users } from 'lucide-react';

interface MeetingCardProps {
  meeting: {
    date: string;
    time: string;
    location: string;
    agenda: string;
    my_position: number;
    total_positions: number;
  };
}

const MeetingCard: React.FC<MeetingCardProps> = ({ meeting }) => {
  const meetingDate = new Date(meeting.date);
  const today = new Date();
  const daysUntilMeeting = Math.ceil((meetingDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl p-6 shadow border border-gray-200"
    >
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4">
        <h3 className="text-xl font-bold text-gray-900">Next Meeting</h3>
        <div className={`px-3 py-1 rounded-full text-sm font-medium mt-2 md:mt-0 ${
          daysUntilMeeting <= 1 
            ? 'bg-red-100 text-red-800' 
            : daysUntilMeeting <= 3 
            ? 'bg-yellow-100 text-yellow-800'
            : 'bg-green-100 text-green-800'
        }`}>
          {daysUntilMeeting === 0 ? 'Today' : daysUntilMeeting === 1 ? 'Tomorrow' : `${daysUntilMeeting} days to go`}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <Calendar className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Date</p>
              <p className="font-medium text-gray-900">
                {meetingDate.toLocaleDateString('en-KE', {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <Clock className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Time</p>
              <p className="font-medium text-gray-900">{meeting.time}</p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <MapPin className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Location</p>
              <p className="font-medium text-gray-900">{meeting.location}</p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <Users className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">My Position</p>
              <p className="font-medium text-gray-900">
                #{meeting.my_position} of {meeting.total_positions}
              </p>
              {meeting.my_position === 1 && (
                <p className="text-sm text-green-600 font-medium mt-1">🎉 You're next in line!</p>
              )}
            </div>
          </div>

          <div>
            <p className="text-sm text-gray-600 mb-2">Agenda</p>
            <p className="text-gray-900 bg-gray-50 rounded-lg p-3">
              {meeting.agenda || "Monthly contributions and financial review"}
            </p>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-200">
        <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
          Confirm Attendance
        </button>
        <p className="text-sm text-gray-500 text-center mt-2">
          Please confirm by {meetingDate.toLocaleDateString('en-KE', { day: 'numeric', month: 'short' })}
        </p>
      </div>
    </motion.div>
  );
};

export default MeetingCard;

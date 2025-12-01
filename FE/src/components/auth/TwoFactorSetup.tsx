import React, { useState } from 'react';
import QRCode from 'qrcode.react';

interface TwoFactorSetupProps {
  onSetupComplete: () => void;
  onCancel: () => void;
}

const TwoFactorSetup: React.FC<TwoFactorSetupProps> = ({ onSetupComplete, onCancel }) => {
  const [step, setStep] = useState<'setup' | 'verify'>('setup');
  const [qrCodeData, setQrCodeData] = useState('');
  const [secret, setSecret] = useState('');
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSetup = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/v1/accounts/2fa/setup/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
        },
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setQrCodeData(data.qr_code);
        setSecret(data.secret);
        setStep('verify');
      } else {
        setError(data.error || 'Failed to setup 2FA');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerify = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/v1/accounts/2fa/verify/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('auth_token')}`,
        },
        body: JSON.stringify({ token }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        onSetupComplete();
      } else {
        setError(data.error || 'Invalid token');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  if (step === 'setup') {
    return (
      <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Setup Two-Factor Authentication</h2>
        <p className="mb-4 text-gray-600">
          Two-factor authentication adds an extra layer of security to your account.
        </p>
        <button
          onClick={handleSetup}
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? 'Setting up...' : 'Start Setup'}
        </button>
        <button
          onClick={onCancel}
          className="w-full mt-2 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
        >
          Cancel
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Verify Two-Factor Authentication</h2>
      
      <div className="mb-4">
        <p className="mb-2">Scan this QR code with your authenticator app:</p>
        <div className="flex justify-center mb-4">
          {qrCodeData && <QRCode value={qrCodeData} size={200} />}
        </div>
        <p className="text-sm text-gray-600 mb-2">
          Or enter this secret manually:
        </p>
        <code className="block p-2 bg-gray-100 rounded text-sm mb-4">
          {secret}
        </code>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">
          Enter 6-digit code from your app:
        </label>
        <input
          type="text"
          value={token}
          onChange={(e) => setToken(e.target.value.replace(/\D/g, '').slice(0, 6))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="000000"
          maxLength={6}
        />
      </div>

      <button
        onClick={handleVerify}
        disabled={isLoading || token.length !== 6}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Verifying...' : 'Verify & Enable'}
      </button>
      
      <button
        onClick={() => setStep('setup')}
        className="w-full mt-2 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
      >
        Back
      </button>
    </div>
  );
};

export default TwoFactorSetup;

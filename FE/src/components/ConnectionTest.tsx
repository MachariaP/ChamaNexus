import { useEffect, useState } from 'react';
import api from '../services/api';

const ConnectionTest = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const testConnection = async () => {
      try {
        const response = await api.get('/health/'); // Create this endpoint
        setData(response.data);
      } catch (err) {
        setError('Connection failed');
      }
    };
    testConnection();
  }, []);

  return (
    <div>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

// Responsible for processing uploaded data display and pattern matching replacement functions.

import React, { useState } from 'react';
import api from '../api';

function DataProcessor({ fileData }) {
  const [pattern, setPattern] = useState('');
  const [replacement, setReplacement] = useState('');
  const [processedData, setProcessedData] = useState('');

  const handleProcessData = async () => {
    try {
      const response = await api.post('/process-data', {
        pattern,
        replacement,
        data: fileData,
      });
      setProcessedData(response.data);
    } catch (error) {
      console.error('Error processing data:', error);
      alert('Error processing data');
    }
  };

  return (
    <div>
      <input type="text" placeholder="Enter pattern" value={pattern} onChange={(e) => setPattern(e.target.value)} />
      <input type="text" placeholder="Enter replacement" value={replacement} onChange={(e) => setReplacement(e.target.value)} />
      <button onClick={handleProcessData}>Process Data</button>
      <div dangerouslySetInnerHTML={{ __html: processedData }} />
    </div>
  );
}

export default DataProcessor;
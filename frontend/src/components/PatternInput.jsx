import React, { useState } from 'react';
import api from '../api';

function PatternInput({ fileData, onProcessData }) {
  const [patternDescription, setPatternDescription] = useState('');

  const handleProcess = async () => {
    if (!patternDescription.trim()) {
      alert('Please enter a description.');
      return;
    }

    try {
      const response = await api.post('/process-data/', {
        patternDescription,
        fileData
      });
    //   onProcessData(response.data.html_data);  // Assume 'response.data' contains the HTML data you want to display
      onProcessData(response.data);
    } catch (error) {
      console.error('Error processing data:', error);
      alert('Failed to process data');
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Describe what you want to find and replace"
        value={patternDescription}
        onChange={e => setPatternDescription(e.target.value)}
      />
      <button onClick={handleProcess}>Process Data</button>
    </div>
  );
}

export default PatternInput;

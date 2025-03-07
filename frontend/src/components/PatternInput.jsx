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
      alert('Failed to process data. Please check the internet connection or try again later');
    }
  };

  return (
    <div className="mt-4">
      <input
        type="text"
        placeholder="Describe your need for data processing."
        value={patternDescription}
        onChange={e => setPatternDescription(e.target.value)}
        className="p-2 border bg-black border-gray-300 rounded-md w-80"
      />
      <button 
        onClick={handleProcess} 
        className="ml-2 p-2 bg-green-500 text-white rounded-md hover:bg-green-700 transition-colors"
      >
        Process Data
      </button>
    </div>
  );
}

export default PatternInput;

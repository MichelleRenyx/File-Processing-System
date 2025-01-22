// Responsible for the file upload function.

import React, { useState } from 'react';
import api from '../api';

function FileUploader({ onFileUpload }) {
  const [file, setFile] = useState(null);

  // const handleFileChange = (event) => {
  //   setFile(event.target.files[0]);
  // };
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && (file.name.endsWith('.csv') || file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
        setFile(file);
    } else {
        alert('Please upload a .csv or .xlsx file.');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onFileUpload(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('File type is not supported. Please upload a .xlsx/.csv file.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex justify-center items-center space-x-4 mt-4">
      <input 
        type="file" 
        onChange={handleFileChange} 
        className="p-2 border border-gray-300 rounded-md" 
      />
      <button 
        type="submit" 
        className="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-700 transition-colors"
      >
        Upload File
      </button>
    </form>
  );
}

export default FileUploader;
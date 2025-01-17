import React from 'react';


function DownloadComponent({ onDownload }) {
  return (
    <div className="mt-4">
      <button 
        onClick={onDownload} 
        className="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-700 transition-colors"
      >
        Download Processed Data
      </button>
    </div>
  );
}

export default DownloadComponent;
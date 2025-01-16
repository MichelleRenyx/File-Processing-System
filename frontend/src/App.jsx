import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import DataProcessor from './components/DataProcessor';
import PatternInput from './components/PatternInput';
import DownloadComponent from './components/DownloadComponent';
import './styles/App.css';

function App() {
  const [htmlData, setHtmlData] = useState('');
  const [fileData, setFileData] = useState('');
  const [processedHtmlData, setProcessedHtmlData] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');
  
  const handleFileUpload = responseData => {
    setHtmlData(responseData.data);
    setFileData(responseData.data); // save the file data for pattern processing
  };

  const handleProcessData = responseData => {
    setProcessedHtmlData(responseData.html_data); // Update HTML data with processed results
    setDownloadUrl(responseData.download_url);
  };


  const handleDownload = () => {
    if (downloadUrl) {
      window.open(downloadUrl, '_blank');
    } else {
      alert('Download URL is missing.');
    }
  };
  

return (
  <div className="App">
      <h1>Upload and Process Files</h1>
      <FileUploader onFileUpload={handleFileUpload} />
      {htmlData && (
        <>
          <h2>Original Data</h2>
          <DataProcessor htmlData={htmlData} /> {/* Display the original uploaded data */}
        </>
      )}
      {fileData && <PatternInput fileData={fileData} onProcessData={handleProcessData} />}
      {processedHtmlData && (
        <>
          <h2>Processed Data</h2>
          <DataProcessor htmlData={processedHtmlData} /> {/* Display the processed data */}
          <DownloadComponent onDownload={handleDownload} />
        </>
      )}
  </div>
);

}

export default App;
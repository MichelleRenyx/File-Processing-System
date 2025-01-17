import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import DataProcessor from './components/DataProcessor';
import PatternInput from './components/PatternInput';
import DownloadComponent from './components/DownloadComponent';
// import './styles/App.css';

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
  <div className="App p-6 text-center bg-gray-100">
    <h1 className="text-2xl font-bold mb-4">Upload and Process Files</h1>
    <FileUploader onFileUpload={handleFileUpload} />
    {htmlData && (
      <>
        <h2 className="text-xl font-semibold mt-6">Original Data</h2>
        <DataProcessor htmlData={htmlData} />
      </>
    )}
    {fileData && <PatternInput fileData={fileData} onProcessData={handleProcessData} />}
    {processedHtmlData && (
      <>
        <h2 className="text-xl font-semibold mt-6">Processed Data</h2>
        <DataProcessor htmlData={processedHtmlData} />
        <DownloadComponent onDownload={handleDownload} />
      </>
    )}
  </div>
);
}

export default App;
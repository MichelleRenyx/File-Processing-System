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
  <div className="App bg-gradient-to-r from-blue-900 via-blue-800 to-blue-700  min-h-screen p-6 text-center text-white overflow-y-auto">
    <h1 className="text-4xl font-bold mb-6">
      Hands Off <span className="text-teal-300"><span className="typing-effect-wrapper"><span className="typing-effect">Data Processment</span></span></span>
    </h1>
    <p className="text-xl mb-8">
      Say goodbye to data chaos and hello to precision with our AI-powered data
      cleaning platform. 
    </p>
    <p className="text-lg text-yellow-100">
      Supported file type: .xlsx/.csv
    </p>

    <FileUploader onFileUpload={handleFileUpload} />

    {htmlData && (
      <>
        <h2 className="text-2xl font-semibold mt-6">Original Data</h2>
        <DataProcessor htmlData={htmlData} />
      </>
    )}

    {fileData && <PatternInput fileData={fileData} onProcessData={handleProcessData} />}

    {processedHtmlData && (
      <>
        <h2 className="text-2xl font-semibold mt-6">Processed Data</h2>
        <DataProcessor htmlData={processedHtmlData} />
        <div className="mt-6">
          <DownloadComponent onDownload={handleDownload} />
        </div>
      </>
    )}

    <div className="bg-blue-800 p-6 text-center text-white rounded-lg shadow-lg mt-6">
      <h2 className="text-3xl font-semibold mb-4">No-Code Platform</h2>
      <p className="text-lg">
        Transform raw, messy data into clean, high-quality datasets without
        writing a single line of code. Run various transformation modules and
        obtain analytics-ready formats.
      </p>
    </div>
  </div>
);
}

export default App;
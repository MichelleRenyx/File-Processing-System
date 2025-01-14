import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import DataProcessor from './components/DataProcessor';
import './styles/App.css';

function App() {
  const [fileData, setFileData] = useState('');

  return (
    <div className="App">
      <h1>Upload and Process Files</h1>
      <FileUploader onFileUpload={setFileData} />
      {fileData && <DataProcessor fileData={fileData} />}
    </div>
  );
}

export default App;
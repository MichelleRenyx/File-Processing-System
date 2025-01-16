import React from 'react';


function DownloadComponent({ onDownload }) {
    return (
      <div>
        <button onClick={onDownload}>Download Processed Data</button>
      </div>
    );
}

export default DownloadComponent;
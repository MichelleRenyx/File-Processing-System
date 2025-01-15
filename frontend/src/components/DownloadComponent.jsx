import React from 'react';

function DownloadComponent({ onDownload }) {
  return (
    <div>
      <button onClick={() => onDownload('csv')}>Download as CSV</button>
      <button onClick={() => onDownload('xlsx')}>Download as Excel</button>
    </div>
  );
}

export default DownloadComponent;
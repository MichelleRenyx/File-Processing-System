// Responsible for processing uploaded data display.

import React from 'react';


function DataProcessor({ htmlData }) {
  return (
      <div dangerouslySetInnerHTML={{ __html: htmlData }} />
  );
}


export default DataProcessor;
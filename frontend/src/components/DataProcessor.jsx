// Responsible for processing uploaded data display and pattern matching replacement functions.

import React from 'react';


function DataProcessor({ htmlData }) {
  return (
      <div dangerouslySetInnerHTML={{ __html: htmlData }} />
  );
}
export default DataProcessor;
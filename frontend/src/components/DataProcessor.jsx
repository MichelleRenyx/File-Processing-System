// Responsible for processing uploaded data display.

import React, { useEffect, useState } from 'react';

// Parsing HTML table data
const parseHTMLTableData = (htmlString) => {
  const table = document.createElement("table");
  table.innerHTML = htmlString; // insert the HTML string into the table element

  const rows = Array.from(table.querySelectorAll("tr")); // get all rows

  // get the header row
  const headerCells = Array.from(rows[0].querySelectorAll("th, td"));
  const header = headerCells.map((cell) => cell.textContent.trim());

  // parse the data rows
  const data = rows.slice(1).map((row) => {
    const cells = Array.from(row.querySelectorAll("td")); // get all cells in the row
    const rowData = {};

    // map the cells to the header
    header.forEach((col, index) => {
      rowData[col] = cells[index]?.textContent.trim() || ""; // if the cell is empty, use an empty string
    });

    return rowData;
  });

  return data;
};

function DataProcessor({ htmlData }) {
  const [parsedData, setParsedData] = useState([]);

  // Parsing HTML table data
  useEffect(() => {
    if (htmlData) {
      const parsed = parseHTMLTableData(htmlData); // Parsing HTML data
      setParsedData(parsed); // Store the parsed data in the state
    }
  }, [htmlData]);

  const renderTable = () => {
    if (parsedData.length === 0) return null; // If there is no data, the table will not be rendered.
    
    const headers = Object.keys(parsedData[0]); // Get the table header (inferred from the key name of the first data row)
    return (
      <table className="min-w-full table-auto border-collapse mt-4">
        <thead>
          <tr className="bg-blue-950 text-white">
            {headers.map((header, index) => (
              <th key={index} className="px-4 py-2 border-r border-white text-left">{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {parsedData.map((row, index) => (
            <tr
              key={index}
              className={`odd:bg-blue-900 even:bg-blue-950 hover:bg-blue-200`}
            >
              {headers.map((header, colIndex) => (
                <td key={colIndex} className="px-4 py-2 border-r border-white text-left">{row[header]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="overflow-x-auto bg-blue-950 rounded-lg shadow-lg mt-6">
      {renderTable()}
    </div>
  );
}




export default DataProcessor;
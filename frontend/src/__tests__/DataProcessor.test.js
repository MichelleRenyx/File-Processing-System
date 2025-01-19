import React from 'react';
import { render, screen } from '@testing-library/react';
import DataProcessor from 'frontend/src/components/DataProcessor.jsx';
import '@testing-library/jest-dom';

describe('DataProcessor', () => {
  beforeEach(() => {
    console.log('Running tests for DataProcessor');
  });

  test('renders parsed table data correctly', () => {
    const htmlData = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>John Doe</td>
            <td>john.doe@example.com</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Jane Smith</td>
            <td>jane.smith@example.com</td>
          </tr>
        </tbody>
      </table>
    `;
    console.log("htmlData in test:", htmlData);  // Debugging output

    render(<DataProcessor htmlData={htmlData} />);
    
    // Check that table headers are rendered correctly
    expect(screen.getByText(/id/i)).toBeInTheDocument();
    expect(screen.getByText(/name/i)).toBeInTheDocument();
    expect(screen.getByText(/email/i)).toBeInTheDocument();

    // Check that table rows are rendered correctly
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('jane.smith@example.com')).toBeInTheDocument();
  });

  test('does not render anything when htmlData is empty', () => {
    render(<DataProcessor htmlData="" />);

    const table = screen.queryByRole('table');
    expect(table).toBeNull();
  });
});

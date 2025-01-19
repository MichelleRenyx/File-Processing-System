import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DownloadComponent from 'frontend/src/components/DownloadComponent.jsx';
import '@testing-library/jest-dom';

describe('DownloadComponent', () => {
  test('calls onDownload when the button is clicked', () => {
    const mockOnDownload = jest.fn();
    render(<DownloadComponent onDownload={mockOnDownload} />);

    const button = screen.getByText(/download processed data/i);
    fireEvent.click(button);

    expect(mockOnDownload).toHaveBeenCalledTimes(1);
  });
});

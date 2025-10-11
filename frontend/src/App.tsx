/**
 * Main App Component
 * Story 1.1: Upload de Manuais Técnicos (PDF)
 * Combines DocumentUpload and PendingDocumentsList
 */
import React, { useState } from 'react';
import { DocumentUpload } from './components/documents/DocumentUpload';
import { PendingDocumentsList } from './components/documents/PendingDocumentsList';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    // Trigger refresh of pending list
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto">
        {/* Upload Section */}
        <DocumentUpload onUploadSuccess={handleUploadSuccess} />

        {/* Divider */}
        <div className="my-8 border-t border-gray-200"></div>

        {/* Pending Documents List */}
        <PendingDocumentsList refreshTrigger={refreshTrigger} />
      </div>
    </div>
  );
}

export default App;

import React, { useEffect, useState } from "react";
import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import ChatSection from "@/components/ChatSection";
import SheetSelector from "@/components/SheetSelector";
import { useExcelChat } from "@/hooks/useExcelChat";
import HtmlView from "@/components/HtmlView";

const Home: React.FC = () => {
  const {
    file: excelFile,
    fileMetadata,
    messages,
    isLoading,
    inputMessage,
    setInputMessage,
    handleSendMessage,
    handleRemoveFile: handleRemoveExcelFile,
    handleFileUpload: handleExcelFileUpload,
    handleExampleQuery,
    handleSelectSheet,
    isProcessingFile,
  } = useExcelChat();

  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<Array<{ name: string, url: string, type: 'csv' | 'excel' }>>([]);
  const [showHtml, setShowHtml] = useState(false);
  const [currentUrl, setCurrentUrl] = useState<string>();
  const [businessRules, setBusinessRules] = useState<string>(() => {
    // Try to load from localStorage if available
    return localStorage.getItem('business_rules') || 
      'The dataset does not include a ready-made "Parent Equity" column:\n- Value in Parent Equity = Value in column Owner Equity - Value in column Minority Interests.';
  });

  // Save business rules to localStorage when they change
  useEffect(() => {
    localStorage.setItem('business_rules', businessRules);
  }, [businessRules]);

  const handleExcelUpload = (file: File | null) => {
    if (file) {
      const url = URL.createObjectURL(file);
      setUploadedFiles(prev => [{ name: file.name, url, type: 'excel' }, ...prev]);
      handleExcelFileUpload(file);
    }
  };

  const handleCsvUpload = (file: File | null) => {
    if (file) {
      const url = URL.createObjectURL(file);
      setUploadedFiles(prev => [{ name: file.name, url, type: 'csv' }, ...prev]);
      setCsvFile(file);
      handleExcelFileUpload(file);
    }
  };

  const handleRemoveCsvFile = () => {
    if (csvFile) {
      setUploadedFiles(prev => prev.filter(f => f.name !== csvFile.name));
      setCsvFile(null);
    }
  };

  const handleViewFile = (url: string, type: 'csv' | 'excel') => {
    if (type === 'csv') {
      // Open CSV files in new tab
      window.open(url, '_blank');
    }
  };

  const handleCloseHtml = () => {
    setShowHtml(false);
    setCurrentUrl(undefined);
  };

  const handleSheetSelect = (fileId: string, sheetName: string) => {
    handleSelectSheet?.(sheetName);
  };

  const enhanceAndSendMessage = () => {
    // Get the message from inputMessage state
    const message = inputMessage;
    
    // Include business rules in the system prompt if defined
    const enhancedMessage = businessRules.trim() 
      ? `[Business Rules and Definitions: ${businessRules}]\n\n${message}`
      : message;
    
    // Set the input message to the enhanced version and send
    setInputMessage(enhancedMessage);
    handleSendMessage();
  };

  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.link && lastMessage.role === 'assistant') {
      setShowHtml(true);
      setCurrentUrl(messages[messages.length - 1].link || undefined);
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <Header />
      <main className="flex-1 flex flex-col md:flex-row overflow-hidden">
        <Sidebar
          excelFile={excelFile}
          csvFile={csvFile}
          fileMetadata={fileMetadata}
          onExcelUpload={handleExcelUpload}
          onCsvUpload={handleCsvUpload}
          onRemoveExcelFile={handleRemoveExcelFile}
          onRemoveCsvFile={handleRemoveCsvFile}
          onExampleQuery={handleExampleQuery}
          isProcessingFile={isProcessingFile}
          uploadedFiles={uploadedFiles}
          onViewFile={handleViewFile}
          businessRules={businessRules}
          setBusinessRules={setBusinessRules}
        />
        <div className="flex-1 flex flex-col overflow-hidden">
          {excelFile && fileMetadata && (
            <div className="px-4 pt-2">
              <SheetSelector
                file={excelFile}
                fileMetadata={fileMetadata}
                onSheetSelect={handleSheetSelect}
                isDisabled={isLoading || isProcessingFile}
              />
            </div>
          )}
          <div className="flex h-full">
            <div className="flex-1 flex justify-center">
              <ChatSection
                messages={messages}
                isLoading={isLoading}
                inputMessage={inputMessage}
                setInputMessage={setInputMessage}
                onSendMessage={enhanceAndSendMessage}
                fileUploaded={!!excelFile}
                isProcessingFile={isProcessingFile}
                isMinimized={showHtml}
                setShowHtml={setShowHtml}
                setCurrentUrl={setCurrentUrl}
              />
            </div>
            {showHtml && (
              <HtmlView
                url={currentUrl}
                onClose={handleCloseHtml}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;

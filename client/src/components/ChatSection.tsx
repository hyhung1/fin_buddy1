import React, { useRef, useEffect, useState } from "react";
import { Chrome, UserIcon, Send, X } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  fileAnalysis?: any;
  link?: string | null;
  images?: string[];
}

interface ChatSectionProps {
  messages: ChatMessage[];
  isLoading: boolean;
  inputMessage: string;
  setInputMessage: (message: string) => void;
  onSendMessage: () => void;
  fileUploaded: boolean;
  isProcessingFile: boolean;
  isMinimized: boolean;
  setShowHtml: (show: boolean) => void;
  setCurrentUrl: (url: string) => void;
}

// Full-size image modal component
const ImageModal: React.FC<{ image: string; onClose: () => void }> = ({ image, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 z-50 flex justify-center items-center p-4" onClick={onClose}>
      <div className="relative max-w-[90vw] max-h-[90vh]">
        <button 
          className="absolute top-2 right-2 bg-white rounded-full p-1 shadow-lg"
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
        >
          <X className="w-6 h-6" />
        </button>
        <img src={image} alt="Full size visualization" className="max-w-full max-h-[90vh] object-contain" />
      </div>
    </div>
  );
};

const ChatSection: React.FC<ChatSectionProps> = ({
  messages,
  isLoading,
  inputMessage,
  setInputMessage,
  onSendMessage,
  fileUploaded,
  isProcessingFile,
  isMinimized,
  setShowHtml,
  setCurrentUrl
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [fullSizeImage, setFullSizeImage] = useState<string | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSendMessage();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSendMessage();
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputMessage(e.target.value);

    // Auto-resize the textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  };

  const renderTableFromData = (data: any) => {
    if (!data || !Array.isArray(data.headers) || !data.rows || !Array.isArray(data.rows)) {
      return null;
    }

    return (
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-neutral-200 mb-4">
          <thead>
            <tr className="bg-neutral-100">
              {data.headers.map((header: string, index: number) => (
                <th key={index} className="py-2 px-4 border-b text-center text-sm font-medium text-neutral-700" style={{verticalAlign: 'middle'}}>
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.rows.map((row: any[], rowIndex: number) => (
              <tr key={rowIndex} className={rowIndex % 2 === 1 ? "bg-neutral-50" : ""}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} className="py-2 px-4 border-b text-sm text-neutral-800 text-center" style={{verticalAlign: 'middle'}}>
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderMessageContent = (message: ChatMessage) => {
    // 1️⃣  Generic "Label: number" pattern (e.g. "Banks: 736043.33")
    const financialTablePattern = /^([\w\s&]+):\s+([0-9,.]+(\.[0-9]+)?)/;
    // 2️⃣  "Ticker: XXX, ... : number" pattern (e.g. "Ticker: PLX, Total Net Profit … : 14032.41")
    const tickerPattern = /^Ticker:\s*([A-Za-z0-9.-]+),.*?:\s*([0-9,.]+(?:\.[0-9]+)?)$/;
    let tableData = null;
    
    // Check if the content contains multiple lines with the pattern "Something: number"
    // which would indicate financial data that should be displayed as a table
    const lineArr = message.content.split('\n');
    const genericMatches = lineArr.filter(line => financialTablePattern.test(line)).length;
    const tickerMatches  = lineArr.filter(line => tickerPattern.test(line)).length;
    const hasFinancialData = (genericMatches + tickerMatches) >= 3;
    
    if (hasFinancialData || message.content.includes("Net Profit") || message.content.includes("Total Net Profit")) {
      const rows: { sector: string; value: string }[] = [];
      let tableTitle = "";
      
      // Try to extract meaningful title from message content
      // First check for standard Net Profit format
      let titleMatch = message.content.match(/(Net Profit|Total Net Profit).*(\([0-9]{4}-[0-9]{4}\)):/);
      
      // If that doesn't work, look for "Top X sectors" or similar text at the beginning
      if (!titleMatch) {
        titleMatch = message.content.match(/^(Top \d+ sectors.*?(from|for|in|with).*?\d{4}.*?\d{4})/m);
      }
      
      // If we found a title, use it
      if (titleMatch) {
        tableTitle = titleMatch[0].replace(/:\s*$/, ''); // Remove trailing colon if present
      } else if (hasFinancialData) {
        // If no specific title but we have financial data, use a generic title
        tableTitle = "Financial Results";
      }
      
      // Extract rows with financial data - use regex.exec instead of test to avoid resetting lastIndex
      for (const line of lineArr) {
        let match = line.match(financialTablePattern);
        if (match) {
          rows.push({ sector: match[1].trim(), value: match[2].trim() });
          continue;
        }
        match = line.match(tickerPattern);
        if (match) {
          rows.push({ sector: match[1].trim(), value: match[2].trim() });
        }
      }
      
      // If we found rows, create a table
      if (rows.length > 0) {
        // Check if sectors are years (numeric values)
        const hasYearSectors = rows.some(row => /^\d{4}$/.test(row.sector));
        
        // Determine left-hand column label
        const firstHeader = hasYearSectors ? 'Year' : (tickerMatches > 0 ? 'Ticker' : 'Sector');
        
        tableData = (
          <div className="my-1 flex flex-col lg:flex-row gap-4">
            {/* Table section - full width on mobile, left side on desktop */}
            <div className="lg:w-[30%] w-full bg-white rounded-lg overflow-hidden border border-neutral-300 shadow-sm">
              {tableTitle && (
                <div className="text-center p-1 font-semibold bg-neutral-100 border-b text-sm">{tableTitle}</div>
              )}
              <Table className="border-collapse w-full border-neutral-300">
                <TableHeader>
                  <TableRow className="divide-x divide-neutral-300">
                    <TableHead className={`py-2 px-2 text-center border-b border-neutral-300`} style={{width: '40%', verticalAlign: 'middle'}}>
                      {firstHeader}
                    </TableHead>
                    <TableHead className="text-center py-2 px-4 border-b border-neutral-300" style={{width: '60%', verticalAlign: 'middle'}}>
                      <div className="flex flex-col items-center">
                        <span>Value</span>
                        <span>(billion VND)</span>
                      </div>
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody className="max-h-[300px] overflow-hidden relative">
                  {rows.length > 10 ? (
                    <>
                      <div className="max-h-[300px] overflow-hidden" id={`table-content-${tableTitle.replace(/\s+/g, '-').toLowerCase()}`}>
                        {rows.slice(0, 10).map((row, index) => (
                          <TableRow key={index} className="divide-x divide-neutral-300">
                            <TableCell className={`py-3 px-4 border-b border-neutral-300 ${hasYearSectors ? 'text-center' : 'text-center font-medium'}`} style={{width: '40%', verticalAlign: 'middle'}}>
                              {row.sector}
                            </TableCell>
                            <TableCell className="text-center py-3 px-4 border-b border-neutral-300 whitespace-normal break-words" style={{width: '60%', verticalAlign: 'middle'}}>
                              {row.value}
                            </TableCell>
                          </TableRow>
                        ))}
                      </div>
                      <div className="text-center py-2">
                        <button 
                          className="text-primary text-sm hover:underline focus:outline-none"
                          onClick={(e) => {
                            e.preventDefault();
                            const tableId = `table-content-${tableTitle.replace(/\s+/g, '-').toLowerCase()}`;
                            const tableContent = document.getElementById(tableId);
                            const expandButton = e.currentTarget;
                            
                            if (tableContent) {
                              if (tableContent.classList.contains("max-h-[300px]")) {
                                // Expand
                                tableContent.classList.remove("max-h-[300px]");
                                tableContent.classList.add("max-h-none");
                                expandButton.textContent = "Show less";
                                
                                // Update to show all rows
                                const tableBody = tableContent.parentElement;
                                if (tableBody) {
                                  tableContent.innerHTML = '';
                                  rows.forEach((row, idx) => {
                                    const tr = document.createElement('tr');
                                    tr.className = 'border-b divide-x divide-neutral-300';
                                    
                                    const td1 = document.createElement('td');
                                    td1.className = `py-3 px-4 ${hasYearSectors ? 'text-center' : 'text-center font-medium'} border-neutral-300`;
                                    td1.style.width = '40%';
                                    td1.style.verticalAlign = 'middle';
                                    td1.textContent = row.sector;
                                    
                                    const td2 = document.createElement('td');
                                    td2.className = 'text-center py-3 px-4 whitespace-normal break-words border-neutral-300';
                                    td2.style.width = '60%';
                                    td2.style.verticalAlign = 'middle';
                                    td2.textContent = row.value;
                                    
                                    tr.appendChild(td1);
                                    tr.appendChild(td2);
                                    tableContent.appendChild(tr);
                                  });
                                }
                              } else {
                                // Collapse
                                tableContent.classList.add("max-h-[300px]");
                                tableContent.classList.remove("max-h-none");
                                expandButton.textContent = "Show more...";
                                
                                // Reset to show first 10 rows
                                const tableBody = tableContent.parentElement;
                                if (tableBody) {
                                  tableContent.innerHTML = '';
                                  rows.slice(0, 10).forEach((row, idx) => {
                                    const tr = document.createElement('tr');
                                    tr.className = 'border-b divide-x divide-neutral-300';
                                    
                                    const td1 = document.createElement('td');
                                    td1.className = `py-3 px-4 ${hasYearSectors ? 'text-center' : 'text-center font-medium'} border-neutral-300`;
                                    td1.style.width = '40%';
                                    td1.style.verticalAlign = 'middle';
                                    td1.textContent = row.sector;
                                    
                                    const td2 = document.createElement('td');
                                    td2.className = 'text-center py-3 px-4 whitespace-normal break-words border-neutral-300';
                                    td2.style.width = '60%';
                                    td2.style.verticalAlign = 'middle';
                                    td2.textContent = row.value;
                                    
                                    tr.appendChild(td1);
                                    tr.appendChild(td2);
                                    tableContent.appendChild(tr);
                                  });
                                }
                              }
                            }
                          }}
                        >
                          Show more...
                        </button>
                      </div>
                    </>
                  ) : (
                    rows.map((row, index) => (
                      <TableRow key={index} className="divide-x divide-neutral-300">
                        <TableCell className={`py-3 px-4 border-b border-neutral-300 ${hasYearSectors ? 'text-center' : 'text-center font-medium'}`} style={{width: '40%', verticalAlign: 'middle'}}>
                          {row.sector}
                        </TableCell>
                        <TableCell className="text-center py-3 px-4 border-b border-neutral-300 whitespace-normal break-words" style={{width: '60%', verticalAlign: 'middle'}}>
                          {row.value}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
            
            {/* Visualization section - full width on mobile, right side on desktop */}
            {message.images && message.images.length > 0 && (
              <div className="lg:w-[70%] w-full overflow-hidden rounded-lg border-2 border-neutral-300 shadow-sm bg-white p-2">
                <div className="text-[9px] font-medium text-neutral-500 mb-0.5 px-1">Visualization</div>
                {message.images.length === 1 ? (
                  // Single image display (existing code)
                  <div className="relative border border-neutral-200 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48c3R5bGU+QGtleWZyYW1lcyBzcGluIHt0byB7dHJhbnNmb3JtOiByb3RhdGUoMzYwZGVnKX19PC9zdHlsZT48cGF0aCBkPSJNMTIgMjJjNS41MjMgMCAxMC00LjQ3NyAxMC0xMFMxNy41MjMgMiAxMiAyIDIgNi40NzcgMiAxMnM0LjQ3NyAxMCAxMCAxMHoiIHN0cm9rZT0iI0QyRDZEQyIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1kYXNoYXJyYXk9IjQwLDQwIiBzdHJva2UtZGFzaG9mZnNldD0iMTAwIiBzdHlsZT0idHJhbnNmb3JtLW9yaWdpbjogY2VudGVyOyBhbmltYXRpb246IHNwaW4gMXMgbGluZWFyIGluZmluaXRlOyI+PC9wYXRoPjwvc3ZnPg==')] bg-no-repeat bg-center bg-[length:40px_40px]">
                    <img 
                      src={message.images[0]} 
                      alt="Visualization" 
                      className="w-full h-auto max-h-[500px] cursor-pointer block"
                      onClick={() => message.images && setFullSizeImage(message.images[0])}
                      onError={(e) => {
                        // Handle image loading errors
                        const target = e.target as HTMLImageElement;
                        target.onerror = null; // Prevent infinite error loop
                        target.src = ''; // Clear the src
                        // Show error message
                        target.style.display = 'none';
                        const parent = target.parentNode as HTMLElement;
                        if (parent) {
                          const errorMsg = document.createElement('div');
                          errorMsg.className = 'text-red-500 text-sm py-4 px-2 text-center';
                          errorMsg.textContent = 'Unable to load visualization. The image may still be generating.';
                          parent.appendChild(errorMsg);
                        }
                      }}
                      onLoad={(e) => {
                        // Remove spinner background when image loads
                        const parent = (e.target as HTMLElement).parentNode as HTMLElement;
                        if (parent) {
                          parent.className = "relative border border-neutral-200";
                        }
                      }}
                    />
                  </div>
                ) : (
                  // Multiple images display with navigation
                  <div className="flex flex-col space-y-4">
                    {message.images.map((image, imgIndex) => (
                      <div key={imgIndex} className="relative border border-neutral-200 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48c3R5bGU+QGtleWZyYW1lcyBzcGluIHt0byB7dHJhbnNmb3JtOiByb3RhdGUoMzYwZGVnKX19PC9zdHlsZT48cGF0aCBkPSJNMTIgMjJjNS41MjMgMCAxMC00LjQ3NyAxMC0xMFMxNy41MjMgMiAxMiAyIDIgNi40NzcgMiAxMnM0LjQ3NyAxMCAxMCAxMHoiIHN0cm9rZT0iI0QyRDZEQyIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1kYXNoYXJyYXk9IjQwLDQwIiBzdHJva2UtZGFzaG9mZnNldD0iMTAwIiBzdHlsZT0idHJhbnNmb3JtLW9yaWdpbjogY2VudGVyOyBhbmltYXRpb246IHNwaW4gMXMgbGluZWFyIGluZmluaXRlOyI+PC9wYXRoPjwvc3ZnPg==')] bg-no-repeat bg-center bg-[length:40px_40px]">
                        <div className="absolute top-2 left-2 bg-black bg-opacity-50 text-white rounded-full px-2 py-1 text-xs z-10">
                          Image {imgIndex + 1} of {message.images?.length}
                        </div>
                        <img 
                          src={image} 
                          alt={`Visualization ${imgIndex + 1}`} 
                          className="w-full h-auto max-h-[500px] block cursor-pointer"
                          onClick={() => setFullSizeImage(image)}
                          onError={(e) => {
                            // Handle image loading errors
                            const target = e.target as HTMLImageElement;
                            target.onerror = null; // Prevent infinite error loop
                            target.src = ''; // Clear the src
                            // Show error message
                            target.style.display = 'none';
                            const parent = target.parentNode as HTMLElement;
                            if (parent) {
                              const errorMsg = document.createElement('div');
                              errorMsg.className = 'text-red-500 text-sm py-4 px-2 text-center';
                              errorMsg.textContent = 'Unable to load visualization. The image may still be generating.';
                              parent.appendChild(errorMsg);
                            }
                          }}
                          onLoad={(e) => {
                            // Remove spinner background when image loads
                            const parent = (e.target as HTMLElement).parentNode as HTMLElement;
                            if (parent) {
                              parent.className = "relative border border-neutral-200";
                            }
                          }}
                        />
                        <div className="absolute bottom-2 right-2 text-[9px] text-white bg-black bg-opacity-50 px-2 py-1 rounded-sm">
                          <button onClick={() => setFullSizeImage(image)} className="hover:underline">
                            Full size
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {message.images.length === 1 && (
                  <div className="text-[9px] text-neutral-400 text-right pr-1 mt-1">
                    <button onClick={() => message.images && setFullSizeImage(message.images[0])} className="hover:underline">
                      Click to view full size
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        );
        
        return (
          <>
            {tableData}
            {message.fileAnalysis && renderTableFromData(message.fileAnalysis.tableData)}
            {/* Suggested Questions - keep existing code */}
            {message.fileAnalysis && 
              message.fileAnalysis.suggestedQuestions && 
              message.fileAnalysis.suggestedQuestions.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium text-neutral-700 mb-2">Suggested questions:</p>
                <div className="flex flex-wrap gap-2">
                  {message.fileAnalysis.suggestedQuestions.map((question: string, index: number) => (
                    <button
                      key={index}
                      className="text-xs bg-neutral-100 hover:bg-neutral-200 text-neutral-800 py-1 px-3 rounded-full transition-colors"
                      onClick={() => handleSuggestedQuestionClick(question)}
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </>
        );
      }
    }
    
    // Default rendering if no financial table was detected
    const textContent = message.content.replace(/\n/g, "<br>"); 
    const hasTable = message.fileAnalysis && message.fileAnalysis.tableData;
    const hasSuggestedQuestions = message.fileAnalysis &&
      message.fileAnalysis.suggestedQuestions &&
      message.fileAnalysis.suggestedQuestions.length > 0;

    return (
      <>
        <div className="text-neutral-800 m-0" dangerouslySetInnerHTML={{ __html: textContent }}></div>
        {hasTable && renderTableFromData(message.fileAnalysis.tableData)}
        
        {/* Suggested Questions */}
        {hasSuggestedQuestions && (
          <div className="mt-2">
            <p className="text-sm font-medium text-neutral-700 mb-1">Suggested questions:</p>
            <div className="flex flex-wrap gap-2">
              {message.fileAnalysis.suggestedQuestions.map((question: string, index: number) => (
                <button
                  key={index}
                  className="text-xs bg-neutral-100 hover:bg-neutral-200 text-neutral-800 py-1 px-3 rounded-full transition-colors"
                  onClick={() => handleSuggestedQuestionClick(question)}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}
      </>
    );
  };

  const handleSuggestedQuestionClick = (question: string) => {
    setInputMessage(question);
    // Focus the textarea
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleMessageClick = (message: ChatMessage) => {
    if (message.link) {
      setShowHtml(true);
      setCurrentUrl(message.link);
    }
  };
  return (
    <div className={`h-full transition-all duration-700 ease-out ${isMinimized ? 'w-[98%]' : 'w-[95%]'}`}>
      {fullSizeImage && <ImageModal image={fullSizeImage} onClose={() => setFullSizeImage(null)} />}
      <section className={`h-full flex-1 flex flex-col overflow-hidden`} >
        <ScrollArea className="flex-1 py-2.5 space-y-2.5">
          {/* Message history */}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex items-start gap-2 max-w-4xl mx-auto py-1.5 ${message.link ? 'cursor-pointer' : ''} ${
                message.role === 'user' ? 'justify-end' : ''
              }`}
              onClick={() => handleMessageClick(message)}
            >
              {message.role === 'assistant' && (
                <div className="flex-shrink-0 mr-3">
                  <div className="w-9 h-9 rounded-full bg-primary flex items-center justify-center text-white">
                    <Chrome className="h-4.5 w-4.5" />
                  </div>
                </div>
              )}
              <div
                className={`rounded-lg p-3 max-w-[90%] border prose prose-sm whitespace-pre-wrap ${
                  message.role === 'user'
                    ? 'bg-white border-[#ececf1]'
                    : 'bg-[#f7f7f8] border-[#ececf1]'
                }`}
              >
                {message.role === 'user' ? (
                  <p className="whitespace-pre-wrap m-0">{message.content}</p>
                ) : (
                  renderMessageContent(message)
                )}
              </div>
              {message.role === 'user' && (
                <div className="flex-shrink-0 ml-3">
                  <div className="w-9 h-9 rounded-full bg-neutral-300 flex items-center justify-center text-neutral-600">
                    <UserIcon className="h-4.5 w-4.5" />
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start max-w-4xl mx-auto">
              <div className="flex-shrink-0 mr-3">
                <div className="w-9 h-9 rounded-full bg-primary flex items-center justify-center text-white">
                  <Chrome className="h-4.5 w-4.5" />
                </div>
              </div>
              <div className="bg-[#f7f7f8] rounded-lg p-3 border border-[#ececf1] max-w-[90%]">
                <div className="flex space-x-1">
                  <span className="dot bg-neutral-400 w-2 h-2 rounded-full animate-bounce"></span>
                  <span className="dot bg-neutral-400 w-2 h-2 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                  <span className="dot bg-neutral-400 w-2 h-2 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </ScrollArea>

        <div className="p-3 border-t border-neutral-200 bg-white">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="flex items-end gap-3">
              <div className="flex-1 relative">
                <Textarea
                  ref={textareaRef}
                  value={inputMessage}
                  onChange={handleTextareaChange}
                  onKeyDown={handleKeyDown}
                  className="w-full bg-[#f7f7f8] border border-[#ececf1] rounded-full px-4 py-3 pr-10 resize-none min-h-[44px] focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all shadow-sm hover:shadow-md scrollbar-hide"
                  placeholder={fileUploaded ? "Ask a question about your financial data..." : "Upload your data and ask anything about it"}
                  disabled={isProcessingFile || isLoading}
                  rows={1}
                  style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                />
              </div>
              <Button
                type="submit"
                className="bg-primary text-white px-4 py-3 rounded-full"
                disabled={!inputMessage.trim() || isLoading || isProcessingFile}
              >
                <Send className="h-5 w-5" />
              </Button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ChatSection;

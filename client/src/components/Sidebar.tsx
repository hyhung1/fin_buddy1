import React from "react";
import { FileAnalysis } from "@shared/schema";
import FileUpload from "./FileUpload";
import { CheckCircle, FileSpreadsheet, Eye, BookText, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface SidebarProps {
  excelFile: File | null;
  csvFile: File | null;
  fileMetadata: FileAnalysis | null;
  onExcelUpload: (file: File) => void;
  onCsvUpload: (file: File) => void;
  onRemoveExcelFile: () => void;
  onRemoveCsvFile: () => void;
  onExampleQuery: (query: string) => void;
  isProcessingFile: boolean;
  uploadedFiles: Array<{ name: string; url: string; type: 'csv' | 'excel' }>;
  onViewFile: (url: string, type: 'csv' | 'excel') => void;
  businessRules: string;
  setBusinessRules: (rules: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  excelFile,
  csvFile,
  fileMetadata,
  onExcelUpload,
  onCsvUpload,
  onRemoveExcelFile,
  onRemoveCsvFile,
  onExampleQuery,
  isProcessingFile,
  uploadedFiles,
  onViewFile,
  businessRules,
  setBusinessRules,
}) => {
  // Use suggested questions from metadata if available, otherwise use default examples
  const suggestedQuestions = fileMetadata?.suggestedQuestions || [];
  const exampleQueries = suggestedQuestions.length > 0
    ? suggestedQuestions
    : [
      "What are the total sales for Q2?",
      "Who is the top performing salesperson?",
      "Show me a breakdown of sales by region"
    ];

  return (
    <aside className="h-full overflow-auto w-full md:w-72 bg-white border-r border-neutral-200 flex flex-col">
      <div className="p-3 border-b border-neutral-200">
        <h2 className="text-base font-medium mb-3 text-neutral-800">Upload File</h2>
        <FileUpload
          onFileUpload={(file) => {
            const ext = file.name.split('.').pop()?.toLowerCase();
            if (ext === 'csv') {
              onCsvUpload(file);
            } else {
              onExcelUpload(file);
            }
          }}
          onRemoveFile={() => {
            if (excelFile) onRemoveExcelFile();
            if (csvFile) onRemoveCsvFile();
          }}
          acceptedFormats={['.xlsx', '.xls', '.csv']}
          maxFileSize={500}
        />
      </div>

      <div className="p-3 border-b border-neutral-200">
        <div className="flex items-center gap-2 mb-2">
          <FileSpreadsheet className="h-4 w-4 text-primary" />
          <h2 className="text-base font-medium text-neutral-800">Business Rules & Definitions</h2>
        </div>
        <p className="text-xs text-neutral-500 mb-2">
          Add your organization's business rules and definitions to improve analysis quality.
        </p>
        <Textarea
          placeholder="e.g., Revenue recognition rules, KPI definitions, accounting periods..."
          className="min-h-[160px] text-sm"
          value={businessRules}
          onChange={(e) => setBusinessRules(e.target.value)}
        />
      </div>
    </aside>
  );
};

export default Sidebar;

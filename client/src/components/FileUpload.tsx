import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { FileSpreadsheet, XIcon, AlertCircle, RefreshCw, CheckCircle } from "lucide-react";
import { formatFileSize } from "@/lib/utils";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface UploadedFile {
  file: File;
  status: "uploading" | "failed" | "complete";
  id: string;
}

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  onRemoveFile: (fileId: string) => void;
  onRetry?: (fileId: string) => void;
  acceptedFormats?: string[];
  maxFileSize?: number;
  multiple?: boolean;
  showDemoFiles?: boolean; // For demonstration purposes
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileUpload,
  onRemoveFile,
  onRetry,
  acceptedFormats = [".xlsx", ".xls", ".csv"],
  maxFileSize = 500, // 500KB
  multiple = false,
  showDemoFiles = false,
}) => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    setError(null);
    if (fileRejections.length > 0) {
      setError(`Invalid file type or size. Please upload ${acceptedFormats.join(', ')} files under ${maxFileSize}kb.`);
      return;
    }

    if (acceptedFiles.length === 0) return;

    const newFiles = acceptedFiles.map(file => ({
      file,
      status: "uploading" as const,
      id: Math.random().toString(36).substring(2, 9)
    }));

    setFiles(prev => multiple ? [...prev, ...newFiles] : newFiles);
    
    // Call the onFileUpload handler for each file
    acceptedFiles.forEach(file => onFileUpload(file));
    
    // Mark file upload as complete immediately
    // In a real application, this would happen after the server responds
    if (newFiles.length > 0) {
      setTimeout(() => {
        setFiles(prev => 
          prev.map(f => ({ ...f, status: "complete" }))
        );
      }, 800); // Short delay to simulate upload completion
    }
  }, [onFileUpload, acceptedFormats, maxFileSize, multiple]);

  const handleRemoveFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
    onRemoveFile(fileId);
  };

  const handleRetry = (fileId: string) => {
    const fileToRetry = files.find(f => f.id === fileId);
    if (fileToRetry) {
      setFiles(prev => 
        prev.map(f => f.id === fileId ? {...f, status: "uploading"} : f)
      );
      
      if (onRetry) {
        onRetry(fileId);
      } else {
        onFileUpload(fileToRetry.file);
      }
      
      // Mark as complete after a delay
      setTimeout(() => {
        setFiles(prev => 
          prev.map(f => f.id === fileId ? { ...f, status: "complete" } : f)
        );
      }, 800);
    }
  };

  const acceptConfig = acceptedFormats.reduce((acc, ext) => {
    if (ext === '.xlsx') {
      acc['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'] = ['.xlsx'];
    } else if (ext === '.xls') {
      acc['application/vnd.ms-excel'] = ['.xls'];
    } else if (ext === '.csv') {
      acc['text/csv'] = ['.csv'];
    }
    // Add more formats as needed
    return acc;
  }, {} as { [key: string]: string[] });

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptConfig,
    maxFiles: multiple ? undefined : 1,
    multiple: multiple,
    maxSize: maxFileSize * 1024, // Convert to bytes
  });

  return (
    <div className="space-y-3">
      <div
        {...getRootProps()}
        className={`border border-dashed ${
          isDragActive ? "border-green-500 bg-green-50" : "border-gray-300 bg-white hover:bg-gray-50"
        } rounded-lg p-4 flex flex-col items-center justify-center transition-colors cursor-pointer min-h-[140px]`}
      >
        <input {...getInputProps()} />
        <div className="mb-2 text-green-600">
          <FileSpreadsheet className="h-7 w-7" />
        </div>

        <p className="text-center text-gray-700 text-sm mb-1">
          <span className="font-medium">Drag & drop your files here</span>
        </p>
        <p className="text-center text-gray-700 text-sm mb-2">or</p>
        <button className="px-4 py-1.5 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors text-sm">
          Choose files
        </button>
        <p className="text-center text-gray-500 text-xs mt-2">
          Only {acceptedFormats.join(' and ')} files.
        </p>
      </div>
      
      <div>
        {files.length > 0 && <h3 className="font-medium text-sm mb-2">Uploaded Files</h3>}
        {files.length === 0 && !showDemoFiles ? (
          <p className="text-gray-500 text-sm">No files uploaded yet</p>
        ) : (
          <div className="space-y-2">
            {files.map((file) => (
              <div key={file.id} className="p-3 bg-white border rounded-md flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="bg-neutral-100 p-2 rounded">
                    <FileSpreadsheet className="h-5 w-5 text-neutral-500" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-neutral-800">{file.file.name}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <p className="text-xs text-neutral-500">
                        {(file.file.size / 1024 / 1024).toFixed(1)} MB
                        {file.status === "uploading" && " | Processing..."}
                        {file.status === "failed" && " | Upload failed"}
                      </p>
                      {file.status === "complete" && (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      )}
                      {file.status === "uploading" && (
                        <span className="text-xs text-neutral-500 animate-pulse">Uploading...</span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  {file.status === "failed" ? (
                    <button 
                      onClick={() => handleRetry(file.id)}
                      className="p-1.5 rounded-full hover:bg-neutral-100 text-neutral-500"
                    >
                      <RefreshCw className="h-4 w-4" />
                    </button>
                  ) : null}
                  <button 
                    onClick={() => handleRemoveFile(file.id)}
                    className="p-1.5 rounded-full hover:bg-neutral-100 text-neutral-500"
                  >
                    <XIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Demo files for visual representation - shown only when showDemoFiles is true */}
      {showDemoFiles && (
        <>
          <div className="mt-4">
            <h3 className="font-medium mb-2">Uploaded Files</h3>
            <div className="space-y-3">
              {/* Failed upload example */}
              <div className="p-4 bg-white border rounded-md flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="bg-neutral-100 p-2 rounded">
                    <FileSpreadsheet className="h-5 w-5 text-neutral-500" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-neutral-800">Universal-Icon-Set.jpg</p>
                    <p className="text-xs text-neutral-500">Upload failed</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="p-1.5 rounded-full hover:bg-neutral-100 text-neutral-500">
                    <RefreshCw className="h-4 w-4" />
                  </button>
                  <button className="p-1.5 rounded-full hover:bg-neutral-100 text-neutral-500">
                    <XIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              {/* Successful upload example */}
              <div className="p-4 bg-white border rounded-md flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="bg-neutral-100 p-2 rounded">
                    <FileSpreadsheet className="h-5 w-5 text-neutral-500" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-neutral-800">Quarterly-Report.xlsx</p>
                    <div className="flex items-center gap-2 mt-1">
                      <p className="text-xs text-neutral-500">2.4 MB</p>
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="p-1.5 rounded-full hover:bg-neutral-100 text-neutral-500">
                    <XIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {error && (
        <Alert variant="destructive" className="mt-4">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default FileUpload;

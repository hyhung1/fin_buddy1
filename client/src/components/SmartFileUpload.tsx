import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import { FileSpreadsheet, XIcon, CheckCircle, AlertCircle, Table } from "lucide-react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface SmartFileUploadProps {
  onSuccessfulUpload?: (data: any) => void;
}

const SmartFileUpload: React.FC<SmartFileUploadProps> = ({ 
  onSuccessfulUpload 
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const onDrop = (acceptedFiles: File[], fileRejections: any[]) => {
    setError(null);
    
    if (fileRejections.length > 0) {
      setError(`Invalid file type. Please upload an Excel or CSV file.`);
      return;
    }

    if (acceptedFiles.length === 0) return;

    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    maxFiles: 1,
    multiple: false,
    disabled: isLoading
  });

  const handleUpload = async () => {
    if (!file) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Call the smart upload endpoint
      const response = await axios.post('/api/upload_smart', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Set results
      setResult(response.data);
      
      // Call the callback if provided
      if (onSuccessfulUpload) {
        onSuccessfulUpload(response.data);
      }
      
      console.log("File processed with header detection:", response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
      console.error("Upload error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  const renderResults = () => {
    if (!result) return null;
    
    return (
      <Card className="mt-4">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-green-500" />
            File Processed Successfully
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium">File Information</p>
              <div className="flex flex-wrap gap-2 mt-1">
                <Badge variant="outline">{result.file_name}</Badge>
                <Badge variant="secondary">
                  Header Row: {typeof result.header_row === 'number' ? result.header_row + 1 : 'Unknown'}
                </Badge>
              </div>
            </div>
            
            <div>
              <p className="text-sm font-medium">Detected Columns</p>
              <div className="flex flex-wrap gap-1 mt-1">
                {result.columns && Array.isArray(result.columns) ? (
                  result.columns.map((column: string, index: number) => (
                    <Badge key={index} variant="outline" className="mt-1">
                      {column}
                    </Badge>
                  ))
                ) : (
                  <Badge variant="outline">No columns detected</Badge>
                )}
              </div>
            </div>
            
            <div>
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium">Sample Data Preview</p>
                <Table className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="bg-muted p-2 rounded-md mt-1 overflow-x-auto">
                <pre className="text-xs">
                  {result.sample_data ? 
                    JSON.stringify(result.sample_data, null, 2) : 
                    "No sample data available"}
                </pre>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="space-y-4">
      {!result && (
        <>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed ${isDragActive ? "border-primary bg-blue-50" : "border-neutral-300 bg-neutral-100 hover:bg-neutral-200"
              } rounded-lg p-6 flex flex-col items-center justify-center transition-colors cursor-pointer ${isLoading ? "opacity-50 cursor-not-allowed" : ""
              }`}
          >
            <input {...getInputProps()} />
            <div className="mb-4 text-primary">
              <FileSpreadsheet className="h-12 w-12" />
            </div>

            <p className="text-center text-neutral-600 mb-2">
              <span className="font-medium">Drop your Excel or CSV file here</span>
            </p>
            <p className="text-center text-neutral-500 text-sm mb-4">
              or click to browse files
            </p>

            <p className="text-center text-neutral-400 text-xs">
              Supported formats: .xlsx, .xls, .csv
            </p>
          </div>

          {file && (
            <div className="bg-muted p-3 rounded-md flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileSpreadsheet className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium">{file.name}</span>
                <span className="text-xs text-muted-foreground">
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleUpload}
                  disabled={isLoading}
                >
                  {isLoading ? "Processing..." : "Upload & Process"}
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => setFile(null)}
                  disabled={isLoading}
                >
                  <XIcon className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </>
      )}

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {renderResults()}

      {result && (
        <div className="flex justify-end">
          <Button variant="outline" onClick={resetUpload}>
            Upload Another File
          </Button>
        </div>
      )}
    </div>
  );
};

export default SmartFileUpload; 
import React, { useState } from "react";
import Header from "@/components/Header";
import SmartFileUpload from "@/components/SmartFileUpload";
import FileUpload from "@/components/FileUpload";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const SmartUpload: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  const handleSuccessfulUpload = (data: any) => {
    console.log("File uploaded successfully:", data);
    // You can add more logic here if needed
  };

  const handleFileUpload = (file: File) => {
    console.log("File uploaded:", file.name);
    setUploadedFiles(prev => [...prev, file.name]);
  };

  const handleRemoveFile = (fileId: string) => {
    console.log("File removed:", fileId);
    // In a real app, you'd use the fileId to remove the file
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <Header />
      <main className="flex-1 flex flex-col overflow-auto p-6">
        <div className="max-w-2xl mx-auto w-full">
          <div className="mb-4">
            <h1 className="text-xl font-bold mb-1">File Upload</h1>
            <p className="text-muted-foreground text-sm">
              Upload your files with drag and drop functionality. 
              Choose between our new file upload UI or smart Excel processing.
            </p>
          </div>
          
          <Tabs defaultValue="newUpload">
            <TabsList className="mb-3">
              <TabsTrigger value="newUpload">Modern Upload UI</TabsTrigger>
              <TabsTrigger value="smartUpload">Smart Excel Upload</TabsTrigger>
            </TabsList>
            
            <TabsContent value="newUpload">
              <Card className="shadow-sm">
                <CardHeader className="pb-2 pt-4">
                  <CardDescription className="text-xs">
                    Drag and drop your files, or click to browse
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0">
                  <FileUpload 
                    onFileUpload={handleFileUpload}
                    onRemoveFile={handleRemoveFile}
                    acceptedFormats={['.xlsx', '.xls', '.csv']}
                    maxFileSize={500}
                    multiple={true}
                  />
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="smartUpload">
              <Card>
                <CardHeader>
                  <CardTitle>Smart Excel Upload</CardTitle>
                  <CardDescription>
                    Upload your Excel or CSV files with automatic header detection
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <SmartFileUpload onSuccessfulUpload={handleSuccessfulUpload} />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
};

export default SmartUpload; 
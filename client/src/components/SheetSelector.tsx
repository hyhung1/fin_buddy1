import React from 'react';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { FileAnalysis } from '@shared/schema';
import { apiRequest } from '@/lib/queryClient';
import { toast } from '@/hooks/use-toast';

interface SheetSelectorProps {
  file: File | null;
  fileMetadata: FileAnalysis | null;
  onSheetSelect: (fileId: string, sheetName: string) => void;
  isDisabled?: boolean;
}

const SheetSelector: React.FC<SheetSelectorProps> = ({ 
  file, 
  fileMetadata, 
  onSheetSelect,
  isDisabled = false 
}) => {
  const [selectedSheet, setSelectedSheet] = React.useState<string>('');
  const [isConverting, setIsConverting] = React.useState(false);

  React.useEffect(() => {
    // Set the active sheet as the selected sheet when fileMetadata changes
    if (fileMetadata && fileMetadata.activeSheet) {
      setSelectedSheet(fileMetadata.activeSheet);
    } else if (fileMetadata && fileMetadata.sheets && fileMetadata.sheets.length > 0) {
      // Default to the first sheet if no active sheet is set
      setSelectedSheet(fileMetadata.sheets[0].name);
    }
  }, [fileMetadata]);

  const handleSheetSelect = () => {
    if (!fileMetadata || !selectedSheet || !fileMetadata.fileId) return;
    
    setIsConverting(true);
    
    // Use the callback directly instead of making our own API call
    // This ensures consistency with the hook implementation
    onSheetSelect(fileMetadata.fileId, selectedSheet);
    
    // Reset converting state after a short delay to show the UI state
    setTimeout(() => {
      setIsConverting(false);
    }, 500);
  };

  // Only show for Excel files with multiple sheets
  const isExcelFile = file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'));
  const hasMultipleSheets = fileMetadata && fileMetadata.sheets && fileMetadata.sheets.length > 1;
  
  if (!isExcelFile || !hasMultipleSheets || !fileMetadata) {
    return null;
  }

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button 
          variant="outline" 
          className="w-full mb-4"
          disabled={isDisabled}
        >
          <span className="mr-2">📋</span>
          Select Sheet: {selectedSheet || 'Choose a sheet'}
        </Button>
      </SheetTrigger>
      <SheetContent side="right">
        <SheetHeader>
          <SheetTitle>Select Excel Sheet</SheetTitle>
          <SheetDescription>
            Choose which sheet from the Excel file you want to analyze
          </SheetDescription>
        </SheetHeader>
        
        <div className="py-6">
          <RadioGroup 
            value={selectedSheet} 
            onValueChange={setSelectedSheet}
            className="flex flex-col space-y-3"
          >
            {fileMetadata.sheets.map((sheet) => (
              <div key={sheet.name} className="flex items-center space-x-2">
                <RadioGroupItem value={sheet.name} id={`sheet-${sheet.name}`} />
                <Label htmlFor={`sheet-${sheet.name}`} className="flex flex-col">
                  <span className="font-medium">{sheet.name}</span>
                  <span className="text-xs text-gray-500">
                    {sheet.rowCount} rows, {sheet.columnCount} columns
                  </span>
                </Label>
              </div>
            ))}
          </RadioGroup>
        </div>
        
        <div className="mt-4">
          <Button 
            onClick={handleSheetSelect} 
            disabled={!selectedSheet || selectedSheet === fileMetadata.activeSheet || isConverting}
            className="w-full"
          >
            {isConverting ? 'Processing...' : 'Analyze Selected Sheet'}
          </Button>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default SheetSelector;
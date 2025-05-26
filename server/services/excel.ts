import * as XLSX from 'xlsx';
import { FileAnalysis } from '@shared/schema';
import fs from 'fs';

interface SheetData {
  name: string;
  rowCount: number;
  columnCount: number;
  headers?: string[];
  sampleData?: Record<string, any[]>;
}

/**
 * Process an Excel file and extract its data and metadata
 */
export async function processExcelFile(filePath: string): Promise<FileAnalysis> {
  try {
    // Read the file
    const workbook = XLSX.readFile(filePath);
    const sheets: SheetData[] = [];

    // Process each sheet
    for (const sheetName of workbook.SheetNames) {
      const worksheet = workbook.Sheets[sheetName];
      const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      
      if (data.length === 0) {
        // Skip empty sheets
        continue;
      }

      // Calculate dimensions
      const rowCount = data.length;
      const columnCount = data.length > 0 ? (data[0] as any[]).length : 0;
      
      // Extract headers (first row) if they exist
      let headers: string[] = [];
      let sampleData: Record<string, any[]> = {};
      
      if (rowCount > 0) {
        headers = (data[0] as any[]).map(cell => String(cell || ''));
        
        // Extract sample data (first 5 rows) for each column
        if (rowCount > 1 && headers.length > 0) {
          for (let colIndex = 0; colIndex < headers.length; colIndex++) {
            const columnName = headers[colIndex] || `Column${colIndex + 1}`;
            sampleData[columnName] = [];
            
            // Get up to 5 sample values from each column
            for (let rowIndex = 1; rowIndex < Math.min(6, rowCount); rowIndex++) {
              const row = data[rowIndex] as any[];
              if (row && colIndex < row.length) {
                sampleData[columnName].push(row[colIndex]);
              }
            }
          }
        }
      }

      sheets.push({
        name: sheetName,
        rowCount,
        columnCount,
        headers,
        sampleData
      });
    }

    return { sheets };
  } catch (error) {
    console.error('Error processing Excel file:', error);
    throw error;
  }
}

/**
 * Extract data from a specific sheet and columns in the Excel file
 */
export async function extractDataFromSheet(filePath: string, sheetName: string, columns?: string[]): Promise<any[]> {
  try {
    const workbook = XLSX.readFile(filePath);
    
    // Check if sheet exists
    if (!workbook.SheetNames.includes(sheetName)) {
      throw new Error(`Sheet "${sheetName}" not found in the Excel file`);
    }
    
    const worksheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(worksheet);
    
    // Filter columns if specified
    if (columns && columns.length > 0) {
      return data.map(row => {
        const filteredRow: Record<string, any> = {};
        for (const col of columns) {
          if (col in row) {
            filteredRow[col] = row[col];
          }
        }
        return filteredRow;
      });
    }
    
    return data;
  } catch (error) {
    console.error('Error extracting data from sheet:', error);
    throw error;
  }
}

/**
 * Formats data into a table structure for the frontend
 */
export function formatTableData(data: any[], limit: number = 10): { headers: string[]; rows: any[][] } {
  if (!data || data.length === 0) {
    return { headers: [], rows: [] };
  }
  
  // Extract headers from the first object
  const headers = Object.keys(data[0]);
  
  // Convert data to rows
  const rows = data.slice(0, limit).map(item => {
    return headers.map(header => item[header]);
  });
  
  return { headers, rows };
}

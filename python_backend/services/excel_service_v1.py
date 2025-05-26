import pandas as pd
from fastapi import UploadFile, HTTPException
import io
from pathlib import Path
from typing import List

async def read_excel_file(file: UploadFile) -> pd.ExcelFile:
    try:
        content = await file.read()
        excel_data = io.BytesIO(content)
        return pd.ExcelFile(excel_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read Excel file: {str(e)}"
        )

def convert_sheet_to_csv(df: pd.DataFrame, original_filename: str, sheet_name: str) -> UploadFile:
    csv_data = io.BytesIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    
    return UploadFile(
        filename=f"{Path(original_filename).stem}_{sheet_name}.csv",
        file=csv_data
    )

async def convert_excel_to_list_of_csv(file: UploadFile) -> List[UploadFile]:
    try:
        # Read the Excel file
        excel_file = await read_excel_file(file)
        sheet_names = excel_file.sheet_names
        
        csv_files = []
        
        # Convert each sheet to CSV
        for sheet_name in sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file = convert_sheet_to_csv(df, file.filename, sheet_name)
            csv_files.append(csv_file)
        
        return csv_files
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to convert Excel file to CSV: {str(e)}"
        )
    finally:
        # Ensure the original file is closed
        await file.close()
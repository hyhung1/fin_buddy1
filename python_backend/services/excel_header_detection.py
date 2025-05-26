import pandas as pd
import os
import logging
from pathlib import Path
from fastapi import UploadFile, HTTPException
import io

logger = logging.getLogger("excel_buddy")

def read_table_auto(file_content, file_type="csv", sample_rows=50, **read_kwargs):
    """
    Read a CSV or Excel file from bytes content, auto-detecting which row is the header.
    
    Args:
        file_content: Bytes content of the file
        file_type: "csv" or "excel"
        sample_rows: Number of rows to sample for header detection
        **read_kwargs: Additional arguments to pass to the pandas read function
    
    Returns:
        df (DataFrame): the loaded table
        header_idx (int): zero-based index of the detected header row
    """
    try:
        if file_type == "csv":
            reader = lambda content, **kw: pd.read_csv(io.BytesIO(content), **kw)
        else:  # excel
            reader = lambda content, **kw: pd.read_excel(io.BytesIO(content), engine="openpyxl", **kw)

        # 1) sample raw rows without headers
        raw = reader(file_content, header=None, nrows=sample_rows, **read_kwargs)

        # 2) find the first "string-heavy" row
        header_idx = 0
        for i, row in raw.iterrows():
            non_num = row.map(
                lambda x: not isinstance(x, (int, float)) and not str(x).replace(".", "", 1).isdigit()
            ).sum()
            if non_num >= len(row) * 0.6:
                header_idx = i
                break

        # 3) re-read full file using discovered header
        df = reader(file_content, header=header_idx, **read_kwargs)
        df.reset_index(drop=True, inplace=True)
        return df, header_idx
    
    except Exception as e:
        logger.error(f"Error in read_table_auto: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

async def process_uploaded_file(upload_file: UploadFile, save_dir: Path):
    """
    Process an uploaded file, detect header, save as CSV, and return the dataframe.
    
    Args:
        upload_file: The uploaded file
        save_dir: Directory to save processed files
        
    Returns:
        tuple: (DataFrame, header_row, output_path)
    """
    try:
        file_content = await upload_file.read()
        file_extension = upload_file.filename.split('.')[-1].lower()
        
        # Determine file type
        file_type = "csv" if file_extension == "csv" else "excel"
        
        # Auto-detect header and read file
        df, header_idx = read_table_auto(file_content, file_type=file_type)
        
        # Create a unique filename for the processed file
        base_name = upload_file.filename.rsplit('.', 1)[0]
        output_filename = f"{base_name}_processed_header{header_idx}.csv"
        output_path = save_dir / output_filename
        
        # Save processed DataFrame to CSV
        df.to_csv(output_path, index=False)
        
        # Log a concise summary for troubleshooting (disabled by default)
        if logger.isEnabledFor(logging.DEBUG):
            preview_cols = ', '.join(df.columns[:5])
            logger.debug(
                "Loaded DataFrame with %d rows × %d cols (preview cols: %s)…", 
                len(df), df.shape[1], preview_cols
            )
        
        return df, header_idx, output_path
    
    except Exception as e:
        logger.error(f"Error processing uploaded file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}") 
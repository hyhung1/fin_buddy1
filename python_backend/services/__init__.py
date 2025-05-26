"""Utility re-exports for the *services* package.

Only CSV-conversion and smart header-detection helpers are exposed here.  The
Gemini helper functions relied on `google.adk`, which may not be installed in
every runtime environment and are no longer required by the backend.
"""

# CSV helpers ---------------------------------------------------------------
from .excel_service_v1 import convert_excel_to_list_of_csv  # legacy – still useful elsewhere
from .excel_header_detection import process_uploaded_file  # preferred smart helper

__all__ = [
    'convert_excel_to_list_of_csv',
    'process_uploaded_file',
]
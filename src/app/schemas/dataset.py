from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class DatasetUploadResponse(BaseModel):
    """Respuesta al subir un dataset"""
    dataset_id: str
    filename: str
    rows: int
    columns: int
    column_names: List[str]
    column_types: Dict[str, str]
    upload_timestamp: datetime
    file_size_bytes: int


class DataPreviewRequest(BaseModel):
    """Request para previsualizar datos"""
    dataset_id: str
    rows: int = Field(default=10, ge=1, le=100)


class DataPreviewResponse(BaseModel):
    """Respuesta con preview de datos"""
    dataset_id: str
    preview: List[Dict[str, Any]]
    total_rows: int
    showing_rows: int


class DataCleaningRequest(BaseModel):
    """Request para limpieza de datos"""
    dataset_id: str
    drop_duplicates: bool = False
    fill_na_strategy: Optional[str] = Field(
        default=None,
        description="Estrategia nulos: 'mean', 'median', 'mode', etc"
    )
    columns_to_drop: Optional[List[str]] = None
    type_conversions: Optional[Dict[str, str]] = Field(
        default=None,
        description="Conversiones de tipo: {'col': 'int64'}"
    )


class DataCleaningResponse(BaseModel):
    """Respuesta de limpieza de datos"""
    dataset_id: str
    original_rows: int
    cleaned_rows: int
    rows_removed: int
    columns_dropped: List[str]
    null_values_handled: int
    type_conversions_applied: Dict[str, str]

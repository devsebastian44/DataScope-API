from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.dataset import (
    DatasetUploadResponse, DataPreviewRequest, DataPreviewResponse,
    DataCleaningRequest, DataCleaningResponse
)
from app.services.data_processor import DataProcessor
from app.utils.file_handler import FileHandler
from app.core.responses import success_response

router = APIRouter()

@router.post("/upload", response_model=dict, summary="Subir dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Sube un archivo CSV o Excel y lo procesa.
    
    - **file**: Archivo CSV o Excel (.csv, .xlsx, .xls)
    
    Retorna información del dataset cargado incluyendo:
    - ID único del dataset
    - Número de filas y columnas
    - Nombres y tipos de columnas
    - Tamaño del archivo
    """
    # Guardar archivo
    dataset_id, file_path = await FileHandler.save_upload_file(file)
    
    # Cargar dataset
    df = FileHandler.load_dataset(file_path)
    
    # Obtener tamaño del archivo
    file_size = FileHandler.get_file_size(file_path)
    
    # Almacenar en memoria
    result = DataProcessor.store_dataset(dataset_id, df, file.filename, file_size)
    
    return success_response(
        message="Dataset cargado exitosamente",
        data=result
    )

@router.post("/preview", response_model=dict, summary="Preview del dataset")
async def preview_dataset(request: DataPreviewRequest):
    """
    Obtiene una vista previa del dataset.
    
    - **dataset_id**: ID del dataset
    - **rows**: Número de filas a mostrar (1-100, default: 10)
    """
    result = DataProcessor.get_preview(request.dataset_id, request.rows)
    
    return success_response(
        message="Preview generado exitosamente",
        data=result
    )

@router.post("/clean", response_model=dict, summary="Limpiar dataset")
async def clean_dataset(request: DataCleaningRequest):
    """
    Limpia el dataset aplicando varias transformaciones.
    
    - **dataset_id**: ID del dataset
    - **drop_duplicates**: Eliminar duplicados
    - **fill_na_strategy**: Estrategia para valores nulos ('mean', 'median', 'mode', 'drop', 'forward_fill', 'backward_fill')
    - **columns_to_drop**: Lista de columnas a eliminar
    - **type_conversions**: Diccionario con conversiones de tipo {'columna': 'tipo'}
    """
    result = DataProcessor.clean_data(
        dataset_id=request.dataset_id,
        drop_duplicates=request.drop_duplicates,
        fill_na_strategy=request.fill_na_strategy,
        columns_to_drop=request.columns_to_drop,
        type_conversions=request.type_conversions
    )
    
    return success_response(
        message="Dataset limpiado exitosamente",
        data=result
    )
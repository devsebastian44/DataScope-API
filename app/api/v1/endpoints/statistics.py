from fastapi import APIRouter
from app.schemas.statistics import (
    StatisticsRequest, StatisticsResponse,
    DistributionRequest, DistributionResponse
)
from app.services.statistics_service import StatisticsService
from app.core.responses import success_response

router = APIRouter()

@router.post("/descriptive", response_model=dict, summary="Estadísticas descriptivas")
async def get_descriptive_statistics(request: StatisticsRequest):
    """
    Calcula estadísticas descriptivas del dataset.
    
    Para cada columna numérica calcula:
    - mean, median, std, min, max, cuartiles
    - conteo de valores nulos
    - valores únicos
    
    Para columnas categóricas:
    - moda y frecuencia
    - top valores más frecuentes
    
    - **dataset_id**: ID del dataset
    - **columns**: Columnas específicas a analizar (opcional, si no se especifica analiza todas)
    - **include_correlations**: Incluir matriz de correlación
    """
    result = StatisticsService.calculate_statistics(
        dataset_id=request.dataset_id,
        columns=request.columns,
        include_correlations=request.include_correlations
    )
    
    return success_response(
        message="Estadísticas calculadas exitosamente",
        data=result
    )

@router.post("/distribution", response_model=dict, summary="Distribución de datos")
async def get_distribution(request: DistributionRequest):
    """
    Analiza la distribución de una columna específica.
    
    Para columnas numéricas incluye:
    - Histograma de frecuencias
    - Skewness (asimetría)
    - Kurtosis (curtosis)
    
    Para columnas categóricas:
    - Conteo de valores
    
    - **dataset_id**: ID del dataset
    - **column**: Nombre de la columna
    - **bins**: Número de bins para el histograma (5-100, default: 30)
    """
    result = StatisticsService.calculate_distribution(
        dataset_id=request.dataset_id,
        column=request.column,
        bins=request.bins
    )
    
    return success_response(
        message="Distribución calculada exitosamente",
        data=result
    )
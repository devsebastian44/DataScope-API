from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StatisticsRequest(BaseModel):
    """Request para calcular estadísticas"""
    dataset_id: str
    columns: Optional[List[str]] = Field(
        default=None,
        description="Columnas para analizar. Si es None, analiza todas."
    )
    include_correlations: bool = False


class ColumnStatistics(BaseModel):
    """Estadísticas de una columna"""
    column_name: str
    data_type: str
    count: int
    null_count: int
    null_percentage: float
    unique_count: int

    # Para columnas numéricas
    mean: Optional[float] = None
    median: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    q25: Optional[float] = None
    q75: Optional[float] = None

    # Para columnas categóricas
    mode: Optional[Any] = None
    mode_frequency: Optional[int] = None
    top_values: Optional[Dict[str, int]] = None


class StatisticsResponse(BaseModel):
    """Respuesta con estadísticas del dataset"""
    dataset_id: str
    total_rows: int
    total_columns: int
    memory_usage_mb: float
    column_statistics: List[ColumnStatistics]
    correlation_matrix: Optional[Dict[str, Dict[str, float]]] = None


class DistributionRequest(BaseModel):
    """Request para análisis de distribución"""
    dataset_id: str
    column: str
    bins: int = Field(default=30, ge=5, le=100)


class DistributionResponse(BaseModel):
    """Respuesta con distribución de datos"""
    dataset_id: str
    column: str
    distribution: Dict[str, int]
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None

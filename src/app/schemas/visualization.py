from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PlotType(str, Enum):
    """Tipos de gráficos disponibles"""
    HISTOGRAM = "histogram"
    BOXPLOT = "boxplot"
    SCATTER = "scatter"
    LINE = "line"
    BAR = "bar"
    HEATMAP = "heatmap"
    VIOLIN = "violin"
    PAIRPLOT = "pairplot"
    COUNTPLOT = "countplot"


class PlotFormat(str, Enum):
    """Formatos de salida del gráfico"""
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"


class VisualizationRequest(BaseModel):
    """Request para generar visualización"""
    dataset_id: str
    plot_type: PlotType
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    hue_column: Optional[str] = None
    columns: Optional[List[str]] = Field(
        default=None,
        description="Para heatmap o pairplot, lista de columnas a incluir"
    )
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    color: Optional[str] = "steelblue"
    figsize_width: int = Field(default=10, ge=4, le=20)
    figsize_height: int = Field(default=6, ge=4, le=20)
    plot_format: PlotFormat = PlotFormat.PNG
    dpi: int = Field(default=100, ge=50, le=300)

    @validator('x_column')
    def validate_x_column(cls, v, values):
        plot_type = values.get('plot_type')
        required_types = [
            PlotType.HISTOGRAM, PlotType.BOXPLOT, PlotType.SCATTER,
            PlotType.LINE, PlotType.BAR, PlotType.VIOLIN, PlotType.COUNTPLOT
        ]
        if plot_type in required_types:
            if v is None:
                raise ValueError(f"x_column es requerido para {plot_type}")
        return v


class VisualizationResponse(BaseModel):
    """Respuesta con visualización generada"""
    dataset_id: str
    plot_type: str
    plot_url: str
    plot_path: str
    filename: str
    format: str
    width: int
    height: int
    file_size_bytes: int

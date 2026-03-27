from fastapi import APIRouter
from app.schemas.visualization import VisualizationRequest
from app.services.visualization_service import VisualizationService
from app.core.responses import success_response


router = APIRouter()


@router.post(
    "/generate",
    response_model=dict,
    summary="Generar visualización"
)
async def generate_visualization(request: VisualizationRequest):
    """
    Genera una visualización personalizada del dataset.

    **Tipos de gráficos disponibles:**
    - **histogram**: Histograma de distribución (requiere x_column)
    - **boxplot**: Diagrama de caja (requiere x_column, opcional y_column)
    - **scatter**: Gráfico de dispersión (requiere x_column, y_column)
    - **line**: Gráfico de líneas (requiere x_column, y_column)
    - **bar**: Gráfico de barras (requiere x_column, opcional y_column)
    - **heatmap**: Mapa de calor de correlación (opcional columns)
    - **violin**: Gráfico de violín (requiere x_column, opcional y_column)
    - **pairplot**: Matriz de dispersión (opcional columns)
    - **countplot**: Conteo de categorías (requiere x_column)

    **Parámetros:**
    - **dataset_id**: ID del dataset
    - **plot_type**: Tipo de gráfico
    - **x_column**: Columna para eje X
    - **y_column**: Columna para eje Y (opcional)
    - **hue_column**: Columna para colorear por categorías (opcional)
    - **columns**: Lista de columnas (para heatmap/pairplot)
    - **title**: Título del gráfico
    - **xlabel, ylabel**: Etiquetas de los ejes
    - **color**: Color principal del gráfico
    - **figsize_width, figsize_height**: Tamaño de la figura
    - **plot_format**: Formato de salida (png, jpg, svg)
    - **dpi**: Resolución del gráfico

    **Retorna:**
    - URL para acceder al gráfico
    - Información del archivo generado
    """
    result = VisualizationService.generate_plot(
        dataset_id=request.dataset_id,
        plot_type=request.plot_type,
        x_column=request.x_column,
        y_column=request.y_column,
        hue_column=request.hue_column,
        columns=request.columns,
        title=request.title,
        xlabel=request.xlabel,
        ylabel=request.ylabel,
        color=request.color,
        figsize=(request.figsize_width, request.figsize_height),
        plot_format=request.plot_format.value,
        dpi=request.dpi
    )

    return success_response(
        message="Visualización generada exitosamente",
        data=result
    )

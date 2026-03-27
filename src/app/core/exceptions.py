from fastapi import HTTPException, status


class EDAException(HTTPException):
    """Excepción base para la API"""
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(status_code=status_code, detail=detail)


class FileProcessingError(EDAException):
    """Error al procesar archivos"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Error procesando archivo: {detail}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class InvalidFileFormatError(EDAException):
    """Formato de archivo no válido"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Formato de archivo inválido: {detail}",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )


class DataValidationError(EDAException):
    """Error de validación de datos"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Error de validación: {detail}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class ColumnNotFoundError(EDAException):
    """Columna no encontrada en el dataset"""
    def __init__(self, column: str):
        super().__init__(
            detail=f"Columna '{column}' no encontrada en el dataset",
            status_code=status.HTTP_404_NOT_FOUND
        )


class VisualizationError(EDAException):
    """Error al generar visualización"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Error generando visualización: {detail}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

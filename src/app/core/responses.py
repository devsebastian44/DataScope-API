from typing import Any, Optional

from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Respuesta estándar de la API"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[list] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operación exitosa",
                "data": {"key": "value"},
                "errors": None
            }
        }


def success_response(message: str, data: Any = None) -> dict:
    """Genera una respuesta exitosa"""
    return StandardResponse(
        success=True,
        message=message,
        data=data
    ).model_dump()


def error_response(message: str, errors: list = None) -> dict:
    """Genera una respuesta de error"""
    return StandardResponse(
        success=False,
        message=message,
        data=None,
        errors=errors or []
    ).model_dump()

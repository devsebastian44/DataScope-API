import os
import uuid
from pathlib import Path
from typing import Tuple
import pandas as pd
from fastapi import UploadFile
from app.config import settings
from app.core.exceptions import InvalidFileFormatError, FileProcessingError


class FileHandler:
    """Manejo de archivos subidos"""

    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Valida el archivo subido"""
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in settings.ALLOWED_EXTENSIONS:
            msg = (
                f"Extensión {file_ext} no permitida. Formatos aceptados: "
                f"{settings.ALLOWED_EXTENSIONS}"
            )
            raise InvalidFileFormatError(msg)

    @staticmethod
    async def save_upload_file(file: UploadFile) -> Tuple[str, Path]:
        """Guarda el archivo subido y retorna ID y path"""
        FileHandler.validate_file(file)

        # Generar ID único
        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix
        filename = f"{file_id}{file_ext}"
        file_path = settings.UPLOAD_DIR / filename

        try:
            # Guardar archivo
            content = await file.read()

            # Validar tamaño
            if len(content) > settings.MAX_FILE_SIZE:
                max_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
                msg = f"Archivo muy grande. Máximo permitido: {max_mb:.2f} MB"
                raise FileProcessingError(msg)

            with open(file_path, "wb") as f:
                f.write(content)

            return file_id, file_path

        except Exception as e:
            if file_path.exists():
                file_path.unlink()
            raise FileProcessingError(f"Error guardando archivo: {str(e)}")

    @staticmethod
    def load_dataset(file_path: Path) -> pd.DataFrame:
        """Carga un dataset desde un archivo"""
        file_ext = file_path.suffix.lower()

        try:
            if file_ext == '.csv':
                return pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            else:
                msg = f"Extensión no soportada: {file_ext}"
                raise InvalidFileFormatError(msg)
        except Exception as e:
            raise FileProcessingError(f"Error cargando dataset: {str(e)}")

    @staticmethod
    def get_file_size(file_path: Path) -> int:
        """Obtiene el tamaño del archivo en bytes"""
        return os.path.getsize(file_path)

    @staticmethod
    def delete_file(file_path: Path) -> None:
        """Elimina un archivo"""
        if file_path.exists():
            file_path.unlink()

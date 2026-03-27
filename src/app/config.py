from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "EDA API - Exploratory Data Analysis"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API REST profesional para análisis exploratorio"

    # CORS
    ALLOWED_ORIGINS: list = ["*"]  # En producción, dominios concretos

    # File Upload Settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: set = {".csv", ".xlsx", ".xls"}
    UPLOAD_DIR: Path = Path("uploads")
    OUTPUT_DIR: Path = Path("outputs")

    # Data Processing
    MAX_ROWS_PREVIEW: int = 100
    DEFAULT_CHUNK_SIZE: int = 10000

    # Visualization
    PLOT_DPI: int = 100
    PLOT_FIGSIZE: tuple = (10, 6)
    PLOT_FORMATS: set = {"png", "jpg", "svg"}

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Crear directorios si no existen
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.OUTPUT_DIR.mkdir(exist_ok=True)

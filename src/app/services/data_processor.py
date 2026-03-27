import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from app.core.exceptions import DataValidationError, ColumnNotFoundError


class DataProcessor:
    """Servicio para procesamiento de datos"""

    # Almacenamiento en memoria de datasets (en producción usar Redis/DB)
    _datasets: Dict[str, pd.DataFrame] = {}
    _metadata: Dict[str, dict] = {}

    @classmethod
    def store_dataset(
        cls,
        dataset_id: str,
        df: pd.DataFrame,
        filename: str,
        file_size: int
    ) -> dict:
        """Almacena un dataset en memoria"""
        cls._datasets[dataset_id] = df
        cls._metadata[dataset_id] = {
            "filename": filename,
            "upload_timestamp": datetime.now(),
            "file_size_bytes": file_size,
            "rows": len(df),
            "columns": len(df.columns)
        }

        return {
            "dataset_id": dataset_id,
            "filename": filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "column_types": {
                col: str(dtype) for col, dtype in df.dtypes.items()
            },
            "upload_timestamp": cls._metadata[dataset_id]["upload_timestamp"],
            "file_size_bytes": file_size
        }

    @classmethod
    def get_dataset(cls, dataset_id: str) -> pd.DataFrame:
        """Obtiene un dataset almacenado"""
        if dataset_id not in cls._datasets:
            raise DataValidationError(f"Dataset '{dataset_id}' no encontrado")
        return cls._datasets[dataset_id]

    @classmethod
    def get_preview(cls, dataset_id: str, rows: int = 10) -> dict:
        """Obtiene preview del dataset"""
        df = cls.get_dataset(dataset_id)
        preview_df = df.head(rows)

        return {
            "dataset_id": dataset_id,
            "preview": preview_df.to_dict(orient="records"),
            "total_rows": len(df),
            "showing_rows": len(preview_df)
        }

    @classmethod
    def clean_data(
        cls,
        dataset_id: str,
        drop_duplicates: bool = False,
        fill_na_strategy: Optional[str] = None,
        columns_to_drop: Optional[List[str]] = None,
        type_conversions: Optional[Dict[str, str]] = None
    ) -> dict:
        """Limpia el dataset"""
        df = cls.get_dataset(dataset_id).copy()
        original_rows = len(df)
        columns_dropped = []
        null_handled = 0
        conversions_applied = {}

        # Eliminar duplicados
        if drop_duplicates:
            df = df.drop_duplicates()

        # Eliminar columnas
        if columns_to_drop:
            for col in columns_to_drop:
                if col in df.columns:
                    df = df.drop(columns=[col])
                    columns_dropped.append(col)

        # Manejar valores nulos
        if fill_na_strategy:
            null_handled = df.isnull().sum().sum()

            if fill_na_strategy == "drop":
                df = df.dropna()
            elif fill_na_strategy == "mean":
                df = df.fillna(df.select_dtypes(include=[np.number]).mean())
            elif fill_na_strategy == "median":
                df = df.fillna(df.select_dtypes(include=[np.number]).median())
            elif fill_na_strategy == "mode":
                df = df.fillna(df.mode().iloc[0])
            elif fill_na_strategy == "forward_fill":
                df = df.fillna(method='ffill')
            elif fill_na_strategy == "backward_fill":
                df = df.fillna(method='bfill')

        # Conversiones de tipo
        if type_conversions:
            for col, dtype in type_conversions.items():
                if col in df.columns:
                    try:
                        df[col] = df[col].astype(dtype)
                        conversions_applied[col] = dtype
                    except Exception as e:
                        msg = (
                            f"No se pudo convertir '{col}' to {dtype}: "
                            f"{str(e)}"
                        )
                        raise DataValidationError(msg)

        # Actualizar dataset
        cls._datasets[dataset_id] = df

        return {
            "dataset_id": dataset_id,
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "rows_removed": original_rows - len(df),
            "columns_dropped": columns_dropped,
            "null_values_handled": null_handled,
            "type_conversions_applied": conversions_applied
        }

    @classmethod
    def validate_columns(cls, dataset_id: str, columns: List[str]) -> None:
        """Valida que las columnas existan en el dataset"""
        df = cls.get_dataset(dataset_id)
        for col in columns:
            if col not in df.columns:
                raise ColumnNotFoundError(col)

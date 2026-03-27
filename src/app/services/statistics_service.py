import pandas as pd
import numpy as np
from typing import List, Optional
from scipy import stats
from app.services.data_processor import DataProcessor
from app.schemas.statistics import ColumnStatistics


class StatisticsService:
    """Servicio para cálculo de estadísticas"""

    @staticmethod
    def calculate_statistics(
        dataset_id: str,
        columns: Optional[List[str]] = None,
        include_correlations: bool = False
    ) -> dict:
        """Calcula estadísticas descriptivas del dataset"""
        df = DataProcessor.get_dataset(dataset_id)

        # Seleccionar columnas
        if columns:
            DataProcessor.validate_columns(dataset_id, columns)
            df_analysis = df[columns]
        else:
            df_analysis = df

        # Calcular estadísticas por columna
        column_stats = []
        for col in df_analysis.columns:
            stats_dict = StatisticsService._calculate_column_statistics(
                df_analysis, col
            )
            column_stats.append(ColumnStatistics(**stats_dict))

        # Calcular correlaciones si se solicita
        correlation_matrix = None
        if include_correlations:
            numeric_df = df_analysis.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr = numeric_df.corr()
                correlation_matrix = {
                    col: corr[col].to_dict() for col in corr.columns
                }

        mem = df_analysis.memory_usage(deep=True).sum() / (1024 * 1024)
        return {
            "dataset_id": dataset_id,
            "total_rows": len(df),
            "total_columns": len(df_analysis.columns),
            "memory_usage_mb": mem,
            "column_statistics": [stat.model_dump() for stat in column_stats],
            "correlation_matrix": correlation_matrix
        }

    @staticmethod
    def _calculate_column_statistics(df: pd.DataFrame, column: str) -> dict:
        """Calcula estadísticas de una columna específica"""
        series = df[column]
        dtype = str(series.dtype)

        stats_dict = {
            "column_name": column,
            "data_type": dtype,
            "count": int(series.count()),
            "null_count": int(series.isnull().sum()),
            "null_percentage": float(
                series.isnull().sum() / len(series) * 100
            ),
            "unique_count": int(series.nunique())
        }

        # Estadísticas numéricas
        if pd.api.types.is_numeric_dtype(series):
            is_na = series.isnull().all()
            stats_dict.update({
                "mean": float(series.mean()) if not is_na else None,
                "median": float(series.median()) if not is_na else None,
                "std": float(series.std()) if not is_na else None,
                "min": float(series.min()) if not is_na else None,
                "max": float(series.max()) if not is_na else None,
                "q25": float(series.quantile(0.25)) if not is_na else None,
                "q75": float(series.quantile(0.75)) if not is_na else None
            })

        # Estadísticas categóricas
        else:
            mode_val = series.mode()
            if len(mode_val) > 0:
                stats_dict["mode"] = str(mode_val.iloc[0])
                stats_dict["mode_frequency"] = int(
                    series.value_counts().iloc[0]
                )

            # Top 5 valores más frecuentes
            top_vals = series.value_counts().head(5).to_dict()
            stats_dict["top_values"] = {
                str(k): int(v) for k, v in top_vals.items()
            }

        return stats_dict

    @staticmethod
    def calculate_distribution(
        dataset_id: str,
        column: str,
        bins: int = 30
    ) -> dict:
        """Calcula la distribución de una columna"""
        df = DataProcessor.get_dataset(dataset_id)
        DataProcessor.validate_columns(dataset_id, [column])

        series = df[column].dropna()

        result = {
            "dataset_id": dataset_id,
            "column": column,
            "distribution": {},
            "skewness": None,
            "kurtosis": None
        }

        # Para columnas numéricas
        if pd.api.types.is_numeric_dtype(series):
            counts, bin_edges = np.histogram(series, bins=bins)

            # Crear diccionario de distribución
            distribution = {}
            for i in range(len(counts)):
                label = f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}"
                distribution[label] = int(counts[i])

            result["distribution"] = distribution
            result["skewness"] = float(stats.skew(series))
            result["kurtosis"] = float(stats.kurtosis(series))

        # Para columnas categóricas
        else:
            value_counts = series.value_counts().to_dict()
            result["distribution"] = {
                str(k): int(v) for k, v in value_counts.items()
            }

        return result

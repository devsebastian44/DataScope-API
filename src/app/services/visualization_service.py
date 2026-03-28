import os
import uuid

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from app.config import settings
from app.core.exceptions import VisualizationError
from app.schemas.visualization import PlotType
from app.services.data_processor import DataProcessor

matplotlib.use('Agg')  # Backend sin GUI


class VisualizationService:
    """Servicio para generación de visualizaciones"""

    @staticmethod
    def generate_plot(
        dataset_id: str,
        plot_type: PlotType,
        x_column: str = None,
        y_column: str = None,
        hue_column: str = None,
        columns: list = None,
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        color: str = "steelblue",
        figsize: tuple = (10, 6),
        plot_format: str = "png",
        dpi: int = 100
    ) -> dict:
        """Genera una visualización"""
        df = DataProcessor.get_dataset(dataset_id)

        # Validar columnas
        cols_to_validate = [c for c in [x_column, y_column, hue_column] if c]
        if columns:
            cols_to_validate.extend(columns)
        if cols_to_validate:
            DataProcessor.validate_columns(dataset_id, cols_to_validate)

        # Generar filename único
        plot_id = str(uuid.uuid4())
        filename = f"{plot_id}.{plot_format}"
        plot_path = settings.OUTPUT_DIR / filename

        try:
            # Crear figura
            plt.figure(figsize=figsize)

            # Generar el tipo de gráfico solicitado
            if plot_type == PlotType.HISTOGRAM:
                VisualizationService._create_histogram(df, x_column, color)

            elif plot_type == PlotType.BOXPLOT:
                VisualizationService._create_boxplot(
                    df, x_column, y_column, hue_column
                )

            elif plot_type == PlotType.SCATTER:
                VisualizationService._create_scatter(
                    df, x_column, y_column, hue_column, color
                )

            elif plot_type == PlotType.LINE:
                VisualizationService._create_line(
                    df, x_column, y_column, hue_column
                )

            elif plot_type == PlotType.BAR:
                VisualizationService._create_bar(df, x_column, y_column, color)

            elif plot_type == PlotType.HEATMAP:
                VisualizationService._create_heatmap(df, columns)

            elif plot_type == PlotType.VIOLIN:
                VisualizationService._create_violin(
                    df, x_column, y_column, hue_column
                )

            elif plot_type == PlotType.PAIRPLOT:
                VisualizationService._create_pairplot(
                    df, columns, hue_column
                )

            elif plot_type == PlotType.COUNTPLOT:
                VisualizationService._create_countplot(
                    df, x_column, hue_column
                )

            # Configurar labels y título
            if title:
                plt.title(title, fontsize=14, fontweight='bold')
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)

            plt.tight_layout()

            # Guardar gráfico
            plt.savefig(
                plot_path,
                format=plot_format,
                dpi=dpi,
                bbox_inches='tight'
            )
            plt.close()

            # Obtener tamaño del archivo
            file_size = os.path.getsize(plot_path)

            return {
                "dataset_id": dataset_id,
                "plot_type": plot_type.value,
                "plot_url": f"/outputs/{filename}",
                "plot_path": str(plot_path),
                "filename": filename,
                "format": plot_format,
                "width": figsize[0],
                "height": figsize[1],
                "file_size_bytes": file_size
            }

        except Exception as e:
            if plot_path.exists():
                plot_path.unlink()
            raise VisualizationError(str(e)) from e

    @staticmethod
    def _create_histogram(df: pd.DataFrame, x_column: str, color: str):
        """Crea histograma"""
        plt.hist(
            df[x_column].dropna(),
            bins=30,
            color=color,
            edgecolor='black',
            alpha=0.7
        )
        plt.ylabel('Frecuencia')

    @staticmethod
    def _create_boxplot(
        df: pd.DataFrame,
        x_column: str,
        y_column: str = None,
        hue_column: str = None
    ):
        """Crea boxplot"""
        if y_column:
            sns.boxplot(data=df, x=x_column, y=y_column, hue=hue_column)
        else:
            sns.boxplot(data=df, y=x_column)

    @staticmethod
    def _create_scatter(
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        hue_column: str = None,
        color: str = "steelblue"
    ):
        """Crea scatter plot"""
        if hue_column:
            sns.scatterplot(
                data=df, x=x_column, y=y_column, hue=hue_column, alpha=0.6
            )
        else:
            plt.scatter(df[x_column], df[y_column], color=color, alpha=0.6)

    @staticmethod
    def _create_line(
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        hue_column: str = None
    ):
        """Crea line plot"""
        if hue_column:
            sns.lineplot(data=df, x=x_column, y=y_column, hue=hue_column)
        else:
            plt.plot(df[x_column], df[y_column], marker='o')

    @staticmethod
    def _create_bar(
        df: pd.DataFrame,
        x_column: str,
        y_column: str = None,
        color: str = "steelblue"
    ):
        """Crea bar plot"""
        if y_column:
            df.groupby(x_column)[y_column].mean().plot(kind='bar', color=color)
        else:
            df[x_column].value_counts().plot(kind='bar', color=color)

    @staticmethod
    def _create_heatmap(df: pd.DataFrame, columns: list = None):
        """Crea heatmap de correlación"""
        if columns:
            df_corr = df[columns].corr()
        else:
            df_corr = df.select_dtypes(include=['number']).corr()

        sns.heatmap(df_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)

    @staticmethod
    def _create_violin(
        df: pd.DataFrame,
        x_column: str,
        y_column: str = None,
        hue_column: str = None
    ):
        """Crea violin plot"""
        if y_column:
            sns.violinplot(data=df, x=x_column, y=y_column, hue=hue_column)
        else:
            sns.violinplot(data=df, y=x_column)

    @staticmethod
    def _create_pairplot(
        df: pd.DataFrame,
        columns: list = None,
        hue_column: str = None
    ):
        """Crea pairplot"""
        if columns:
            pairplot_df = df[columns + ([hue_column] if hue_column else [])]
        else:
            pairplot_df = df.select_dtypes(include=['number'])

        sns.pairplot(pairplot_df, hue=hue_column)

    @staticmethod
    def _create_countplot(
        df: pd.DataFrame,
        x_column: str,
        hue_column: str = None
    ):
        """Crea countplot"""
        sns.countplot(data=df, x=x_column, hue=hue_column)

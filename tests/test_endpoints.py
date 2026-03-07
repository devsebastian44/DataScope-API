import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import pandas as pd
from app.main import app

client = TestClient(app)

# Crear un CSV de prueba
@pytest.fixture
def sample_csv(tmp_path):
    """Crea un CSV de prueba"""
    df = pd.DataFrame({
        'edad': [25, 30, 35, 40, 45],
        'salario': [30000, 40000, 50000, 60000, 70000],
        'ciudad': ['A', 'B', 'A', 'C', 'B']
    })
    csv_path = tmp_path / "test_data.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

def test_health_check():
    """Test del endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_dataset(sample_csv):
    """Test de carga de dataset"""
    with open(sample_csv, 'rb') as f:
        response = client.post(
            "/api/v1/dataset/upload",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "dataset_id" in data["data"]
    assert data["data"]["rows"] == 5
    assert data["data"]["columns"] == 3
    
    return data["data"]["dataset_id"]

def test_preview_dataset(sample_csv):
    """Test de preview del dataset"""
    # Primero subir el dataset
    with open(sample_csv, 'rb') as f:
        upload_response = client.post(
            "/api/v1/dataset/upload",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    
    dataset_id = upload_response.json()["data"]["dataset_id"]
    
    # Luego obtener preview
    response = client.post(
        "/api/v1/dataset/preview",
        json={"dataset_id": dataset_id, "rows": 3}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["preview"]) == 3

def test_descriptive_statistics(sample_csv):
    """Test de estadísticas descriptivas"""
    with open(sample_csv, 'rb') as f:
        upload_response = client.post(
            "/api/v1/dataset/upload",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    
    dataset_id = upload_response.json()["data"]["dataset_id"]
    
    response = client.post(
        "/api/v1/statistics/descriptive",
        json={
            "dataset_id": dataset_id,
            "include_correlations": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "column_statistics" in data["data"]
    assert "correlation_matrix" in data["data"]

def test_generate_visualization(sample_csv):
    """Test de generación de visualización"""
    with open(sample_csv, 'rb') as f:
        upload_response = client.post(
            "/api/v1/dataset/upload",
            files={"file": ("test_data.csv", f, "text/csv")}
        )
    
    dataset_id = upload_response.json()["data"]["dataset_id"]
    
    response = client.post(
        "/api/v1/visualization/generate",
        json={
            "dataset_id": dataset_id,
            "plot_type": "histogram",
            "x_column": "edad",
            "title": "Test Histogram"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "plot_url" in data["data"]
    assert data["data"]["plot_type"] == "histogram"

def test_invalid_file_format():
    """Test con formato de archivo inválido"""
    response = client.post(
        "/api/v1/dataset/upload",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    
    assert response.status_code == 415  # Unsupported Media Type

def test_nonexistent_dataset():
    """Test con dataset inexistente"""
    response = client.post(
        "/api/v1/dataset/preview",
        json={"dataset_id": "nonexistent-id", "rows": 10}
    )
    
    assert response.status_code == 422  # Unprocessable Entity
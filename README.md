# 🚀 EDA API - Exploratory Data Analysis

API REST profesional para Análisis Exploratorio de Datos construida con FastAPI, Python, pandas y seaborn.

## 📋 Características

- ✅ Carga de datasets en CSV y Excel
- ✅ Limpieza y transformación de datos
- ✅ Estadísticas descriptivas completas
- ✅ Visualizaciones dinámicas personalizables
- ✅ Documentación automática con Swagger
- ✅ Arquitectura en capas (routers, services, schemas)
- ✅ Manejo robusto de errores
- ✅ Respuestas JSON consistentes

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **pandas**: Manipulación y análisis de datos
- **numpy**: Computación numérica
- **matplotlib & seaborn**: Visualización de datos
- **Pydantic**: Validación de datos
- **uvicorn**: Servidor ASGI

## 📦 Instalación

### Opción 1: Local

```bash
# Clonar el repositorio
git clone <repository-url>
cd eda-api

# Crear entorno virtual
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar la aplicación
python -m app.main
```

### Opción 2: Docker

```bash
# Construir imagen
docker build -t eda-api .

# Ejecutar contenedor
docker run -p 8000:8000 eda-api
```

## 🚀 Uso

La API estará disponible en: `http://localhost:8000`

- **Documentación Swagger**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 📚 Endpoints

### Dataset Management

#### 1. Subir Dataset
```http
POST /api/v1/dataset/upload
Content-Type: multipart/form-data

file: <archivo.csv o archivo.xlsx>
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Dataset cargado exitosamente",
  "data": {
    "dataset_id": "uuid-123",
    "filename": "data.csv",
    "rows": 1000,
    "columns": 15,
    "column_names": ["col1", "col2", "..."],
    "column_types": {"col1": "int64", "col2": "float64"}
  }
}
```

#### 2. Preview de Datos
```http
POST /api/v1/dataset/preview
Content-Type: application/json

{
  "dataset_id": "uuid-123",
  "rows": 10
}
```

#### 3. Limpiar Dataset
```http
POST /api/v1/dataset/clean
Content-Type: application/json

{
  "dataset_id": "uuid-123",
  "drop_duplicates": true,
  "fill_na_strategy": "mean",
  "columns_to_drop": ["col_innecesaria"],
  "type_conversions": {
    "edad": "int64",
    "precio": "float64"
  }
}
```

### Statistics

#### 4. Estadísticas Descriptivas
```http
POST /api/v1/statistics/descriptive
Content-Type: application/json

{
  "dataset_id": "uuid-123",
  "columns": ["edad", "salario"],
  "include_correlations": true
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_rows": 1000,
    "total_columns": 2,
    "column_statistics": [
      {
        "column_name": "edad",
        "mean": 35.5,
        "median": 34.0,
        "std": 12.3,
        "min": 18,
        "max": 65,
        "null_count": 5
      }
    ],
    "correlation_matrix": {...}
  }
}
```

#### 5. Distribución
```http
POST /api/v1/statistics/distribution
Content-Type: application/json

{
  "dataset_id": "uuid-123",
  "column": "edad",
  "bins": 30
}
```

### Visualization

#### 6. Generar Visualización
```http
POST /api/v1/visualization/generate
Content-Type: application/json

{
  "dataset_id": "uuid-123",
  "plot_type": "histogram",
  "x_column": "edad",
  "title": "Distribución de Edades",
  "color": "steelblue",
  "plot_format": "png"
}
```

**Tipos de gráficos disponibles:**
- `histogram`: Histograma
- `boxplot`: Diagrama de caja
- `scatter`: Dispersión
- `line`: Líneas
- `bar`: Barras
- `heatmap`: Mapa de calor
- `violin`: Violín
- `pairplot`: Matriz de dispersión
- `countplot`: Conteo

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "plot_url": "/outputs/uuid-plot.png",
    "filename": "uuid-plot.png",
    "format": "png"
  }
}
```

## 📊 Ejemplos de Uso

### Ejemplo Python
```python
import requests

# 1. Subir dataset
files = {'file': open('data.csv', 'rb')}
response = requests.post('http://localhost:8000/api/v1/dataset/upload', files=files)
dataset_id = response.json()['data']['dataset_id']

# 2. Obtener estadísticas
payload = {
    "dataset_id": dataset_id,
    "include_correlations": True
}
stats = requests.post('http://localhost:8000/api/v1/statistics/descriptive', json=payload)
print(stats.json())

# 3. Generar histograma
viz_payload = {
    "dataset_id": dataset_id,
    "plot_type": "histogram",
    "x_column": "edad",
    "title": "Distribución de Edades"
}
viz = requests.post('http://localhost:8000/api/v1/visualization/generate', json=viz_payload)
plot_url = viz.json()['data']['plot_url']
print(f"Gráfico disponible en: http://localhost:8000{plot_url}")
```

### Ejemplo JavaScript
```javascript
// 1. Subir dataset
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('http://localhost:8000/api/v1/dataset/upload', {
  method: 'POST',
  body: formData
});

const { data } = await uploadResponse.json();
const datasetId = data.dataset_id;

// 2. Generar visualización
const vizResponse = await fetch('http://localhost:8000/api/v1/visualization/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    dataset_id: datasetId,
    plot_type: 'scatter',
    x_column: 'edad',
    y_column: 'salario',
    title: 'Edad vs Salario'
  })
});

const vizData = await vizResponse.json();
console.log(vizData.data.plot_url);
```

## 🏗️ Arquitectura

```
app/
├── api/v1/endpoints/     # Endpoints REST
├── services/             # Lógica de negocio
├── schemas/              # Validación Pydantic
├── core/                 # Excepciones y responses
├── utils/                # Utilidades
└── main.py              # Aplicación principal
```

## 🔧 Configuración

Variables de entorno en `.env`:

```bash
API_V1_PREFIX=/api/v1
MAX_FILE_SIZE=52428800
ALLOWED_ORIGINS=["*"]
PLOT_DPI=100
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 Licencia

MIT License

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor abre un issue o pull request.
# DataScope API

![CI](https://github.com/devsebastian44/DataScope-API/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat&logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat&logo=opensourceinitiative&logoColor=white)

---

## 🧠 Overview

**DataScope API** es una API REST profesional orientada al **Análisis Exploratorio de Datos (EDA)** construida sobre el ecosistema moderno de Python. Permite a científicos de datos, analistas e ingenieros interactuar con datasets a través de endpoints HTTP sin necesidad de entornos de notebook, facilitando la integración con aplicaciones web, pipelines de datos o herramientas de BI.

> [!IMPORTANT]
> **Ethical Notice**: Este proyecto tiene fines educativos y de análisis exploratorio de datos. Asegúrese de tener los derechos necesarios para procesar los datos que cargue.

---

El proyecto sigue una **arquitectura en capas** bien definida (routers → services → schemas) que separa responsabilidades y garantiza escalabilidad. Desde la carga de un archivo CSV o Excel hasta la generación de visualizaciones avanzadas, DataScope API cubre el ciclo completo de exploración de datos de forma programática.

---

## ⚙️ Features

- 📂 **Carga de datasets** en formatos CSV y Excel mediante multipart/form-data
- 🔍 **Preview de datos** con control de filas para inspección rápida
- 🧹 **Limpieza y transformación** — eliminación de duplicados, imputación de nulos, conversión de tipos y descarte de columnas
- 📊 **Estadísticas descriptivas completas** — media, mediana, desviación estándar, mínimo, máximo, nulos, correlaciones
- 📈 **Distribución de variables** con soporte de bins configurable
- 🎨 **Visualizaciones dinámicas** en múltiples tipos de gráfico (histogram, boxplot, scatter, line, bar, heatmap, violin, pairplot, countplot)
- 📝 **Documentación automática** con Swagger UI y ReDoc integrados
- 🐳 **Docker-ready** para despliegue inmediato sin configuración de entorno
- ✅ **Manejo robusto de errores** y respuestas JSON consistentes en todos los endpoints

---

## 🛠️ Tech Stack

| Capa | Tecnología | Rol |
|------|-----------|-----|
| Framework web | **FastAPI** | Enrutamiento, validación, documentación automática |
| Servidor ASGI | **Uvicorn** | Servidor de producción y desarrollo |
| Análisis de datos | **Pandas** | Manipulación, limpieza y transformación de datasets |
| Computación numérica | **NumPy** | Operaciones matriciales y estadísticas |
| Visualización | **Matplotlib + Seaborn** | Generación de gráficos estáticos y estadísticos |
| Validación | **Pydantic** | Schemas de entrada/salida y configuración tipada |
| Contenerización | **Docker** | Empaquetado y despliegue portable |
| Lenguaje | **Python 3.11+** | Runtime principal (98.8% del código) |

---

## 📦 Installation

### Opción 1 — Entorno local

```bash
# 1. Clonar el repositorio
git clone https://github.com/devsebastian44/DataScope-API.git
cd DataScope-API

# 2. Crear y activar entorno virtual
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
.\venv\Scripts\Activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env según sea necesario

# 5. Ejecutar la aplicación
python -m app.main
```

### Opción 2 — Docker

```bash
# Construir la imagen
docker build -t datascope-api .

# Ejecutar el contenedor
docker run -p 8000:8000 datascope-api
```

---

## ▶️ Usage

Una vez levantada la aplicación, la API estará disponible en `http://localhost:8000`.

| Interfaz | URL |
|----------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| Health Check | `http://localhost:8000/health` |

### Flujo básico en Python

```python
import requests

# 1. Subir dataset
files = {'file': open('data.csv', 'rb')}
upload = requests.post('http://localhost:8000/api/v1/dataset/upload', files=files)
dataset_id = upload.json()['data']['dataset_id']

# 2. Limpiar datos
clean_payload = {
    "dataset_id": dataset_id,
    "drop_duplicates": True,
    "fill_na_strategy": "mean"
}
requests.post('http://localhost:8000/api/v1/dataset/clean', json=clean_payload)

# 3. Estadísticas descriptivas
stats = requests.post('http://localhost:8000/api/v1/statistics/descriptive', json={
    "dataset_id": dataset_id,
    "include_correlations": True
})
print(stats.json())

# 4. Generar visualización
viz = requests.post('http://localhost:8000/api/v1/visualization/generate', json={
    "dataset_id": dataset_id,
    "plot_type": "histogram",
    "x_column": "edad",
    "title": "Distribución de Edades",
    "color": "steelblue",
    "plot_format": "png"
})
print(viz.json()['data']['plot_url'])
```

### Tipos de gráficos disponibles

| Tipo | Descripción |
|------|-------------|
| `histogram` | Distribución de frecuencias |
| `boxplot` | Diagrama de caja y bigotes |
| `scatter` | Dispersión entre dos variables |
| `line` | Serie de tiempo o tendencia |
| `bar` | Comparación por categorías |
| `heatmap` | Matriz de correlación visual |
| `violin` | Distribución y densidad |
| `pairplot` | Matriz de dispersión multivariable |
| `countplot` | Conteo de valores categóricos |

---

## 📁 Project Structure

```
DataScope-API/
│
├── app/                        # Código fuente principal
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/      # Routers REST (dataset, statistics, visualization)
│   ├── services/               # Lógica de negocio y procesamiento de datos
│   ├── schemas/                # Modelos Pydantic para request/response
│   ├── core/                   # Configuración, excepciones y respuestas estándar
│   ├── utils/                  # Funciones utilitarias reutilizables
│   └── main.py                 # Punto de entrada de la aplicación FastAPI
│
├── outputs/                    # Gráficos generados (PNG, SVG, etc.)
├── tests/                      # Suite de pruebas con pytest
├── uploads/                    # Almacenamiento temporal de datasets subidos
│
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Archivos ignorados por Git
├── Dockerfile                  # Imagen Docker de la aplicación
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación principal
```

---

## 🔧 Configuration

Variables de entorno disponibles en `.env`:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `API_V1_PREFIX` | Prefijo base de la API | `/api/v1` |
| `MAX_FILE_SIZE` | Tamaño máximo de archivo en bytes | `52428800` (50 MB) |
| `ALLOWED_ORIGINS` | Orígenes CORS permitidos | `["*"]` |
| `PLOT_DPI` | Resolución de gráficos generados | `100` |

---

## 🧪 Testing

```bash
# Ejecutar toda la suite de pruebas
pytest tests/

# Con reporte de cobertura
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🚀 Roadmap

- [ ] **Autenticación y autorización** — API Keys o JWT para proteger endpoints
- [ ] **Soporte a bases de datos** — Conexión directa a PostgreSQL, MySQL o MongoDB como fuente de datos
- [ ] **Exportación de reportes** — Generación de reportes EDA en PDF o HTML
- [ ] **Análisis avanzado** — Detección de outliers, test de normalidad, análisis de series temporales
- [ ] **WebSockets** — Streaming de resultados para datasets grandes en tiempo real
- [ ] **Cache de datasets** — Redis para almacenamiento temporal y mejora de performance
- [ ] **CI/CD Pipeline** — GitHub Actions para testing automático y despliegue continuo
- [ ] **Soporte multiusuario** — Sesiones independientes por usuario con namespacing de datasets

---

## 📄 License

Distribuido bajo la licencia **MIT**.

---

## 👨‍💻 Author

**Sebastian**
- 🐙 GitHub: [@devsebastian44](https://github.com/devsebastian44)

---

## 🤝 Contributing

Las contribuciones son lo que hacen que la comunidad de código abierto sea un lugar increíble para aprender, inspirar y crear. Cualquier contribución que hagas será **muy apreciada**.

1. Fork del proyecto
2. Crea tu rama de característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'feat: add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
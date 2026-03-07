# Railway Deployment Guide

## 🚀 Despliegue en Railway

### Prerrequisitos
- Cuenta en [Railway.app](https://railway.app)
- Repositorio GitHub conectado

### Pasos para despliegue

1. **Conectar Repositorio**
   - Entra a Railway dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Selecciona `devsebastian44/DataScope-API`

2. **Configuración Automática**
   - Railway detectará `railway.toml` automáticamente
   - Usará Python 3.11 y el comando de inicio configurado

3. **Variables de Entorno**
   - Railway configurará automáticamente las variables definidas en `railway.toml`
   - Puedes ajustarlas en Settings → Variables

4. **Volúmenes Persistentes**
   - Los volúmenes `uploads` y `outputs` se crearán automáticamente
   - Los archivos subidos y gráficos generados persistirán

### Endpoints Disponibles
- **API**: `https://tu-app.railway.app/api/v1/`
- **Documentación**: `https://tu-app.railway.app/docs`
- **Health Check**: `https://tu-app.railway.app/health`

### Variables de Entorno Configuradas
- `API_V1_PREFIX=/api/v1`
- `MAX_FILE_SIZE=52428800` (50MB)
- `ALLOWED_ORIGINS=*`
- `PLOT_DPI=100`

### Notas Importantes
- Railway proporciona almacenamiento persistente para volúmenes
- La API se reiniciará automáticamente en caso de fallos
- El despliegue es automático con cada push a la rama principal

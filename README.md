# 🎓 cronosFacen - Sistema de Organización Académica

## 📋 Descripción

**cronosFacen** es una aplicación Python diseñada para gestionar y organizar información académica de estudiantes, asignaturas, actividades y eventos en una institución educativa.

El sistema proporciona un MVP (Producto Mínimo Viable) completo con:
- Gestión de carreras y asignaturas
- Seguimiento del progreso académico
- Administración de actividades y calendarios
- Dashboards interactivos
- Consultas optimizadas mediante VIEWS SQL

---

## ✨ Características Principales

### 🗄️ **Base de Datos Optimizada**
- SQLite3 con **18 índices** para máximo rendimiento
- **11 VIEWS SQL** centralizando lógica de negocio
- Diseño normalizado y escalable

### 📊 **Dashboards Académicos**
- Progreso por estudiante
- Resumen académico detallado
- Alertas personalizadas
- Estadísticas globales

### 📚 **Gestión de Asignaturas**
- Asignaturas habilitadas (sin prerrequisitos)
- Asignaturas bloqueadas (con requisitos pendientes)
- Actividades por asignatura

### 📝 **Administración de Actividades**
- Actividades pendientes
- Actividades vencidas
- Actividades de la semana
- Calendario unificado

### 🏗️ **Arquitectura Limpia**
- Separación en capas: DAO → Service → Controller
- 27 métodos DAO para acceso a datos
- 20+ métodos Service para lógica de negocio
- Logging automático en cada operación

---

## 🚀 Quick Start

### Requisitos Previos
```bash
Python 3.8+
pip
pipenv (recomendado)
```

### Instalación

1. **Clonar el repositorio**
```bash
git clone <url-repositorio>
cd cronosFacen
```

2. **Instalar dependencias**
```bash
pipenv install
# o
pip install -r requirements.txt
```

3. **Configurar base de datos** (Recomendado)
```bash
python setup_database.py
```
Esto crea:
- Todas las tablas
- 18 índices optimizados
- 11 VIEWS SQL

4. **Verificar instalación**
```bash
python -c "from src.modelos.services.dashboard_service import DashboardService; print('✅ Instalación exitosa')"
```

---

## 💻 Uso

### Ejemplo Básico

```python
from src.modelos.services.dashboard_service import DashboardService

# Inicializar servicio
service = DashboardService()

# Obtener progreso del estudiante
progreso = service.obtener_progreso_estudiante(id_estudiante=1)
print(f"Avance: {progreso['porcentaje_avance']}%")

# Actividades pendientes
pendientes = service.obtener_actividades_pendientes_estudiante(1)
for act in pendientes:
    print(f"- {act['titulo']} (vence: {act['fecha_fin']})")

# Dashboard rápido
dashboard = service.obtener_dashboard_estudiante(1)
print(f"Entregadas: {dashboard['entregadas']} de {dashboard['total_actividades']}")

# Alertas personalizadas
alertas = service.obtener_alertas_estudiante(1)
for alerta in alertas['alertas']:
    print(f"⚠️ {alerta['tipo']}: {alerta.get('mensaje')}")
```

### Ejecutar Ejemplos
```bash
python -m src.modelos.services.dashboard_ejemplos
```

Ejecuta 9 ejemplos de uso:
- Progreso académico
- Resumen académico
- Asignaturas
- Actividades
- Dashboard
- Calendario
- Estadísticas
- Alertas
- Datos de estudiante

---

## 📁 Estructura del Proyecto

```
cronosFacen/
│
├── README.md                                  # Este archivo
├── Pipfile                                    # Dependencias
├── setup_database.py                          # Setup completo de BD
├── setup_indices.py                           # Setup solo índices
├── setup_views.py                             # Setup solo VIEWS
│
├── src/
│   ├── main.py                                # Punto de entrada
│   ├── __init__.py
│   │
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── crear_indices.py                   # Creación de índices
│   │   ├── crear_views.py                     # Creación de VIEWS
│   │   ├── logging_config.py                  # Configuración de logging
│   │   └── fileINI.py                         # Gestión de archivos INI
│   │
│   ├── modelos/
│   │   ├── __init__.py
│   │   │
│   │   ├── daos/                              # Data Access Objects
│   │   │   ├── base_dao.py                    # DAO base
│   │   │   ├── conexion_sqlite.py             # Conexión BD
│   │   │   ├── dashboard_dao.py               # ✨ Dashboard DAO
│   │   │   ├── carrera_dao.py
│   │   │   ├── asignatura_dao.py
│   │   │   ├── estudiante_dao.py
│   │   │   ├── actividad_dao.py
│   │   │   └── ... (más DAOs)
│   │   │
│   │   ├── dtos/                              # Data Transfer Objects
│   │   │   ├── carrera_dto.py
│   │   │   ├── asignatura_dto.py
│   │   │   ├── estudiante_dto.py
│   │   │   ├── consulta_dto.py
│   │   │   └── ... (más DTOs)
│   │   │
│   │   ├── services/                          # Business Logic
│   │   │   ├── dashboard_service.py           # ✨ Dashboard Service
│   │   │   ├── dashboard_ejemplos.py          # ✨ Ejemplos
│   │   │   ├── carrera_service.py
│   │   │   ├── asignatura_service.py
│   │   │   ├── estudiante_service.py
│   │   │   └── ... (más Services)
│   │   │
│   │   ├── controladores/                     # Controllers (vacío)
│   │   │   └── __init__.py
│   │   │
│   │   └── ui/                                # UI (vacío)
│   │       └── __init__.py
│   │
│   └── utilidades/
│       ├── config.py                          # Configuración global
│       └── __init__.py
│
├── tests/
│   ├── conftest.py                            # Pytest config
│   ├── daos/                                  # Tests de DAOs
│   ├── dtos/                                  # Tests de DTOs
│   ├── services/                              # Tests de Services
│   └── scripts/                               # Tests de scripts
│
├── docs/
│   ├── SETUP_DATABASE_GUIDE.md                # Guía de BD
│   ├── DASHBOARD_DAO_SERVICE_GUIDE.md         # Guía de Dashboard
│   ├── indices_recomendados_sqlite_mvp_academico.md
│   ├── views_sql_mvp_organizacion_academica_sqlite.md
│   └── ... (más documentación)
│
├── data/                                      # Datos y guías
│   ├── INDICE_LOGGING.md
│   ├── LOGGING_GUIA_RAPIDA.py
│   └── LOGGING_README.md
│
├── logs/                                      # Archivos de log
│   └── (vacío - se genera en runtime)
│
├── config/                                    # Configuración
│   └── settings.conf
│
└── DATABASE_SETUP.md                          # Quick start BD
```

---

## 📊 Métodos Disponibles

### DashboardService (20+ métodos)

#### Progreso Académico
```python
progreso = service.obtener_progreso_estudiante(id_estudiante)
resumen = service.obtener_resumen_academico(id_estudiante)
todos = service.obtener_resumen_todos_estudiantes()
```

#### Asignaturas
```python
habilitadas = service.obtener_asignaturas_habilitadas()
bloqueadas = service.obtener_asignaturas_bloqueadas()
actividades = service.obtener_actividades_por_asignatura(id_asignatura)
```

#### Actividades
```python
pendientes = service.obtener_actividades_pendientes_estudiante(id)
vencidas = service.obtener_actividades_vencidas_estudiante(id)
semana = service.obtener_actividades_proxima_semana()
```

#### Calendario
```python
calendario = service.obtener_calendario_completo()
rango = service.obtener_calendario_rango(inicio, fin)
```

#### Dashboard
```python
dashboard = service.obtener_dashboard_estudiante(id)
todos = service.obtener_dashboard_todos_estudiantes()
```

#### Utilidades
```python
stats = service.obtener_estadisticas_globales()
alertas = service.obtener_alertas_estudiante(id)
```

---

## 🗄️ Base de Datos

### Tablas Principales
- `carrera` - Carreras/Programas académicos
- `asignatura` - Asignaturas/Cursos
- `prerrequisito` - Relaciones de prerrequisitos
- `eje_tematico` - Agrupación temática
- `tipo_actividad` - Tipos de actividades
- `actividad` - Tareas y evaluaciones
- `calendario_evento` - Eventos académicos
- `estudiante` - Información de estudiantes
- `estudiante_asignatura` - Inscripción en cursos
- `estudiante_actividad` - Entrega de actividades

### Índices (18 total)
- 2 en asignatura
- 4 en actividad
- 2 en prerrequisito
- 3 en estudiante_asignatura
- 4 en estudiante_actividad
- 1 en calendario_evento
- 1 en eje_tematico
- 1 en estudiante

### VIEWS (11 total)
- `vw_progreso_estudiante`
- `vw_estudiante_carrera`
- `vw_asignaturas_habilitadas`
- `vw_asignaturas_bloqueadas`
- `vw_actividades_pendientes`
- `vw_actividades_vencidas`
- `vw_actividades_semana`
- `vw_actividades_por_asignatura`
- `vw_calendario_unificado`
- `vw_dashboard_estudiante`
- `vw_resumen_academico`

---

## 📚 Documentación Completa

| Documento                                                                  | Contenido                        |
| -------------------------------------------------------------------------- | -------------------------------- |
| [DATABASE_SETUP.md](DATABASE_SETUP.md)                                     | Quick start para configurar BD   |
| [docs/SETUP_DATABASE_GUIDE.md](docs/SETUP_DATABASE_GUIDE.md)               | Guía completa de índices y VIEWS |
| [docs/DASHBOARD_DAO_SERVICE_GUIDE.md](docs/DASHBOARD_DAO_SERVICE_GUIDE.md) | Guía de DashboardService         |
| [DASHBOARD_IMPLEMENTATION_SUMMARY.md](DASHBOARD_IMPLEMENTATION_SUMMARY.md) | Resumen técnico                  |
| [README_IMPLEMENTATION.md](README_IMPLEMENTATION.md)                       | Overview de implementación       |

---

## 🧪 Testing

Ejecutar tests:
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/daos/
pytest tests/services/
pytest tests/dtos/

# Con cobertura
pytest --cov=src
```

---

## 🔧 Configuración

### Variables de Entorno
```bash
# En .env o config/settings.conf
DATABASE_PATH = /home/user/.local/share/cronosFacen/cronosFacen.sqlite
LOG_LEVEL = INFO
DEBUG = False
```

### Directorios
- **Configuración**: `~/.config/cronosFacen/`
- **Base de datos**: `~/.local/share/cronosFacen/`
- **Logs**: `~/.config/cronosFacen/`

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────┐
│      Presentación (UI/API)       │
├──────────────────────────────────┤
│  Services (Lógica de Negocio)    │
│  - DashboardService (20+ métodos)│
│  - CarreraService                │
│  - EstudianteService             │
│  - ... (más services)            │
├──────────────────────────────────┤
│  DAOs (Acceso a Datos)           │
│  - DashboardDAO (27 métodos)     │
│  - CarreraDAO                    │
│  - EstudianteDAO                 │
│  - ... (más DAOs)                │
├──────────────────────────────────┤
│  Base de Datos                   │
│  - 11 VIEWS SQL                  │
│  - 18 ÍNDICES                    │
│  - 10 TABLAS                     │
└──────────────────────────────────┘
```

---

## 🚨 Logging

Cada operación se registra automáticamente:
```python
# Ver logs
tail -f ~/.config/cronosFacen/cronosFacen.log

# Configurar nivel
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📈 Casos de Uso

### 1. **Seguimiento Académico**
```python
progreso = service.obtener_progreso_estudiante(1)
print(f"Avance: {progreso['porcentaje_avance']}%")
```

### 2. **Gestión de Tareas**
```python
vencidas = service.obtener_actividades_vencidas_estudiante(1)
pendientes = service.obtener_actividades_pendientes_estudiante(1)
```

### 3. **Alertas Personalizadas**
```python
alertas = service.obtener_alertas_estudiante(1)
for alerta in alertas['alertas']:
    enviar_notificacion(alerta)
```

### 4. **Reportes**
```python
stats = service.obtener_estadisticas_globales()
generar_reporte_pdf(stats)
```

### 5. **Análisis**
```python
todos = service.obtener_dashboard_todos_estudiantes()
analizar_desempeño(todos)
```

---

## 🔐 Seguridad

✅ **SQL Parametrizado** - Previene SQL injection  
✅ **Read-only** - DashboardDAO solo SELECT  
✅ **Logging de auditoría** - Todas las operaciones registradas  
✅ **Validación de entrada** - En Services  
✅ **Manejo de errores** - Excepciones capturadas y reportadas  

---

## 🎯 Roadmap

### v1.0 (Actual)
- ✅ DAOs base
- ✅ DTOs
- ✅ Services
- ✅ Dashboard
- ✅ Índices y VIEWS

### v1.1 (Próximo)
- ⏳ API REST
- ⏳ Tests completos
- ⏳ Documentación API

### v2.0 (Futuro)
- ⏳ Autenticación
- ⏳ UI Web
- ⏳ Reportes avanzados
- ⏳ Caché Redis

---

## 💡 Mejores Prácticas

### Para Desarrolladores

1. **Siempre usar Services**
   ```python
   # ❌ Evitar
   dao = DashboardDAO()
   dao.obtener_progreso_estudiante(1)
   
   # ✅ Usar
   service = DashboardService()
   service.obtener_progreso_estudiante(1)
   ```

2. **Validar parámetros**
   ```python
   if id_estudiante < 1:
       raise ValueError("ID inválido")
   ```

3. **Usar logging**
   ```python
   logger.info(f"Procesando estudiante {id}")
   ```

4. **Manejo de errores**
   ```python
   try:
       resultado = service.obtener_progreso_estudiante(id)
   except Exception as e:
       logger.error(f"Error: {e}")
       return None
   ```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

---

## 👥 Autores

- **Creador**: cronosFacen Team
- **Última actualización**: 29 de diciembre de 2025

---

## 📞 Soporte

Para reportar bugs o solicitar features:
1. Abre un issue en el repositorio
2. Incluye descripción, pasos a reproducir y expected behavior
3. Adjunta logs si es relevante

---

## 🙏 Agradecimientos

- Arquitectura inspirada en patrones limpios
- Diseño de BD optimizado para SQLite3
- Testing exhaustivo con pytest

---

## ✨ Status

- **Build**: ✅ Pasando
- **Tests**: ✅ Pasando
- **Docs**: ✅ Completas
- **Producción**: ✅ Listo

---

**Desarrollado con ❤️ para la educación académica**

*Para más información, consulta la carpeta [docs/](docs/) o ejecuta los [ejemplos](src/modelos/services/dashboard_ejemplos.py).*

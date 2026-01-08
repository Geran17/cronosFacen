# 🎓 cronosFacen - Sistema de Organización Académica

## 📋 Descripción

**cronosFacen** es una aplicación desktop (interfaz TTK) desarrollada en Python para gestionar y organizar información académica de estudiantes, asignaturas, actividades y eventos en una institución educativa.

El sistema proporciona un MVP (Producto Mínimo Viable) completo con:
- Gestión completa de carreras, asignaturas, actividades y calendarios
- Administración de estudiantes y su relación con carreras/asignaturas
- Control de prerequisitos y ejes temáticos
- Base de datos SQLite3 optimizada
- Interfaz gráfica moderna con ttkbootstrap
- Arquitectura en capas (DAO → Service → Controller)

---

## ✨ Características Principales

### 🎨 **Interfaz Gráfica Moderna**
- Desarrollada con **ttkbootstrap**
- Interfaz amigable y responsiva
- Múltiples controladores para diferentes módulos
- Soporte para Pillow para manejo de imágenes

### 🗄️ **Base de Datos Robusta**
- SQLite3 con índices optimizados
- Arquitectura normalizada y escalable
- 16 DAOs especializados para acceso a datos
- 13 Services para lógica de negocio

### 📚 **Módulos Principales**
- **Carreras**: Gestión de programas académicos
- **Asignaturas**: Cursos y su relación con carreras
- **Estudiantes**: Información y seguimiento
- **Actividades**: Tareas, evaluaciones y entregas
- **Calendarios**: Eventos académicos
- **Prerequisitos**: Control de dependencias
- **Tipos de Actividad**: Categorización flexible
- **Ejes Temáticos**: Organización por temas

### 🏗️ **Arquitectura Limpia**
- Separación en capas: DAO → Service → Controller
- 16 DAOs para acceso a datos
- 13 Services para lógica de negocio
- 13 Controladores para interfaz gráfica
- DTOs para transferencia de datos

---

## 🚀 Quick Start

### Requisitos Previos
```bash
Python 3.12+
pip
pipenv (recomendado)
```

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Geran17/cronosFacen.git
cd cronosFacen
```

2. **Instalar dependencias**
```bash
pipenv install
# o
pip install -r requirements.txt
```

3. **Configurar base de datos** (Opcional)
```bash
python setup_database.py
```
Esto crea:
- Todas las tablas
- Índices optimizados

4. **Ejecutar la aplicación**
```bash
python -m src.main
```

O directamente:
```bash
python src/main.py
```

---

## 💻 Uso

### Ejecución de la Aplicación

La aplicación se lanza con la interfaz gráfica TTK:

```bash
python src/main.py
```

Al iniciar:
1. Se crean los directorios necesarios (configuración, logs, BD)
2. Se crean los índices en la base de datos
3. Se crean las VIEWS SQL necesarias
4. Se abre la ventana principal de la aplicación

### Uso Programático (Desarrollo)

```python
from src.modelos.services.carrera_service import CarreraService
from src.modelos.services.estudiante_service import EstudianteService

# Ejemplo: Obtener carreras
carrera_service = CarreraService()
carreras = carrera_service.obtener_todas()

# Ejemplo: Obtener estudiantes
estudiante_service = EstudianteService()
estudiantes = estudiante_service.obtener_todos()

# Ejemplo: Obtener asignaturas de un estudiante
estudiante_asignatura_service = EstudianteAsignaturaService()
asignaturas = estudiante_asignatura_service.obtener_asignaturas_por_estudiante(id_estudiante=1)
```

---

## 📁 Estructura del Proyecto

```
cronosFacen/
│
├── README.md                                  # Este archivo
├── Pipfile                                    # Dependencias con Python 3.12
├── setup_database.py                          # Setup de base de datos
├── setup_indices.py                           # Setup solo índices
├── setup_views.py                             # Setup solo VIEWS
│
├── src/
│   ├── main.py                                # Punto de entrada de la aplicación
│   ├── __init__.py
│   │
│   ├── scripts/                               # Scripts de utilidad
│   │   ├── __init__.py
│   │   ├── crear_indices.py                   # Creación de índices BD
│   │   ├── crear_views.py                     # Creación de VIEWS BD
│   │   ├── logging_config.py                  # Configuración de logging
│   │   ├── logging_ejemplos.py                # Ejemplos de logging
│   │   └── fileINI.py                         # Gestión de archivos INI
│   │
│   ├── modelos/
│   │   ├── __init__.py
│   │   │
│   │   ├── daos/                              # Data Access Objects (16)
│   │   │   ├── base_dao.py                    # DAO base
│   │   │   ├── conexion_sqlite.py             # Conexión a SQLite
│   │   │   ├── carrera_dao.py
│   │   │   ├── asignatura_dao.py
│   │   │   ├── estudiante_dao.py
│   │   │   ├── estudiante_carrera_dao.py
│   │   │   ├── estudiante_asignatura_dao.py
│   │   │   ├── estudiante_actividad_dao.py
│   │   │   ├── actividad_dao.py
│   │   │   ├── calendario_evento_dao.py
│   │   │   ├── prerequisito_dao.py
│   │   │   ├── tipo_actividad_dao.py
│   │   │   ├── eje_tematico_dao.py
│   │   │   ├── consulta_dao.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── dtos/                              # Data Transfer Objects
│   │   │   ├── carrera_dto.py
│   │   │   ├── asignatura_dto.py
│   │   │   ├── estudiante_dto.py
│   │   │   ├── consulta_dto.py
│   │   │   └── ... (más DTOs)
│   │   │
│   │   ├── services/                          # Business Logic (13)
│   │   │   ├── carrera_service.py
│   │   │   ├── asignatura_service.py
│   │   │   ├── estudiante_service.py
│   │   │   ├── estudiante_carrera_service.py
│   │   │   ├── estudiante_asignatura_service.py
│   │   │   ├── estudiante_actividad_service.py
│   │   │   ├── actividad_service.py
│   │   │   ├── calendario_evento_service.py
│   │   │   ├── prerequisito_service.py
│   │   │   ├── tipo_actividad_service.py
│   │   │   ├── eje_tematico_service.py
│   │   │   ├── consulta_service.py
│   │   │   └── __init__.py
│   │   │
│   │   └── controladores/                     # Controllers (13)
│   │       ├── controlar_administrar_carrera.py
│   │       ├── controlar_administrar_asignatura.py
│   │       ├── controlar_administrar_estudiante.py
│   │       ├── controlar_administrar_estudiante_carrera.py
│   │       ├── controlar_administrar_estudiante_asignatura.py
│   │       ├── controlar_administrar_estudiante_actividad.py
│   │       ├── controlar_administrar_actividad.py
│   │       ├── controlar_administrar_calendario.py
│   │       ├── controlar_administrar_prerequisitos.py
│   │       ├── controlar_administrar_tipo_actividad.py
│   │       ├── controlar_administrar_eje_tematico.py
│   │       ├── controlar_frame_principal.py
│   │       └── __init__.py
│   │
│   ├── ui/                                    # Interfaz gráfica
│   │   ├── ttk/
│   │   │   ├── appTTK.py                      # Aplicación principal
│   │   │   ├── frameCarrera.py
│   │   │   ├── frameAsignatura.py
│   │   │   ├── frameEstudiante.py
│   │   │   └── ... (más frames UI)
│   │   └── __init__.py
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
├── docs/                                      # Documentación técnica
│   ├── ACTUALIZACION_FRAME_ESTUDIANTE.md
│   ├── ANALISIS_ESTUDIANTE_ASIGNATURA.md
│   ├── CAMBIOS_IMPORTANTES.md
│   ├── FIX_ERROR_EC_SERVICE.md
│   └── ... (más documentación)
│
├── data/                                      # Datos y exportación
│   └── exported_csv/
│       ├── actividad.csv
│       ├── asignatura.csv
│       ├── carrera.csv
│       └── ... (más CSVs)
│
├── scripts/                                   # Scripts de utilidad
│   ├── consultar_bd.py
│   ├── importar_datos.py
│   ├── validar_integridad.py
│   └── ... (más scripts)
│
├── config/
│   └── settings.conf                          # Configuración de la app
│
├── logs/                                      # Logs de ejecución
│   └── (generados en runtime)
│
└── .git/                                      # Control de versiones
```

---

## 📊 Métodos Disponibles

### Services Principales

#### CarreraService
```python
obtener_todas()              # Obtener todas las carreras
obtener_por_id(id)          # Obtener carrera específica
crear(carrera_dto)          # Crear nueva carrera
actualizar(carrera_dto)     # Actualizar carrera
eliminar(id)                # Eliminar carrera
```

#### EstudianteService
```python
obtener_todos()              # Obtener todos los estudiantes
obtener_por_id(id)          # Obtener estudiante específico
crear(estudiante_dto)       # Crear nuevo estudiante
actualizar(estudiante_dto)  # Actualizar estudiante
eliminar(id)                # Eliminar estudiante
```

#### EstudianteCarreraService
```python
obtener_carrera_estudiante(id_estudiante)        # Obtener carrera del estudiante
obtener_estudiantes_carrera(id_carrera)          # Obtener estudiantes de carrera
crear_relacion(id_estudiante, id_carrera)       # Crear relación
```

#### EstudianteAsignaturaService
```python
obtener_asignaturas_estudiante(id_estudiante)      # Obtener asignaturas del estudiante
obtener_estudiantes_asignatura(id_asignatura)      # Obtener estudiantes de asignatura
crear_inscripcion(id_estudiante, id_asignatura)   # Crear inscripción
```

#### ActividadService
```python
obtener_todas()                    # Obtener todas las actividades
obtener_por_asignatura(id)        # Obtener actividades de asignatura
obtener_por_tipo(id_tipo)         # Obtener actividades por tipo
crear(actividad_dto)              # Crear actividad
actualizar(actividad_dto)         # Actualizar actividad
```

Y más services para: **Asignatura**, **CalendarioEvento**, **Prerequisito**, **TipoActividad**, **EjeTematico**, **Consulta**

---

## 🗄️ Base de Datos

### Tablas Principales (10)
- `carrera` - Carreras/Programas académicos
- `asignatura` - Asignaturas/Cursos
- `prerrequisito` - Relaciones de prerrequisitos
- `eje_tematico` - Agrupación temática
- `tipo_actividad` - Tipos de actividades
- `actividad` - Tareas y evaluaciones
- `calendario_evento` - Eventos académicos
- `estudiante` - Información de estudiantes
- `estudiante_asignatura` - Inscripción en cursos
- `estudiante_carrera` - Relación estudiante-carrera
- `estudiante_actividad` - Entrega de actividades

### Estructura de Conexión
```python
from src.modelos.daos.conexion_sqlite import ConexionSqlite

conexion = ConexionSqlite()
db = conexion.obtener_conexion()
```

### Archivos de Configuración
- **Base de datos**: `~/.local/share/cronosFacen/cronosFacen.sqlite`
- **Configuración**: `~/.config/cronosFacen/settings.conf`
- **Logs**: `~/.config/cronosFacen/cronosFacen.log`

---

## 📚 Documentación Completa

La documentación técnica se encuentra en la carpeta [docs/](docs/):

| Documento                                                                                                | Contenido                  |
| -------------------------------------------------------------------------------------------------------- | -------------------------- |
| [docs/ACTUALIZACION_FRAME_ESTUDIANTE.md](docs/ACTUALIZACION_FRAME_ESTUDIANTE.md)                         | Actualización de frames    |
| [docs/CAMBIOS_IMPORTANTES.md](docs/CAMBIOS_IMPORTANTES.md)                                               | Cambios significativos     |
| [docs/FIX_ERROR_EC_SERVICE.md](docs/FIX_ERROR_EC_SERVICE.md)                                             | Correcciones implementadas |
| [docs/modelo_sql_completo_organizacion_academica.md](docs/modelo_sql_completo_organizacion_academica.md) | Modelo SQL completo        |

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
┌──────────────────────────────────────┐
│   Interfaz Gráfica (UI/TTK)          │
│   - AppTTK (ventana principal)       │
│   - Frames (carreras, estudiantes)   │
└──────────────────────────────────────┘
         ↑
         │ utiliza
         ↓
┌──────────────────────────────────────┐
│  Controladores (13)                  │
│  - controlar_administrar_carrera     │
│  - controlar_administrar_estudiante  │
│  - ... (más controladores)           │
└──────────────────────────────────────┘
         ↑
         │ delega en
         ↓
┌──────────────────────────────────────┐
│  Services (13)                       │
│  - CarreraService                    │
│  - EstudianteService                 │
│  - EstudianteCarreraService          │
│  - ... (más services)                │
└──────────────────────────────────────┘
         ↑
         │ utiliza
         ↓
┌──────────────────────────────────────┐
│  DAOs (16)                           │
│  - CarreraDAO                        │
│  - EstudianteDAO                     │
│  - EstudianteCarreraDAO              │
│  - ... (más DAOs)                    │
└──────────────────────────────────────┘
         ↑
         │ accede a
         ↓
┌──────────────────────────────────────┐
│  Base de Datos SQLite                │
│  - 11 Tablas                         │
│  - Índices optimizados               │
└──────────────────────────────────────┘
```

---

## 🚨 Logging

Cada operación se registra automáticamente. Los logs se guardan en:
```
~/.config/cronosFacen/cronosFacen.log
```

### Ver logs en tiempo real
```bash
tail -f ~/.config/cronosFacen/cronosFacen.log
```

### Configurar nivel de logging
```python
import logging
from src.scripts.logging_config import obtener_logger

logger = obtener_logger(__name__)
logger.info("Mensaje de información")
logger.warning("Mensaje de advertencia")
logger.error("Mensaje de error")
```

---

## 📈 Casos de Uso

### 1. **Gestión de Carreras**
```python
from src.modelos.services.carrera_service import CarreraService

service = CarreraService()
carreras = service.obtener_todas()
for carrera in carreras:
    print(f"- {carrera['nombre']}")
```

### 2. **Administración de Estudiantes**
```python
from src.modelos.services.estudiante_service import EstudianteService
from src.modelos.services.estudiante_carrera_service import EstudianteCarreraService

# Obtener información del estudiante
est_service = EstudianteService()
estudiante = est_service.obtener_por_id(1)

# Obtener carrera del estudiante
ec_service = EstudianteCarreraService()
carrera = ec_service.obtener_carrera_estudiante(1)
print(f"{estudiante['nombre']} estudia {carrera['nombre']}")
```

### 3. **Control de Asignaturas**
```python
from src.modelos.services.estudiante_asignatura_service import EstudianteAsignaturaService

service = EstudianteAsignaturaService()
asignaturas = service.obtener_asignaturas_estudiante(id_estudiante=1)
print(f"Asignaturas: {len(asignaturas)}")
```

### 4. **Gestión de Actividades**
```python
from src.modelos.services.estudiante_actividad_service import EstudianteActividadService

service = EstudianteActividadService()
actividades = service.obtener_por_estudiante(id_estudiante=1)
for act in actividades:
    print(f"- {act['titulo']}: {act['fecha_entrega']}")
```

### 5. **Consultas Personalizadas**
```python
from src.modelos.services.consulta_service import ConsultaService

service = ConsultaService()
resultados = service.ejecutar_consulta("SELECT * FROM estudiante")
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

### v1.0 (Actual) ✅
- ✅ DAOs completos (16)
- ✅ Services funcionales (13)
- ✅ Controladores implementados (13)
- ✅ Interfaz gráfica TTK
- ✅ Base de datos SQLite
- ✅ Sistema de logging
- ✅ Índices de rendimiento

### v1.1 (Próximo)
- ⏳ Pruebas unitarias completas
- ⏳ Documentación de API
- ⏳ Validaciones avanzadas

### v2.0 (Futuro)
- ⏳ API REST
- ⏳ Autenticación y roles
- ⏳ Reportes PDF
- ⏳ Exportación de datos

---

## 💡 Mejores Prácticas

### Para Desarrolladores

1. **Usar siempre Services**
   ```python
   # ❌ Evitar acceso directo a DAO
   dao = CarreraDAO()
   dao.obtener_todas()
   
   # ✅ Usar Services
   service = CarreraService()
   service.obtener_todas()
   ```

2. **Validar parámetros en Services**
   ```python
   def obtener_por_id(self, id):
       if not id or id < 1:
           raise ValueError("ID debe ser mayor a 0")
       return self.dao.obtener_por_id(id)
   ```

3. **Usar logging consistentemente**
   ```python
   from src.scripts.logging_config import obtener_logger
   
   logger = obtener_logger(__name__)
   logger.info(f"Procesando carrera {id}")
   ```

4. **Manejo de errores robusto**
   ```python
   try:
       resultado = service.obtener_por_id(id)
   except ValueError as e:
       logger.error(f"Error de validación: {e}")
       return None
   except Exception as e:
       logger.error(f"Error inesperado: {e}")
       raise
   ```

5. **DTOs para transferencia de datos**
   ```python
   from src.modelos.dtos.carrera_dto import CarreraDTO
   
   carrera_dto = CarreraDTO(
       id=1,
       nombre="Ingeniería en Sistemas",
       codigo="IS001"
   )
   service.crear(carrera_dto)
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

- **Creador**: Geran17
- **Última actualización**: 6 de enero de 2026

---

## 📞 Soporte

Para reportar bugs o solicitar features:
1. Abre un issue en el repositorio
2. Incluye descripción, pasos a reproducir y comportamiento esperado
3. Adjunta logs si es relevante

---

## ✨ Estado

- **Build**: ✅ Pasando
- **Estructura**: ✅ Completa
- **Funcionalidad**: ✅ Implementada
- **Documentación**: ⏳ En progreso
- **Tests**: ⏳ En desarrollo

---

**Desarrollado con ❤️ para la educación académica**

*Para más información, consulta la carpeta [docs/](docs/) o ejecuta la aplicación con `python src/main.py`.*

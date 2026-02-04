# 🎓 cronosFacen - Sistema de Organización Académica

## 📋 Descripción

**cronosFacen** es una aplicación desktop (TTK) en Python para gestionar información académica de estudiantes, asignaturas, actividades y eventos.

Incluye:

- Gestión de carreras, asignaturas, actividades y calendarios
- Administración de estudiantes y relaciones académicas
- Control de prerequisitos y ejes temáticos
- Base de datos SQLite optimizada
- Interfaz moderna con ttkbootstrap
- Arquitectura en capas (DAO → Service → Controller)

---

## 🚀 Quick Start

### Requisitos

```bash
Python 3.12+
pip
pipenv (opcional)
```

### Instalación

```bash
pipenv install
# o
pip install -r requirements.txt
```

### Configurar base de datos (opcional)

```bash
python setup_database.py
python setup_indices.py
python setup_views.py
```

### Ejecutar

```bash
python src/main.py
```

---

## 📁 Estructura del Proyecto

```text
cronosFacen/
├── README.md
├── Pipfile
├── Pipfile.lock
├── setup_database.py
├── setup_indices.py
├── setup_views.py
├── config/
│   └── settings.conf
└── src/
    ├── main.py
    ├── configuracion/
    │   ├── __init__.py
    │   └── config_app.py
    ├── modelos/
    │   ├── daos/
    │   ├── dtos/
    │   └── services/
    ├── controladores/
    └── ui/
        └── ttk/
```

---

## ⚙️ Configuración

La configuración vive en `config/settings.conf`.

- Tema y pestañas visibles: sección `[UI]`.
- Logging: sección `[Logging]`.
- Base de datos: sección `[BaseDatos]`.

---

## 🧩 Arquitectura

```text
UI (TTK)
  ↓
Controladores
  ↓
Services
  ↓
DAOs
  ↓
SQLite
```

---

## 🗄️ Base de Datos

Tablas principales:

- carrera, asignatura, estudiante
- estudiante_asignatura, estudiante_carrera, estudiante_actividad
- actividad, tipo_actividad
- eje_tematico, prerequisito, calendario_evento

---

## 🚨 Logging

Configuración en `config/settings.conf` sección `[Logging]`.

---

## 👥 Autor

- **Creador**: Geran17
- **Última actualización**: 2026-02-04

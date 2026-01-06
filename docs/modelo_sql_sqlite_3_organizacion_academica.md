# Modelo SQL – SQLite3

Este archivo define el **modelo SQL completo adaptado a SQLite3** para una aplicación de organización académica y seguimiento del progreso del estudiante.

SQLite no soporta algunas características avanzadas (ENUM nativo, SERIAL, CHECK complejos con subconsultas), por lo que el diseño fue ajustado manteniendo **integridad lógica y claridad conceptual**.

---

## 0. Configuración recomendada

```sql
PRAGMA foreign_keys = ON;
```

---

## 1. Tabla: Carrera

```sql
CREATE TABLE carrera (
    id_carrera INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    plan TEXT NOT NULL,
     TEXT NOT NULL,
    creditos_totales INTEGER
);
```

---

## 2. Tabla: Asignatura

```sql
CREATE TABLE asignatura (
    id_asignatura INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    creditos INTEGER NOT NULL,
    horas_semanales INTEGER,
    tipo TEXT CHECK (tipo IN ('obligatoria', 'electiva')),
    id_carrera INTEGER NOT NULL,
    FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera)
        ON DELETE CASCADE
);
```

---

## 3. Tabla: Prerrequisito

```sql
CREATE TABLE prerrequisito (
    id_asignatura INTEGER NOT NULL,
    id_asignatura_prerrequisito INTEGER NOT NULL,
    PRIMARY KEY (id_asignatura, id_asignatura_prerrequisito),
    FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE,
    FOREIGN KEY (id_asignatura_prerrequisito)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE,
    CHECK (id_asignatura <> id_asignatura_prerrequisito)
);
```

---

## 4. Tabla: Eje Temático

```sql
CREATE TABLE eje_tematico (
    id_eje INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    orden INTEGER,
    id_asignatura INTEGER NOT NULL,
    FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE
);
```

---

## 5. Tabla: TipoActividad

```sql
CREATE TABLE tipo_actividad (
    id_tipo_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    siglas TEXT NOT NULL UNIQUE,
    descripcion TEXT
);
```

---

## 6. Tabla: Actividad

```sql
CREATE TABLE actividad (
    id_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    id_eje INTEGER NOT NULL,
    id_tipo_actividad INTEGER NOT NULL,
    FOREIGN KEY (id_eje)
        REFERENCES eje_tematico(id_eje)
        ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_actividad)
        REFERENCES tipo_actividad(id_tipo_actividad)
);
```

📌 Fechas almacenadas como TEXT en formato ISO `YYYY-MM-DD`.

---

## 7. Tabla: CalendarioEvento

```sql
CREATE TABLE calendario_evento (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    afecta_actividades INTEGER DEFAULT 0
);
```

---

## 8. Tabla: Estudiante

```sql
CREATE TABLE estudiante (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
);
```

📌 **Importante:** Las carreras del estudiante se gestionan a través de la tabla **EstudianteCarrera** (Sección 8.1),
que permite la relación muchos a muchos entre estudiantes y carreras.

---

## 8.1. Tabla: EstudianteCarrera

```sql
CREATE TABLE estudiante_carrera (
    id_estudiante INTEGER NOT NULL,
    id_carrera INTEGER NOT NULL,
    estado TEXT NOT NULL CHECK (
        estado IN ('activa', 'inactiva', 'suspendida', 'completada', 'abandonada')
    ),
    fecha_inscripcion TEXT NOT NULL,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    es_carrera_principal INTEGER DEFAULT 1,
    periodo_ingreso TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_estudiante, id_carrera),
    FOREIGN KEY (id_estudiante)
        REFERENCES estudiante(id_estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera)
        ON DELETE RESTRICT
);
```

**Propósito:** Permite que un estudiante pueda estar inscrito en múltiples carreras simultáneamente.

**Estados:**

- `activa`: Cursando actualmente
- `inactiva`: Temporalmente inactiva (puede reactivarse)
- `suspendida`: Suspensión formal
- `completada`: Carrera finalizada/graduado
- `abandonada`: Dejó la carrera sin completar

📌 Fechas en formato ISO `YYYY-MM-DD`.  
📄 Ver documentación completa en: `docs/modelo_sql_estudiante_carrera.md`

---

## 9. Tabla: EstudianteAsignatura

```sql
CREATE TABLE estudiante_asignatura (
    id_estudiante INTEGER NOT NULL,
    id_asignatura INTEGER NOT NULL,
    estado TEXT CHECK (
        estado IN ('no_cursada', 'cursando', 'aprobada', 'reprobada')
    ),
    nota_final REAL,
    periodo TEXT,
    PRIMARY KEY (id_estudiante, id_asignatura),
    FOREIGN KEY (id_estudiante)
        REFERENCES estudiante(id_estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE
);
```

---

## 10. Tabla: EstudianteActividad

```sql
CREATE TABLE estudiante_actividad (
    id_estudiante INTEGER NOT NULL,
    id_actividad INTEGER NOT NULL,
    estado TEXT CHECK (
        estado IN ('pendiente', 'en_progreso', 'entregada', 'vencida')
    ),
    fecha_entrega TEXT,
    PRIMARY KEY (id_estudiante, id_actividad),
    FOREIGN KEY (id_estudiante)
        REFERENCES estudiante(id_estudiante)
        ON DELETE CASCADE,
    FOREIGN KEY (id_actividad)
        REFERENCES actividad(id_actividad)
        ON DELETE CASCADE
);
```

---

## 11. Observaciones específicas de SQLite

- No existe `SERIAL`: se usa `INTEGER PRIMARY KEY AUTOINCREMENT`
- No hay `BOOLEAN`: se usa `INTEGER (0 / 1)`
- Fechas como `TEXT` en formato ISO
- `CHECK` funciona correctamente para validaciones simples

---

✅ *Este esquema es ideal para MVPs, prototipos, aplicaciones móviles, proyectos académicos y pruebas locales.*

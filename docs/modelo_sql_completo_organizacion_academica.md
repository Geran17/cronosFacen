# Modelo SQL – Organización Académica del Estudiante

Este archivo define el **modelo SQL completo**, normalizado y comentado, para una aplicación de organización académica y seguimiento del progreso de una carrera.

El diseño contempla:
- Carreras y asignaturas con prerrequisitos
- Ejes temáticos y actividades
- Tipos de actividad
- Calendario académico
- Seguimiento del progreso del estudiante

---

## 1. Tabla: Carrera
```sql
CREATE TABLE carrera (
    id_carrera SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    modalidad VARCHAR(30) NOT NULL,
    creditos_totales INT
);
```

---

## 2. Tabla: Asignatura
```sql
CREATE TABLE asignatura (
    id_asignatura SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL,
    horas_semanales INT,
    tipo VARCHAR(20) CHECK (tipo IN ('obligatoria', 'electiva')),
    id_carrera INT NOT NULL,
    CONSTRAINT fk_asignatura_carrera
        FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera)
        ON DELETE CASCADE
);
```

---

## 3. Tabla: Prerrequisito (autorrelación)
```sql
CREATE TABLE prerrequisito (
    id_asignatura INT NOT NULL,
    id_asignatura_prerrequisito INT NOT NULL,
    PRIMARY KEY (id_asignatura, id_asignatura_prerrequisito),
    CONSTRAINT fk_asignatura
        FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE,
    CONSTRAINT fk_prerrequisito
        FOREIGN KEY (id_asignatura_prerrequisito)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE,
    CONSTRAINT chk_no_autorreferencia
        CHECK (id_asignatura <> id_asignatura_prerrequisito)
);
```

---

## 4. Tabla: Eje Temático
```sql
CREATE TABLE eje_tematico (
    id_eje SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    orden INT,
    id_asignatura INT NOT NULL,
    CONSTRAINT fk_eje_asignatura
        FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE
);
```

---

## 5. Tabla: TipoActividad
```sql
CREATE TABLE tipo_actividad (
    id_tipo_actividad SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    siglas VARCHAR(5) UNIQUE NOT NULL,
    descripcion TEXT
);
```

---

## 6. Tabla: Actividad
```sql
CREATE TABLE actividad (
    id_actividad SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    id_eje INT NOT NULL,
    id_tipo_actividad INT NOT NULL,
    CONSTRAINT fk_actividad_eje
        FOREIGN KEY (id_eje)
        REFERENCES eje_tematico(id_eje)
        ON DELETE CASCADE,
    CONSTRAINT fk_actividad_tipo
        FOREIGN KEY (id_tipo_actividad)
        REFERENCES tipo_actividad(id_tipo_actividad)
);
```

---

## 7. Tabla: CalendarioEvento
```sql
CREATE TABLE calendario_evento (
    id_evento SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    afecta_actividades BOOLEAN DEFAULT FALSE
);
```

---

## 8. Tabla: Estudiante
```sql
CREATE TABLE estudiante (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    id_carrera INT NOT NULL,
    CONSTRAINT fk_estudiante_carrera
        FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera)
);
```

---

## 9. Tabla: EstudianteAsignatura (progreso académico)
```sql
CREATE TABLE estudiante_asignatura (
    id_estudiante INT NOT NULL,
    id_asignatura INT NOT NULL,
    estado VARCHAR(20) CHECK (
        estado IN ('no_cursada', 'cursando', 'aprobada', 'reprobada')
    ),
    nota_final NUMERIC(4,2),
    periodo VARCHAR(20),
    PRIMARY KEY (id_estudiante, id_asignatura),
    CONSTRAINT fk_ea_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiante(id_estudiante)
        ON DELETE CASCADE,
    CONSTRAINT fk_ea_asignatura
        FOREIGN KEY (id_asignatura)
        REFERENCES asignatura(id_asignatura)
        ON DELETE CASCADE
);
```

---

## 10. Tabla: EstudianteActividad
```sql
CREATE TABLE estudiante_actividad (
    id_estudiante INT NOT NULL,
    id_actividad INT NOT NULL,
    estado VARCHAR(20) CHECK (
        estado IN ('pendiente', 'en_progreso', 'entregada', 'vencida')
    ),
    fecha_entrega DATE,
    PRIMARY KEY (id_estudiante, id_actividad),
    CONSTRAINT fk_eact_estudiante
        FOREIGN KEY (id_estudiante)
        REFERENCES estudiante(id_estudiante)
        ON DELETE CASCADE,
    CONSTRAINT fk_eact_actividad
        FOREIGN KEY (id_actividad)
        REFERENCES actividad(id_actividad)
        ON DELETE CASCADE
);
```

---

## 11. Observaciones finales

- El modelo está **normalizado (3FN)**
- Permite evolución incremental (MVP → sistema completo)
- Soporta análisis de progreso, bloqueos por prerrequisitos y carga académica
- Es compatible con PostgreSQL (recomendado)

---

📌 *Este esquema es una base sólida tanto para implementación práctica como para defensa académica del proyecto.*


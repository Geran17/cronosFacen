# Tabla EstudianteCarrera - Relación Muchos a Muchos

## Análisis del Problema

### Situación Actual
En el modelo actual, la tabla `estudiante` tiene una relación **uno a uno** con `carrera` a través del campo `id_carrera`:

```sql
CREATE TABLE estudiante (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    id_carrera INTEGER NOT NULL,  -- ❌ Solo permite UNA carrera
    FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera)
);
```

**Limitaciones:**
- Un estudiante solo puede estar inscrito en una carrera
- No permite dobles titulaciones
- No permite cambios de carrera manteniendo el historial
- No permite carreras simultáneas

### Solución Propuesta: Tabla `estudiante_carrera`

Crear una tabla intermedia que permita **relación muchos a muchos** entre estudiantes y carreras.

---

## Diseño de la Tabla

### Estructura SQL

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

---

## Campos Explicados

| Campo                  | Tipo    | Descripción                                      | Valores/Formato                                      |
| ---------------------- | ------- | ------------------------------------------------ | ---------------------------------------------------- |
| `id_estudiante`        | INTEGER | ID del estudiante                                | FK → estudiante                                      |
| `id_carrera`           | INTEGER | ID de la carrera                                 | FK → carrera                                         |
| `estado`               | TEXT    | Estado actual de la inscripción                  | activa, inactiva, suspendida, completada, abandonada |
| `fecha_inscripcion`    | TEXT    | Fecha de inscripción formal                      | ISO: YYYY-MM-DD                                      |
| `fecha_inicio`         | TEXT    | Fecha de inicio de cursado (opcional)            | ISO: YYYY-MM-DD                                      |
| `fecha_fin`            | TEXT    | Fecha de finalización/egreso (opcional)          | ISO: YYYY-MM-DD                                      |
| `es_carrera_principal` | INTEGER | Indica si es la carrera principal del estudiante | 0 = No, 1 = Sí                                       |
| `periodo_ingreso`      | TEXT    | Periodo académico de ingreso                     | Ej: "2024-1", "2024-2"                               |
| `observaciones`        | TEXT    | Notas adicionales                                | Texto libre                                          |

---

## Estados Posibles

### `activa`
Estudiante cursando actualmente la carrera.
- **Uso:** Carrera en curso normal
- **Transiciones:** → inactiva, suspendida, completada, abandonada

### `inactiva`
Inscripción temporalmente inactiva (puede reactivarse).
- **Uso:** Estudiante tomó un receso pero planea continuar
- **Transiciones:** → activa, suspendida, abandonada

### `suspendida`
Suspensión formal por razones administrativas o académicas.
- **Uso:** Decisión institucional o del estudiante
- **Transiciones:** → activa, abandonada

### `completada`
Carrera finalizada exitosamente (graduado).
- **Uso:** Estudiante egresó/se graduó
- **Transiciones:** Estado final (no cambia)

### `abandonada`
Estudiante dejó la carrera sin completarla.
- **Uso:** Deserción o cambio definitivo
- **Transiciones:** Estado final (no cambia)

---

## Casos de Uso

### Caso 1: Estudiante con una sola carrera
```sql
INSERT INTO estudiante_carrera 
    (id_estudiante, id_carrera, estado, fecha_inscripcion, es_carrera_principal, periodo_ingreso)
VALUES 
    (1, 5, 'activa', '2024-03-01', 1, '2024-1');
```

### Caso 2: Estudiante con doble titulación
```sql
-- Carrera principal
INSERT INTO estudiante_carrera 
    (id_estudiante, id_carrera, estado, fecha_inscripcion, es_carrera_principal, periodo_ingreso)
VALUES 
    (2, 3, 'activa', '2023-03-01', 1, '2023-1');

-- Segunda carrera
INSERT INTO estudiante_carrera 
    (id_estudiante, id_carrera, estado, fecha_inscripcion, es_carrera_principal, periodo_ingreso)
VALUES 
    (2, 7, 'activa', '2024-03-01', 0, '2024-1');
```

### Caso 3: Cambio de carrera manteniendo historial
```sql
-- Carrera anterior (abandonada)
INSERT INTO estudiante_carrera 
    (id_estudiante, id_carrera, estado, fecha_inscripcion, fecha_fin, es_carrera_principal, periodo_ingreso)
VALUES 
    (3, 2, 'abandonada', '2022-03-01', '2023-12-15', 0, '2022-1');

-- Nueva carrera (activa)
INSERT INTO estudiante_carrera 
    (id_estudiante, id_carrera, estado, fecha_inscripcion, es_carrera_principal, periodo_ingreso)
VALUES 
    (3, 4, 'activa', '2024-03-01', 1, '2024-1');
```

### Caso 4: Graduación
```sql
UPDATE estudiante_carrera 
SET estado = 'completada', fecha_fin = '2024-12-20'
WHERE id_estudiante = 1 AND id_carrera = 5;
```

---

## Consultas Útiles

### Carreras activas de un estudiante
```sql
SELECT c.nombre, ec.fecha_inscripcion, ec.periodo_ingreso, ec.es_carrera_principal
FROM estudiante_carrera ec
JOIN carrera c ON ec.id_carrera = c.id_carrera
WHERE ec.id_estudiante = ? AND ec.estado = 'activa'
ORDER BY ec.es_carrera_principal DESC, ec.fecha_inscripcion;
```

### Estudiantes activos por carrera
```sql
SELECT e.nombre, e.correo, ec.fecha_inscripcion, ec.periodo_ingreso
FROM estudiante_carrera ec
JOIN estudiante e ON ec.id_estudiante = e.id_estudiante
WHERE ec.id_carrera = ? AND ec.estado = 'activa'
ORDER BY ec.fecha_inscripcion;
```

### Historial completo de un estudiante
```sql
SELECT c.nombre, ec.estado, ec.fecha_inscripcion, ec.fecha_inicio, ec.fecha_fin
FROM estudiante_carrera ec
JOIN carrera c ON ec.id_carrera = c.id_carrera
WHERE ec.id_estudiante = ?
ORDER BY ec.fecha_inscripcion DESC;
```

---

## Reglas de Negocio

### Restricciones Recomendadas

1. **Carrera principal única:** Un estudiante solo puede tener una carrera con `es_carrera_principal = 1` en estado `activa`
2. **Fechas coherentes:** `fecha_fin` debe ser posterior a `fecha_inscripcion`
3. **Estados finales:** Los estados `completada` y `abandonada` no deberían cambiar
4. **Carrera activa:** Al menos una carrera activa si el estudiante está cursando

### Validaciones a Nivel de Aplicación

```python
def validar_carrera_principal_unica(id_estudiante):
    """Verificar que solo hay una carrera principal activa"""
    sql = """
        SELECT COUNT(*) as count 
        FROM estudiante_carrera 
        WHERE id_estudiante = ? 
        AND estado = 'activa' 
        AND es_carrera_principal = 1
    """
    # Debe retornar count = 1

def validar_fechas(fecha_inscripcion, fecha_fin):
    """Validar coherencia de fechas"""
    if fecha_fin and fecha_inscripcion:
        return fecha_fin >= fecha_inscripcion
    return True
```

---

## Migración del Modelo Actual

### ⚠️ Cambio Importante: Eliminación de id_carrera

A partir de esta versión, la tabla `estudiante` **ya no contiene** el campo `id_carrera`. 
Todas las relaciones estudiante-carrera se gestionan exclusivamente a través de la tabla `estudiante_carrera`.

### Proceso de Migración (Bases de Datos Existentes)

Si tienes una base de datos con la estructura antigua (con `id_carrera` en `estudiante`):

#### Paso 1: Migrar datos a estudiante_carrera

```bash
python scripts/migrar_estudiante_carrera.py
```

Este script:
- Crea la tabla `estudiante_carrera` si no existe
- Copia los datos de `estudiante.id_carrera` a `estudiante_carrera`
- Marca todas las carreras como 'activa' y 'principal'

#### Paso 2: Eliminar campo id_carrera (Opcional pero recomendado)

```bash
python scripts/eliminar_id_carrera_estudiante.py
```

Este script:
- ⚠️ Crea un backup automático de la base de datos
- Elimina el campo `id_carrera` de la tabla `estudiante`
- Verifica la integridad después de la migración
- **Es una operación irreversible** (pero hay backup)

**Uso con confirmación:**
```bash
# Solicita confirmación antes de ejecutar
python scripts/eliminar_id_carrera_estudiante.py

# Ejecutar sin confirmación (usar con precaución)
python scripts/eliminar_id_carrera_estudiante.py --force
```

### Estructura Nueva (Actual)

```sql
-- Tabla estudiante (SIN id_carrera)
CREATE TABLE estudiante (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
);

-- Tabla estudiante_carrera (relación muchos a muchos)
CREATE TABLE estudiante_carrera (
    id_estudiante INTEGER NOT NULL,
    id_carrera INTEGER NOT NULL,
    estado TEXT NOT NULL,
    fecha_inscripcion TEXT NOT NULL,
    -- ... otros campos
    PRIMARY KEY (id_estudiante, id_carrera),
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera) ON DELETE RESTRICT
);
```

### Compatibilidad de Código

**Antes (código antiguo):**
```python
# ❌ Ya no funciona
estudiante = EstudianteDTO(
    nombre="Juan Pérez",
    correo="juan@email.com",
    id_carrera=5  # Este campo ya no existe
)
estudiante_dao.insertar(estudiante)
```

**Ahora (código nuevo):**
```python
from modelos.services.estudiante_carrera_service import EstudianteCarreraService

# 1. Crear estudiante (sin carrera)
estudiante = EstudianteDTO(
    nombre="Juan Pérez",
    correo="juan@email.com"
)
id_estudiante = estudiante_dao.insertar(estudiante)

# 2. Asignar carrera(s) usando EstudianteCarreraService
ec_service = EstudianteCarreraService()
dto_carrera = EstudianteCarreraDTO(
    id_estudiante=id_estudiante,
    id_carrera=5,
    estado='activa',
    fecha_inscripcion='2024-03-01',
    es_carrera_principal=1,
    periodo_ingreso='2024-1'
)
ec_service.inscribir_estudiante(dto_carrera)
```

---

## Índices Recomendados

```sql
-- Búsqueda por estudiante
CREATE INDEX idx_estudiante_carrera_estudiante 
ON estudiante_carrera(id_estudiante);

-- Búsqueda por carrera
CREATE INDEX idx_estudiante_carrera_carrera 
ON estudiante_carrera(id_carrera);

-- Búsqueda por estado
CREATE INDEX idx_estudiante_carrera_estado 
ON estudiante_carrera(estado);

-- Búsqueda de carrera principal activa
CREATE INDEX idx_estudiante_carrera_principal_activa 
ON estudiante_carrera(id_estudiante, es_carrera_principal, estado);
```

---

## Ventajas de este Diseño

✅ **Flexibilidad:** Permite múltiples carreras por estudiante  
✅ **Historial:** Mantiene registro de carreras anteriores  
✅ **Estados:** Gestión completa del ciclo de vida de la inscripción  
✅ **Escalabilidad:** Fácil agregar nuevos campos (becas, modalidad, etc.)  
✅ **Integridad:** Relaciones bien definidas con CASCADE y RESTRICT  
✅ **Consultas:** Permite análisis de cambios de carrera, tasas de graduación, etc.  

---

## Extensiones Futuras

Campos adicionales que podrían agregarse:

- `modalidad`: TEXT (presencial, virtual, semipresencial)
- `turno`: TEXT (mañana, tarde, noche)
- `sede`: TEXT (si la universidad tiene múltiples sedes)
- `creditos_reconocidos`: INTEGER (créditos convalidados de otra carrera)
- `promedio_acumulado`: REAL (promedio en esta carrera específica)
- `semestre_actual`: INTEGER (semestre que está cursando)

---

✅ **Este diseño es compatible con SQLite3 y sigue las convenciones del proyecto actual.**

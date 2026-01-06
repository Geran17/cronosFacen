# Índices Recomendados – SQLite (MVP Organización Académica)

Este documento define los **índices recomendados para SQLite3** basados en:
- el modelo de datos
- las consultas SQL del MVP
- el volumen esperado (MVP / prototipo)

El objetivo es **mejorar rendimiento sin sobre–optimizar**.

---

## 1. Principios usados

Antes de crear índices como loco 😅, seguimos estas reglas:

- Indexar **claves foráneas** usadas en JOINs
- Indexar columnas usadas en **WHERE**, **ORDER BY** y **GROUP BY**
- No indexar tablas muy chicas de catálogo innecesariamente
- Evitar índices redundantes (SQLite ya indexa PK automáticamente)

---

## 2. Índices por entidad

---

### 📘 Carrera

🔹 No requiere índices adicionales
- Tabla pequeña
- Acceso mayormente por PK

---

### 📗 Asignatura

Usada en:
- joins con carrera
- prerrequisitos
- progreso del estudiante

```sql
CREATE INDEX idx_asignatura_carrera
ON asignatura (id_carrera);
```

```sql
CREATE INDEX idx_asignatura_codigo
ON asignatura (codigo);
```

---

### 🔗 Prerrequisito

Tabla crítica para habilitaciones y bloqueos.

```sql
CREATE INDEX idx_prerrequisito_asignatura
ON prerrequisito (id_asignatura);
```

```sql
CREATE INDEX idx_prerrequisito_requisito
ON prerrequisito (id_asignatura_prerrequisito);
```

---

### 📚 Eje Temático

```sql
CREATE INDEX idx_eje_asignatura
ON eje_tematico (id_asignatura);
```

---

### 📝 TipoActividad

🔹 No requiere índices extra
- Tabla catálogo
- Muy pocos registros

---

### 🧩 Actividad

Usada intensivamente en calendario y dashboard.

```sql
CREATE INDEX idx_actividad_eje
ON actividad (id_eje);
```

```sql
CREATE INDEX idx_actividad_fechas
ON actividad (fecha_inicio, fecha_fin);
```

```sql
CREATE INDEX idx_actividad_tipo
ON actividad (id_tipo_actividad);
```

---

### 🗓️ CalendarioEvento

```sql
CREATE INDEX idx_evento_fechas
ON calendario_evento (fecha_inicio, fecha_fin);
```

---

### 👤 Estudiante

```sql
CREATE INDEX idx_estudiante_carrera
ON estudiante (id_carrera);
```

---

### 🎓 EstudianteAsignatura

Tabla **clave para progreso**.

```sql
CREATE INDEX idx_ea_estudiante
ON estudiante_asignatura (id_estudiante);
```

```sql
CREATE INDEX idx_ea_asignatura
ON estudiante_asignatura (id_asignatura);
```

```sql
CREATE INDEX idx_ea_estado
ON estudiante_asignatura (estado);
```

---

### 📌 EstudianteActividad

Tabla clave para pendientes y vencidas.

```sql
CREATE INDEX idx_eact_estudiante
ON estudiante_actividad (id_estudiante);
```

```sql
CREATE INDEX idx_eact_actividad
ON estudiante_actividad (id_actividad);
```

```sql
CREATE INDEX idx_eact_estado
ON estudiante_actividad (estado);
```

---

## 3. Índices compuestos recomendados (MVP+)

Solo si el volumen empieza a crecer:

```sql
CREATE INDEX idx_eact_estudiante_estado
ON estudiante_actividad (id_estudiante, estado);
```

```sql
CREATE INDEX idx_actividad_tipo_fecha
ON actividad (id_tipo_actividad, fecha_fin);
```

---

## 4. Índices que NO conviene crear (por ahora)

🚫 Índices sobre columnas TEXT libres (descripcion)
🚫 Índices duplicando PK
🚫 Índices en tablas catálogo chicas

---

## 5. Recomendaciones prácticas SQLite

- Ejecutar `ANALYZE;` tras cargar datos
- Usar `EXPLAIN QUERY PLAN` para validar uso de índices
- No crear índices "por si acaso"
- Menos índices = más velocidad en INSERT/UPDATE

---

## 6. Conclusión

Este set de índices:
- acelera todas las consultas del MVP
- mantiene SQLite liviano
- permite crecer sin rediseñar

📌 *Optimización justa, sin paranoia prematura.*


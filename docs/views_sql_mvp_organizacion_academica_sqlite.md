# VIEWS SQL – MVP Organización Académica (SQLite3)

Este documento define las **VIEWS del MVP**, creadas a partir de las consultas clave ya diseñadas.

Las VIEWS permiten:
- simplificar el código de la aplicación
- centralizar la lógica SQL
- mejorar legibilidad y mantenimiento

Todas las vistas están pensadas para **SQLite3**.

---

## 1. Vista: Progreso general del estudiante

Resume el avance del estudiante en su carrera.

```sql
CREATE VIEW vw_progreso_estudiante AS
SELECT
    ea.id_estudiante,
    a.id_carrera,
    COUNT(a.id_asignatura) AS total_asignaturas,
    SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END) AS asignaturas_aprobadas,
    ROUND(
        100.0 * SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END)
        / COUNT(a.id_asignatura),
        2
    ) AS porcentaje_avance
FROM asignatura a
LEFT JOIN estudiante_asignatura ea
    ON a.id_asignatura = ea.id_asignatura
GROUP BY ea.id_estudiante, a.id_carrera;
```

---

## 2. Vista: Asignaturas habilitadas para cursar

Devuelve las asignaturas cuyos prerrequisitos están aprobados.

```sql
CREATE VIEW vw_asignaturas_habilitadas AS
SELECT a.id_asignatura,
       a.nombre,
       ea.id_estudiante
FROM asignatura a
JOIN estudiante ea
WHERE a.id_asignatura NOT IN (
    SELECT p.id_asignatura
    FROM prerrequisito p
    LEFT JOIN estudiante_asignatura eas
        ON p.id_asignatura_prerrequisito = eas.id_asignatura
       AND eas.id_estudiante = ea.id_estudiante
    WHERE eas.estado IS NULL OR eas.estado <> 'aprobada'
);
```

---

## 3. Vista: Asignaturas bloqueadas

```sql
CREATE VIEW vw_asignaturas_bloqueadas AS
SELECT DISTINCT
    a.id_asignatura,
    a.nombre,
    ea.id_estudiante
FROM asignatura a
JOIN prerrequisito p
    ON a.id_asignatura = p.id_asignatura
JOIN estudiante ea
LEFT JOIN estudiante_asignatura eas
    ON p.id_asignatura_prerrequisito = eas.id_asignatura
   AND eas.id_estudiante = ea.id_estudiante
WHERE eas.estado IS NULL OR eas.estado <> 'aprobada';
```

---

## 4. Vista: Actividades pendientes del estudiante

```sql
CREATE VIEW vw_actividades_pendientes AS
SELECT
    ea.id_estudiante,
    act.id_actividad,
    act.titulo,
    act.fecha_fin,
    ta.siglas AS tipo,
    COALESCE(ea.estado, 'pendiente') AS estado
FROM actividad act
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad;
```

---

## 5. Vista: Actividades vencidas

```sql
CREATE VIEW vw_actividades_vencidas AS
SELECT
    ea.id_estudiante,
    act.id_actividad,
    act.titulo,
    act.fecha_fin
FROM actividad act
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad
WHERE act.fecha_fin < DATE('now')
  AND (ea.estado IS NULL OR ea.estado <> 'entregada');
```

---

## 6. Vista: Actividades de la semana

```sql
CREATE VIEW vw_actividades_semana AS
SELECT
    act.id_actividad,
    act.titulo,
    act.fecha_inicio,
    act.fecha_fin,
    ta.siglas AS tipo
FROM actividad act
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad
WHERE act.fecha_inicio BETWEEN DATE('now') AND DATE('now', '+7 days');
```

---

## 7. Vista: Actividades por asignatura

```sql
CREATE VIEW vw_actividades_por_asignatura AS
SELECT
    a.id_asignatura,
    a.nombre AS asignatura,
    act.id_actividad,
    act.titulo,
    act.fecha_fin,
    ta.nombre AS tipo_actividad
FROM actividad act
JOIN eje_tematico e
    ON act.id_eje = e.id_eje
JOIN asignatura a
    ON e.id_asignatura = a.id_asignatura
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad;
```

---

## 8. Vista: Calendario unificado

Combina actividades y eventos académicos.

```sql
CREATE VIEW vw_calendario_unificado AS
SELECT
    id_actividad AS id,
    titulo,
    fecha_inicio,
    fecha_fin,
    'actividad' AS origen
FROM actividad
UNION ALL
SELECT
    id_evento AS id,
    titulo,
    fecha_inicio,
    fecha_fin,
    'evento' AS origen
FROM calendario_evento;
```

---

## 9. Vista: Dashboard rápido del estudiante

```sql
CREATE VIEW vw_dashboard_estudiante AS
SELECT
    ea.id_estudiante,
    COUNT(*) AS total_actividades,
    SUM(CASE WHEN ea.estado = 'entregada' THEN 1 ELSE 0 END) AS entregadas,
    SUM(CASE WHEN act.fecha_fin < DATE('now') THEN 1 ELSE 0 END) AS vencidas
FROM actividad act
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad
GROUP BY ea.id_estudiante;
```

---

## 10. Observaciones importantes

- SQLite no permite parámetros dentro de VIEWS
- El filtrado por `id_estudiante` se realiza en la consulta a la vista
- Estas VIEWS son **read-only**
- Ideales para alimentar UI y dashboards

---

📌 *Con estas VIEWS, el MVP queda completamente desacoplado de SQL complejo.*


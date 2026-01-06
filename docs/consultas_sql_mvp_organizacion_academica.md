# Consultas SQL – MVP Organización Académica

Este documento define las **consultas SQL clave del MVP**, alineadas con los casos de uso y el backlog técnico.

Las consultas están pensadas para **SQLite3**, pero son fácilmente adaptables a otros motores.

---

## 1. Progreso general de la carrera

### 1.1 Total de asignaturas de la carrera
```sql
SELECT COUNT(*) AS total_asignaturas
FROM asignatura
WHERE id_carrera = :id_carrera;
```

---

### 1.2 Asignaturas aprobadas por el estudiante
```sql
SELECT COUNT(*) AS asignaturas_aprobadas
FROM estudiante_asignatura
WHERE id_estudiante = :id_estudiante
  AND estado = 'aprobada';
```

---

### 1.3 Porcentaje de avance de la carrera
```sql
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN ea.estado = 'aprobada' THEN 1 ELSE 0 END)
        / COUNT(a.id_asignatura),
        2
    ) AS porcentaje_avance
FROM asignatura a
LEFT JOIN estudiante_asignatura ea
    ON a.id_asignatura = ea.id_asignatura
   AND ea.id_estudiante = :id_estudiante
WHERE a.id_carrera = :id_carrera;
```

---

## 2. Asignaturas habilitadas para cursar

### 2.1 Asignaturas cuyos prerrequisitos están aprobados
```sql
SELECT a.id_asignatura, a.nombre
FROM asignatura a
WHERE a.id_asignatura NOT IN (
    SELECT p.id_asignatura
    FROM prerrequisito p
    LEFT JOIN estudiante_asignatura ea
        ON p.id_asignatura_prerrequisito = ea.id_asignatura
       AND ea.id_estudiante = :id_estudiante
    WHERE ea.estado IS NULL OR ea.estado <> 'aprobada'
);
```

📌 Devuelve solo asignaturas **sin bloqueos por prerrequisitos**.

---

## 3. Asignaturas bloqueadas

```sql
SELECT DISTINCT a.id_asignatura, a.nombre
FROM asignatura a
JOIN prerrequisito p
    ON a.id_asignatura = p.id_asignatura
LEFT JOIN estudiante_asignatura ea
    ON p.id_asignatura_prerrequisito = ea.id_asignatura
   AND ea.id_estudiante = :id_estudiante
WHERE ea.estado IS NULL OR ea.estado <> 'aprobada';
```

---

## 4. Actividades pendientes del estudiante

```sql
SELECT act.id_actividad,
       act.titulo,
       act.fecha_fin,
       ta.siglas AS tipo
FROM actividad act
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad
   AND ea.id_estudiante = :id_estudiante
WHERE ea.estado IS NULL
   OR ea.estado IN ('pendiente', 'en_progreso')
ORDER BY act.fecha_fin;
```

---

## 5. Actividades vencidas

```sql
SELECT act.id_actividad,
       act.titulo,
       act.fecha_fin
FROM actividad act
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad
   AND ea.id_estudiante = :id_estudiante
WHERE act.fecha_fin < DATE('now')
  AND (ea.estado IS NULL OR ea.estado <> 'entregada');
```

---

## 6. Actividades de la semana

```sql
SELECT act.titulo,
       act.fecha_inicio,
       act.fecha_fin,
       ta.siglas
FROM actividad act
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad
WHERE act.fecha_inicio BETWEEN DATE('now') AND DATE('now', '+7 days')
ORDER BY act.fecha_inicio;
```

---

## 7. Actividades por asignatura

```sql
SELECT act.titulo,
       act.fecha_fin,
       ta.nombre AS tipo
FROM actividad act
JOIN eje_tematico e
    ON act.id_eje = e.id_eje
JOIN asignatura a
    ON e.id_asignatura = a.id_asignatura
JOIN tipo_actividad ta
    ON act.id_tipo_actividad = ta.id_tipo_actividad
WHERE a.id_asignatura = :id_asignatura
ORDER BY act.fecha_fin;
```

---

## 8. Resumen semanal (dashboard)

```sql
SELECT
    COUNT(*) AS total_actividades,
    SUM(CASE WHEN ea.estado = 'entregada' THEN 1 ELSE 0 END) AS entregadas,
    SUM(CASE WHEN act.fecha_fin < DATE('now') THEN 1 ELSE 0 END) AS vencidas
FROM actividad act
LEFT JOIN estudiante_actividad ea
    ON act.id_actividad = ea.id_actividad
   AND ea.id_estudiante = :id_estudiante;
```

---

## 9. Calendario académico (eventos + actividades)

```sql
SELECT titulo, fecha_inicio, fecha_fin, 'actividad' AS origen
FROM actividad
UNION ALL
SELECT titulo, fecha_inicio, fecha_fin, 'evento' AS origen
FROM calendario_evento
ORDER BY fecha_inicio;
```

---

## 10. Observaciones finales

- Todas las consultas son **read-only**
- Pensadas para alimentar dashboards y vistas
- No requieren lógica compleja en la aplicación
- Optimizables con índices si el proyecto crece

---

📌 *Estas consultas cubren el 100% de los casos de uso del MVP.*


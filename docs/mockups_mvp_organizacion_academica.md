# Mockups del MVP – Organización Académica del Estudiante

Este documento presenta los **mockups del MVP** en formato **textual/Markdown**, pensados como guía clara para el desarrollo de la interfaz.

Los mockups **no son diseño gráfico**, sino una representación estructural de:
- qué pantallas existen
- qué información muestran
- qué datos (VIEWS) las alimentan

---

## 1. Pantalla: Dashboard (Inicio)

### Objetivo
Dar una visión rápida del estado académico general del estudiante.

### Datos utilizados
- `vw_progreso_estudiante`
- `vw_dashboard_estudiante`

### Mockup
```
--------------------------------------------------
 PROGRESO DE LA CARRERA
--------------------------------------------------
 Avance: 42 %
 Asignaturas aprobadas: 10 / 24

--------------------------------------------------
 RESUMEN DE ACTIVIDADES
--------------------------------------------------
 Pendientes: 5
 Entregadas: 12
 Vencidas: 1
--------------------------------------------------
```

---

## 2. Pantalla: Asignaturas de la Carrera

### Objetivo
Visualizar el mapa de la carrera y el estado de cada asignatura.

### Datos utilizados
- `vw_asignaturas_habilitadas`
- `vw_asignaturas_bloqueadas`
- `estudiante_asignatura`

### Mockup
```
--------------------------------------------------
 ASIGNATURAS
--------------------------------------------------
 [✓] Álgebra I              (Aprobada)
 [→] Álgebra II             (Habilitada)
 [~] Cálculo I              (Cursando)
 [×] Probabilidad I         (Bloqueada)
--------------------------------------------------
 Leyenda:
 ✓ Aprobada   → Habilitada   ~ Cursando   × Bloqueada
--------------------------------------------------
```

---

## 3. Pantalla: Detalle de Asignatura

### Objetivo
Ver el detalle interno de una asignatura.

### Datos utilizados
- `vw_actividades_por_asignatura`

### Mockup
```
--------------------------------------------------
 ASIGNATURA: Álgebra II
--------------------------------------------------
 Estado: Habilitada

 Actividades:
 [AA] Ejercicios Unidad 1     12/04  Pendiente
 [AF] Cuestionario 1          15/04  Vencida
 [AI] Foro de discusión       18/04  Pendiente
--------------------------------------------------
```

---

## 4. Pantalla: Actividades

### Objetivo
Gestionar las actividades académicas del estudiante.

### Datos utilizados
- `vw_actividades_pendientes`
- `vw_actividades_vencidas`

### Mockup
```
--------------------------------------------------
 ACTIVIDADES
--------------------------------------------------
 [AA] Ejercicios 3.1     12/04   Pendiente
 [AI] Foro Semana 4      13/04   En progreso
 [AF] Cuestionario 2     14/04   Vencida
--------------------------------------------------
 Filtros: [ Todas | Pendientes | Vencidas ]
--------------------------------------------------
```

---

## 5. Pantalla: Calendario Académico

### Objetivo
Visualizar actividades y eventos en una línea temporal.

### Datos utilizados
- `vw_calendario_unificado`

### Mockup
```
--------------------------------------------------
 CALENDARIO (Vista Semanal)
--------------------------------------------------
 L  M  X  J  V  S  D
 1  2  3  4  5  6  7
       [AF]
          [Evento]
--------------------------------------------------
 Leyenda:
 [AF] Actividad de Fijación
 [Evento] Evento académico
--------------------------------------------------
```

---

## 6. Navegación mínima del MVP

```
[ Dashboard ] [ Asignaturas ] [ Actividades ] [ Calendario ]
```

---

## 7. Relación Mockup ↔ Backend

| Pantalla        | Fuente de datos (VIEW)            |
|-----------------|-----------------------------------|
| Dashboard       | vw_progreso_estudiante            |
|                 | vw_dashboard_estudiante           |
| Asignaturas     | vw_asignaturas_habilitadas        |
|                 | vw_asignaturas_bloqueadas         |
| Detalle materia | vw_actividades_por_asignatura     |
| Actividades     | vw_actividades_pendientes         |
| Calendario      | vw_calendario_unificado           |

---

## 8. Observaciones finales

- Estos mockups definen **estructura y flujo**, no diseño visual
- Son suficientes para implementar el MVP completo
- Permiten dividir tareas frontend/backend sin ambigüedad

📌 *Con estos mockups, el desarrollo deja de ser abstracto y pasa a ser ejecutable.*


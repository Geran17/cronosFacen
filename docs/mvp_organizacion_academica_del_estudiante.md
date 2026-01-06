# MVP – Aplicación de Organización Académica del Estudiante

Este documento define el **MVP (Minimum Viable Product)** de la aplicación, estableciendo **alcance, funcionalidades mínimas, reglas de negocio y pautas técnicas** para guiar el desarrollo sin desviarse ni sobredimensionar el proyecto.

La idea es simple:
> *Ayudar a un estudiante a saber qué tiene que hacer, cuándo y cómo progresa en su carrera.*

---

## 1. Objetivo del MVP

El MVP debe permitir que un estudiante:

- Visualice su **carrera y asignaturas**
- Registre el **estado de cursado** de cada asignatura
- Organice y controle sus **actividades académicas**
- Observe su **progreso general** sin cálculos manuales

Todo lo demás es mejora futura.

---

## 2. Alcance funcional (qué SÍ incluye)

### 2.1 Gestión académica básica

✔ Visualizar una **carrera**
✔ Listar **asignaturas** de la carrera
✔ Ver **prerrequisitos** de cada asignatura
✔ Marcar asignaturas como:

- no cursada
- cursando
- aprobada
- reprobada

---

### 2.2 Progreso del estudiante

✔ Calcular:

- cantidad de asignaturas aprobadas
- porcentaje de avance de la carrera
✔ Identificar asignaturas **habilitadas** para cursar (prerrequisitos cumplidos)
✔ Identificar asignaturas **bloqueadas**

---

### 2.3 Organización de actividades

✔ Listar actividades por:

- asignatura
- eje temático
- semana
✔ Clasificar actividades por **TipoActividad** (AA, AF, AI)
✔ Marcar actividades como:
- pendiente
- en progreso
- entregada
- vencida

---

### 2.4 Calendario académico

✔ Visualizar eventos relevantes:

- exámenes
- cierres
- feriados
✔ Mostrar actividades sobre una **línea temporal**
✔ Detectar actividades vencidas

---

## 3. Fuera del alcance del MVP (NO hacer ahora)

🚫 Autenticación avanzada
🚫 Multiusuario simultáneo
🚫 Sincronización en la nube
🚫 Recomendaciones automáticas
🚫 Notificaciones push
🚫 Gestión de docentes

> *Si entra todo eso, ya no es MVP… es tesis 😄*

---

## 4. Entidades mínimas del MVP

El MVP utiliza solo las entidades necesarias:

- Carrera
- Asignatura
- Prerrequisito
- Estudiante
- EstudianteAsignatura
- EjeTematico
- Actividad
- TipoActividad
- EstudianteActividad
- CalendarioEvento

👉 Todas ya definidas en el modelo SQL.

---

## 5. Casos de uso mínimos

### CU01 – Ver progreso de la carrera

El estudiante puede:
- ver total de asignaturas
- ver cuántas están aprobadas
- ver porcentaje de avance

---

### CU02 – Ver asignaturas habilitadas

El sistema:
- analiza prerrequisitos
- muestra asignaturas que puede cursar

---

### CU03 – Gestionar actividades

El estudiante puede:
- ver actividades pendientes
- marcar una actividad como entregada
- identificar vencidas

---

### CU04 – Vista semanal

El sistema muestra:
- actividades de la semana
- eventos del calendario

---

## 6. Reglas de negocio del MVP

- Una asignatura **solo se habilita** si todos sus prerrequisitos están aprobados
- Una actividad vencida no cambia automáticamente a entregada
- El progreso se mide **solo por asignaturas aprobadas**
- Las fechas se interpretan en formato ISO (YYYY-MM-DD)

---

## 7. Arquitectura sugerida (simple y realista)

### Base de datos

- SQLite3
- Modelo normalizado
- Datos locales

### Backend (opcional)

- Python / Node.js
- Acceso directo a SQLite

### Frontend

- Web simple o app de escritorio
- Vistas clave:
  - Dashboard
  - Asignaturas
  - Actividades
  - Calendario

---

## 8. Métricas de éxito del MVP

El MVP es exitoso si el estudiante:

✔ sabe qué tiene pendiente
✔ entiende su progreso
✔ evita olvidos
✔ puede planificar la semana

Si logra eso, **misión cumplida** 🎯

---

## 9. Evolución futura (post-MVP)

- Recomendaciones de cursado
- Predicción de carga académica
- Alertas automáticas
- Sincronización
- Visualización tipo mapa de carrera

---

📌 *Este MVP prioriza claridad, foco y valor real para el estudiante, evitando complejidad innecesaria en la primera etapa.*

# Backlog Técnico – MVP Organización Académica

Este backlog define las **tareas técnicas mínimas y ordenadas** necesarias para implementar el MVP de la aplicación de organización académica del estudiante.

El enfoque es incremental, realista y alineado al modelo de datos y al MVP previamente definido.

---

## 🧱 Épica 1: Fundamentos del Proyecto

### Tarea 1.1 – Definir stack tecnológico
- Seleccionar lenguaje principal (ej: Python, Java, JS)
- Definir tipo de aplicación (desktop / web / CLI)
- Definir framework si aplica

**Resultado:** stack documentado y coherente con SQLite

---

### Tarea 1.2 – Inicializar repositorio
- Crear estructura base del proyecto
- Configurar control de versiones
- Definir convenciones básicas

**Resultado:** proyecto inicial funcional

---

## 🗄️ Épica 2: Base de Datos

### Tarea 2.1 – Implementar esquema SQLite
- Crear base SQLite
- Ejecutar script SQL del modelo
- Verificar claves foráneas

**Resultado:** base creada sin errores

---

### Tarea 2.2 – Datos iniciales (seed)
- Insertar Tipos de Actividad
- Insertar Asignaturas de ejemplo
- Insertar una Carrera base

**Resultado:** datos mínimos para pruebas

---

## 📚 Épica 3: Gestión Académica

### Tarea 3.1 – ABM de Asignaturas
- Crear asignatura
- Listar asignaturas
- Editar datos básicos

**Resultado:** gestión básica de materias

---

### Tarea 3.2 – Prerrequisitos
- Asociar prerrequisitos entre asignaturas
- Validar dependencias

**Resultado:** grafo académico consistente

---

### Tarea 3.3 – Progreso del estudiante
- Marcar asignaturas como cursadas/aprobadas
- Calcular porcentaje de avance

**Resultado:** visualización simple de progreso

---

## 🗓️ Épica 4: Actividades y Calendario

### Tarea 4.1 – Gestión de Actividades
- Crear actividad
- Asociar tipo de actividad
- Asociar asignatura

**Resultado:** actividades registradas correctamente

---

### Tarea 4.2 – Calendario
- Listar actividades por fecha
- Filtrar por asignatura o tipo

**Resultado:** agenda académica funcional

---

## 📊 Épica 5: Consultas Clave (Core del MVP)

### Tarea 5.1 – Consultas SQL principales
- Actividades de la semana
- Asignaturas pendientes
- Asignaturas habilitadas por prerrequisito

**Resultado:** consultas reutilizables

---

## 🖥️ Épica 6: Interfaz Mínima

### Tarea 6.1 – Pantalla principal
- Resumen de progreso
- Próximas actividades

---

### Tarea 6.2 – Pantalla de gestión
- Asignaturas
- Actividades

**Resultado:** interacción básica con el sistema

---

## ✅ Épica 7: Validaciones y Calidad

### Tarea 7.1 – Validaciones de negocio
- No permitir aprobar sin prerrequisitos
- Fechas válidas

---

### Tarea 7.2 – Pruebas básicas
- Pruebas manuales
- Casos borde

**Resultado:** MVP estable

---

## 🚀 Entregable Final del MVP

- Base SQLite funcional
- Gestión de asignaturas y actividades
- Visualización de progreso
- Calendario académico simple

---

👉 **Todo lo que no esté en este backlog queda fuera del MVP.**

(El enemigo natural del estudiante: el scope creep 😄)

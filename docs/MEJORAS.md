# Sugerencias de Mejoramiento (Roadmap por Etapas)

Este documento describe mejoras útiles para estudiantes y una propuesta de implementación por etapas. La idea es priorizar impacto, reducir riesgo y habilitar funcionalidades en orden lógico.

## Objetivo General

Elevar la utilidad diaria para el estudiante: mejor visibilidad de plazos, menos olvidos, mejor organización y evidencia de progreso.

## Etapa 1: Utilidad inmediata (bajo riesgo, alto impacto)

Enfocada en mejoras rápidas, sin cambios profundos en base de datos.

### 1. Notificaciones locales

**Qué aporta**  
Alertas visibles cuando una actividad está por vencer.

**Implementación**  

1. Crear un servicio de notificaciones locales (OS o pop-up).  
2. Agregar una tarea periódica (timer) que revise eventos próximos.  
3. Definir un umbral por defecto (ej: 1 día).  

**Dependencias**  
Ninguna.

### 2. Búsqueda global de actividades

**Qué aporta**  
Encontrar rápidamente actividades por título, asignatura o estado.

**Implementación**  

1. Campo de búsqueda en pestaña Actividades.  
2. Filtrado en memoria sobre `lista_actividades_detalladas`.  
3. Opción para limpiar búsqueda y ver todo.  

**Dependencias**  
Ninguna.

### 3. Vista semanal/mensual de carga

**Qué aporta**  
Permite al estudiante ver cuántas actividades tiene por semana.

**Implementación**

1. En pestaña Dashboard, agregar un resumen por semana.  
2. Contabilizar actividades por rango de fechas.  
3. Mostrar en gráfico simple o tabla.  

**Dependencias**  
Datos de fechas ya disponibles.

## Etapa 2: Organización avanzada (medio riesgo, medio impacto)

Introduce mejoras que requieren ajustes de modelos o UI más compleja.

### 4. Etiquetas o categorías personalizadas

**Qué aporta**  
Permite agrupar actividades por temas personales (ej: “parcial”, “grupo”, “importante”).

**Implementación**  

1. Crear tabla `etiquetas`.  
2. Relación actividad-etiqueta (many-to-many).  
3. UI para asignar etiquetas en el administrador de actividades.  

**Dependencias**  
Migración de base de datos.

### 5. Priorización automática por urgencia

**Qué aporta**  
Orden automático por urgencia y nivel de impacto.

**Implementación**  

1. Calcular puntuación (días restantes + prioridad).  
2. Ordenar lista por puntaje.  
3. Añadir opción de “Orden automático”.  

**Dependencias**  
Disponibilidad de fecha fin y prioridad.

### 6. Historial de cambios en actividades

**Qué aporta**  
Ver cuándo cambió el estado o fecha de entrega.

**Implementación**  

1. Crear tabla `actividad_historial`.  
2. Registrar cada cambio en estado o fecha.  
3. Vista en detalle desde la tarjeta de actividad.  

**Dependencias**  
Migración de base de datos.

## Etapa 3: Productividad y colaboración (alto impacto, mayor esfuerzo)

Funciones más avanzadas y con más dependencia externa.

### 7. Exportación a calendario (ICS / Google Calendar)

**Qué aporta**  
Sincronizar fechas con el calendario personal.

**Implementación**

1. Generar archivo `.ics` con eventos.  
2. Botón “Exportar Calendario”.  
3. En futuro, API para Google Calendar.  

**Dependencias**  
Librería para ICS o módulo propio.

### 8. Reportes y exportación (PDF/Excel)

**Qué aporta**  
Entregables para estudiante o tutor.

**Implementación**  

1. Exportar progreso y estadísticas.  
2. Generación de PDF con gráfico de avance.  
3. Exportar tablas a Excel.  

**Dependencias**  
Librerías de exportación (pdf/Excel).

### 9. Adjuntos por actividad

**Qué aporta**  
Guardar archivos relevantes (guías, PDFs, links).

**Implementación**  

1. Carpeta de adjuntos en la app.  
2. Tabla `actividad_adjuntos`.  
3. Botón “Adjuntar archivo” en actividad.  

**Dependencias**  
Gestión de archivos local.

## Etapa 4: Ecosistema y nube (máximo impacto, mayor complejidad)

Pensado para crecimiento a largo plazo.

### 10. Backups en la nube

**Qué aporta**  
Evita pérdida de datos y permite acceso desde otros dispositivos.

**Implementación**  

1. Configurar backend de backup (Drive, Dropbox).  
2. Autenticación OAuth.  
3. Subidas automáticas programadas.  

**Dependencias**  
API externa.

### 11. Modo estudiante simplificado

**Qué aporta**  
Vista limpia con solo actividades, alertas y calendario.

**Implementación**  

1. Configuración de perfiles (admin vs estudiante).  
2. Ocultar administradores y opciones avanzadas.  
3. Personalizar home para estudiante.  

**Dependencias**  
Separación de roles.

### 12. Recordatorios personalizados

**Qué aporta**  
Cada estudiante define cuándo quiere ser avisado.

**Implementación**  

1. Guardar preferencias por usuario.  
2. Programar recordatorios con diferentes umbrales.  
3. Mostrar configuración simple en UI.  

**Dependencias**  
Notificaciones base ya implementadas.

## Notas finales

- Se recomienda implementar una etapa completa antes de pasar a la siguiente.  
- Cada etapa debe cerrar con pruebas básicas y feedback de usuarios reales.  
- Priorizar la estabilidad de la base de datos antes de funciones de nube.

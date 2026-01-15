# Mejoras Implementadas: Filtrado y Visualización de Asignaturas

## Cambios Realizados

### 1. **Mejora de Columnas en la Tabla**
- Se agregaron anchos predefinidos y minwidth para mejor control de visualización
- Columna "Asignatura" configurada como expandible (stretch: True) con minwidth de 200px
- Las demás columnas tienen anchos fijos para mejor presentación

**Configuración de columnas:**
- Código: 80px (fijo)
- Asignatura: Expandible con mínimo de 200px
- Créditos: 70px (fijo)
- Estado: 120px (fijo)
- Nota: 60px (fijo)
- Período: 80px (fijo)

### 2. **Mejora de Filtros**
#### Filtro de Búsqueda:
- Ahora con etiqueta más descriptiva: "🔎 Buscar por código/nombre:"
- Ancho ampliado (25 caracteres) para mejor usabilidad
- Tooltip mejorado explicando que es en tiempo real

#### Filtro por Estado:
- Etiqueta más visible con fuente bold
- Separador visual entre filtros para mejor legibilidad
- Estados con emojis para mejor identificación:
  - 🔵 No cursada
  - 🟡 Cursando
  - 🟢 Aprobada
  - 🔴 Reprobada

#### Nuevo Botón "Limpiar Filtros":
- Botón "🔄 Limpiar" para restablecer todos los filtros
- Limpia tanto la búsqueda como el filtro de estado
- Permite volver rápidamente a la vista completa

### 3. **Funcionalidad de Filtrado**
El filtrado ya estaba implementado en el controlador y ahora funciona mejor con:
- Búsqueda en tiempo real por código o nombre de asignatura
- Filtrado por estado del registro
- Combinación de ambos filtros simultáneamente
- Botón para limpiar todos los filtros de una vez

### 4. **Ajuste Automático de Columnas**
- Ya estaba implementado `autofit_columns()` en el controlador
- Se ejecuta automáticamente después de cada actualización de tabla
- Las columnas se ajustan al contenido de manera óptima

## Cómo Usar

### Filtrar por Asignatura:
1. Escribe en el campo "Buscar" el código o nombre de la asignatura
2. La tabla se filtrará automáticamente en tiempo real
3. Acepta búsquedas parciales (ej: "MAT" busca todas las matemáticas)

### Filtrar por Estado:
1. Selecciona un estado en el combobox "Estado"
2. La tabla mostrará solo asignaturas con ese estado

### Combinación de Filtros:
1. Puedes usar búsqueda Y estado juntos
2. Ejemplo: Buscar "Programación" y filtrar por "🟢 Aprobada"

### Limpiar Filtros:
1. Presiona el botón "🔄 Limpiar"
2. Se limpiarán todos los filtros automáticamente
3. Se mostrarán todas las asignaturas nuevamente

## Archivos Modificados

1. **frame_administrar_estudiante_asignatura.py**
   - Mejora en la configuración de columnas de la tabla
   - Mejora en los controles de filtro (búsqueda y estado)
   - Nuevo botón para limpiar filtros

2. **controlar_administrar_estudiante_asignatura.py**
   - Nuevo método `_on_limpiar_filtros()` para el botón
   - Configuración del evento del botón de limpiar filtros

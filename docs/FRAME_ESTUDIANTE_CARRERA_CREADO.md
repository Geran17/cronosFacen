# ✅ Frame Administrar Estudiante-Carrera Creado

## 📋 Resumen

Se ha creado exitosamente el frame `FrameAdministrarEstudianteCarrera` con 487 líneas de código, siguiendo el mismo diseño y estructura de los otros frames de administración del proyecto.

---

## 📁 Archivo Creado

**`src/ui/ttk/frames/frame_administrar_estudiante_carrera.py`** (487 líneas)

---

## 🎨 Estructura del Frame

### Componentes Principales

El frame está dividido en 4 secciones principales:

1. **Frame Superior** - Título del módulo
2. **Frame Selector** - Selector de estudiante
3. **Frame Central** - Tabla y formulario (60/40)
4. **Frame Inferior** - Estadísticas

---

## 🔧 Variables (StringVar/IntVar)

### Variables de Estudiante
- `var_id_estudiante` (IntVar) - ID del estudiante seleccionado
- `var_nombre_estudiante` (StringVar) - Nombre completo del estudiante

### Variables de Carrera
- `var_id_carrera` (IntVar) - ID de la carrera seleccionada
- `var_nombre_carrera` (StringVar) - Nombre de la carrera

### Variables de Inscripción
- `var_estado` (StringVar) - Estado (activa, inactiva, suspendida, completada, abandonada)
- `var_fecha_inscripcion` (StringVar) - Fecha de inscripción (YYYY-MM-DD)
- `var_fecha_inicio` (StringVar) - Fecha de inicio (opcional)
- `var_fecha_fin` (StringVar) - Fecha de finalización (opcional)
- `var_es_principal` (IntVar) - Si es carrera principal (0/1)
- `var_periodo_ingreso` (StringVar) - Periodo académico (ej: 2024-1)

### Variables de Filtro
- `var_filtro_estado` (StringVar) - Filtro de estado para la tabla

---

## 📊 Widgets Principales

### Frame Selector de Estudiante

```
┌───────────────────────────────────────────────┐
│ 👤 Selección de Estudiante                   │
├───────────────────────────────────────────────┤
│ Estudiante: [▼ Juan Pérez - juan@email.com] [🔄] │
└───────────────────────────────────────────────┘
```

**Componentes:**
- `cbx_estudiante` - Combobox con lista de estudiantes
- `btn_refrescar_estudiante` - Botón para recargar lista

---

### Panel Izquierdo: Tabla de Carreras (60%)

```
┌─────────────────────────────────────────────┐
│ 📚 Carreras del Estudiante                  │
├─────────────────────────────────────────────┤
│ Filtrar: [▼ Todos]      💡 Doble clic...   │
├──────┬───────┬────────┬────────┬──────┬────┤
│ID Est│ID Car.│Carrera │Estado  │Prin. │F.In│
├──────┼───────┼────────┼────────┼──────┼────┤
│  1   │  5    │Ing.Inf │activa  │  ⭐  │2024│
│  1   │  3    │Matemát.│activa  │  ☆   │2024│
└──────┴───────┴────────┴────────┴──────┴────┘
```

**Componentes:**
- `cbx_filtro_estado` - Filtro por estado
- `tabla_carreras` - Tableview con 7 columnas
  - ID Estudiante
  - ID Carrera
  - Nombre Carrera
  - Estado
  - Es Principal (⭐/☆)
  - Fecha Inscripción
  - Periodo

---

### Panel Derecho: Formulario (40%)

```
┌──────────────────────────────────────────┐
│ 📝 Detalles de la Inscripción           │
├──────────────────────────────────────────┤
│ ID Estudiante: [1]                      │
│                                          │
│ 🎓 Carrera:                              │
│ [▼ Ingeniería Informática]              │
│                                          │
│ 📊 Estado:                               │
│ [▼ activa]                               │
│                                          │
│ 📅 Fecha Inscripción:                    │
│ [2024-03-01]                             │
│                                          │
│ 📅 Fecha Inicio (opcional):              │
│ [2024-03-15]                             │
│                                          │
│ 📅 Fecha Fin (opcional):                 │
│ [        ]                               │
│                                          │
│ [⭐ Es Carrera Principal]                │
│                                          │
│ 📆 Periodo Ingreso:                      │
│ [2024-1]                                 │
│                                          │
│ 📝 Observaciones:                        │
│ [                        ] │             │
│ [________________________] │             │
│ [________________________]_│             │
│                                          │
│ [➕ Nuevo][💾 Guardar][🗑️ Eliminar]    │
│ [🔄 Cambiar Estado][🎓 Completar]       │
└──────────────────────────────────────────┘
```

**Componentes:**

1. **entry_id_estudiante** - ID del estudiante (readonly)
2. **cbx_carrera** - Combobox para seleccionar carrera
3. **cbx_estado** - Combobox con 5 estados
4. **entry_fecha_inscripcion** - Fecha obligatoria
5. **entry_fecha_inicio** - Fecha opcional
6. **entry_fecha_fin** - Fecha opcional
7. **chk_es_principal** - Toggle button para carrera principal
8. **entry_periodo** - Periodo de ingreso
9. **text_observaciones** - Text widget con scrollbar

**Botones Principales:**
- `btn_nuevo` - Limpiar formulario
- `btn_aplicar` - Guardar inscripción
- `btn_eliminar` - Eliminar inscripción

**Botones Adicionales:**
- `btn_cambiar_estado` - Cambiar estado rápidamente
- `btn_completar` - Marcar como completada

---

## 🎯 Funcionalidades Especiales

### 1. Toggle de Carrera Principal

El botón `chk_es_principal` funciona como toggle:

```python
def _toggle_principal(self):
    """Toggle del estado de carrera principal"""
    nuevo_valor = 0 if self.var_es_principal.get() == 1 else 1
    self.var_es_principal.set(nuevo_valor)
    
    # Actualizar apariencia
    if nuevo_valor == 1:
        self.chk_es_principal.config(
            text="⭐ Es Carrera Principal",
            bootstyle="warning"  # Amarillo lleno
        )
    else:
        self.chk_es_principal.config(
            text="☆ No es Principal",
            bootstyle="warning-outline"  # Amarillo outline
        )
```

**Estados visuales:**
- ✅ Principal: `⭐ Es Carrera Principal` (botón amarillo lleno)
- ☐ No Principal: `☆ No es Principal` (botón amarillo outline)

---

### 2. Filtro Dinámico por Estado

El combobox `cbx_filtro_estado` permite filtrar la tabla:
- **Todos** - Mostrar todas las inscripciones
- **activa** - Solo carreras activas
- **inactiva** - Solo carreras inactivas
- **suspendida** - Solo carreras suspendidas
- **completada** - Solo carreras completadas (graduados)
- **abandonada** - Solo carreras abandonadas

---

### 3. Text Widget con Scrollbar

Para observaciones largas:
```python
self.text_observaciones = Text(
    frame_text,
    height=3,
    wrap=WORD,
    font=("Helvetica", 9),
)
scrollbar = Scrollbar(frame_text, command=self.text_observaciones.yview)
self.text_observaciones.config(yscrollcommand=scrollbar.set)
```

---

## 🔗 Integración con Controlador

El frame espera un controlador `ControlarAdministrarEstudianteCarrera` con:

```python
ControlarAdministrarEstudianteCarrera(
    master=self,
    map_vars=self.map_vars,     # Diccionario de variables
    map_widgets=self.map_widgets, # Diccionario de widgets
)
```

### Widgets Disponibles en map_widgets

```python
{
    'cbx_estudiante': Combobox,
    'btn_refrescar_estudiante': Button,
    'cbx_filtro_estado': Combobox,
    'tabla_carreras': Tableview,
    'entry_id_estudiante': Entry,
    'cbx_carrera': Combobox,
    'cbx_estado': Combobox,
    'entry_fecha_inscripcion': Entry,
    'entry_fecha_inicio': Entry,
    'entry_fecha_fin': Entry,
    'chk_es_principal': Button,
    'entry_periodo': Entry,
    'text_observaciones': Text,
    'btn_nuevo': Button,
    'btn_aplicar': Button,
    'btn_eliminar': Button,
    'btn_cambiar_estado': Button,
    'btn_completar': Button,
    'lbl_estadisticas': Label,
}
```

---

## 📋 Tooltips Implementados

- **cbx_estudiante**: "Seleccione un estudiante para ver sus carreras"
- **btn_refrescar_estudiante**: "Refrescar lista de estudiantes"
- **cbx_carrera**: "Seleccione la carrera a inscribir"
- **entry_fecha_inscripcion**: "Formato: YYYY-MM-DD"
- **entry_fecha_inicio**: "Formato: YYYY-MM-DD (opcional)"
- **entry_fecha_fin**: "Formato: YYYY-MM-DD (opcional)"
- **chk_es_principal**: "Marcar como carrera principal del estudiante (solo una puede ser principal)"
- **entry_periodo**: "Ej: 2024-1, 2024-2"

---

## 🎨 Estilos Utilizados

### Bootstyle Colors

- **primary** - Azul (selector, tabla, labelframes)
- **info** - Cyan (título, campos de formulario)
- **success** - Verde (botón Nuevo, Completar)
- **warning** - Amarillo (carrera principal)
- **danger** - Rojo (botón Eliminar)
- **secondary** - Gris (campos opcionales, filtros)

### Tamaños de Fuente

- **Título**: 16pt bold
- **Labels principales**: 10pt bold
- **Labels secundarios**: 9pt
- **Labels info**: 9pt italic
- **Text widget**: 9pt

---

## 📊 Columnas de la Tabla

| #   | Nombre         | Ancho | Stretch | Alineación |
| --- | -------------- | ----- | ------- | ---------- |
| 1   | ID Est.        | 60px  | No      | Derecha    |
| 2   | ID Car.        | 60px  | No      | Derecha    |
| 3   | Carrera        | Auto  | Sí      | Izquierda  |
| 4   | Estado         | 100px | No      | Centro     |
| 5   | Principal      | 80px  | No      | Centro     |
| 6   | F. Inscripción | 100px | No      | Centro     |
| 7   | Periodo        | 80px  | No      | Centro     |

---

## 🚀 Próximo Paso

### Crear el Controlador

Ahora se debe crear:

**`src/controladores/controlar_administrar_estudiante_carrera.py`**

Con las siguientes funcionalidades:

1. **Carga de datos:**
   - Cargar lista de estudiantes
   - Cargar lista de carreras
   - Cargar inscripciones del estudiante seleccionado

2. **CRUD:**
   - Insertar nueva inscripción
   - Actualizar inscripción existente
   - Eliminar inscripción

3. **Operaciones especiales:**
   - Cambiar estado de inscripción
   - Completar carrera (cambiar a "completada" + fecha fin)
   - Validar carrera principal única

4. **Eventos:**
   - Cambio de estudiante → Recargar tabla
   - Cambio de filtro → Filtrar tabla
   - Doble click en tabla → Cargar formulario
   - Click en botones → Ejecutar acciones

---

## ✅ Características del Frame

- ✅ 487 líneas de código bien estructurado
- ✅ Diseño responsive (60/40)
- ✅ Tooltips informativos
- ✅ Iconos visuales (emoji)
- ✅ Filtros dinámicos
- ✅ Tabla paginada y buscable
- ✅ Validaciones visuales
- ✅ Toggle button para carrera principal
- ✅ Text widget con scroll para observaciones
- ✅ Botones de acción claramente identificados
- ✅ Estructura modular y mantenible
- ✅ Sigue convenciones del proyecto

---

✅ **El frame FrameAdministrarEstudianteCarrera está listo y esperando su controlador.**

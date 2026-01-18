# Análisis de Estructura BD y Vistas para Frame Carreras

## 📊 Análisis de la Estructura de Base de Datos

### Tablas Relevantes

```
carrera
├── id_carrera (PK)
├── nombre
├── plan
├── modalidad
└── creditos_totales

asignatura
├── id_asignatura (PK)
├── codigo
├── nombre
├── creditos
├── semestre (1-8)
├── id_carrera (FK)
└── tipo (obligatoria/electiva)

estudiante_asignatura
├── id_estudiante (FK)
├── id_asignatura (FK)
├── estado (no_cursada/cursando/aprobada/reprobada)
├── nota_final
└── periodo

eje_tematico
├── id_eje (PK)
├── nombre
├── id_asignatura (FK)
└── orden

actividad
├── id_actividad (PK)
├── titulo
├── id_eje (FK)
└── id_tipo_actividad

estudiante_actividad
├── id_estudiante (FK)
├── id_actividad (FK)
├── estado (pendiente/en_progreso/entregada/vencida)
└── fecha_entrega

prerrequisito
├── id_asignatura (FK)
└── id_asignatura_prerrequisito (FK)

estudiante_carrera
├── id_estudiante (FK)
├── id_carrera (FK)
├── estado (activa/inactiva/completada)
├── es_carrera_principal
└── fecha_inscripcion
```

---

## 🎯 Vistas Creadas para Frame Carreras

### VISTA 1: `vw_carreras_estudiante`
**Función**: Obtener carreras del estudiante con información agregada

**Datos que proporciona**:
- Nombre y plan de la carrera
- Estado de la carrera (activa/inactiva/completada)
- Indicador si es carrera principal
- Total de asignaturas en la carrera
- % de progreso general

**Uso en Frame**:
```python
SELECT * FROM vw_carreras_estudiante 
WHERE id_estudiante = ? AND es_carrera_principal = 1
```

---

### VISTA 2: `vw_asignaturas_estudiante_completo`
**Función**: Proporciona TODOS los datos necesarios para las tarjetas de asignatura

**Datos por asignatura**:
```
✓ Nombre de la asignatura
✓ Código
✓ Semestre (agrupa tarjetas)
✓ Tipo (obligatoria/electiva)
✓ Créditos
✓ Estado (cursando, aprobada, etc.)
✓ Nota final
✓ Cantidad de ejes temáticos
✓ Cantidad de actividades TOTALES
✓ Prerequisitos (concatenados)
✓ % Progreso de actividades
```

**Consulta recomendada**:
```python
sql = """
SELECT * FROM vw_asignaturas_estudiante_completo 
WHERE id_estudiante = ? AND id_carrera = ?
ORDER BY semestre, nombre_asignatura
"""
```

**Resultado**: Directamente listo para crear tarjetas

---

### VISTA 3: `vw_asignatura_prerequisitos`
**Función**: Prerequisitos de cada asignatura

**Datos**:
- `prerequisitos`: String concatenado "Asig1, Asig2, Asig3"
- `cantidad_prerequisitos`: Número de prerequisitos

---

### VISTA 4: `vw_progreso_actividades_estudiante`
**Función**: Calcula % de progreso de actividades

**Datos**:
- `total_actividades`: Número total
- `actividades_entregadas`: Completadas
- `porcentaje_progreso`: 0-100%

---

### VISTA 5: `vw_asignaturas_semestre_detalle`
**Función**: Agrupa asignaturas por semestre

**Datos**:
- Semestre como agrupador
- Información completa de cada asignatura

---

## 🔄 Flujo de Datos Recomendado

```
┌─────────────────────────────────┐
│ Usuario Selecciona Estudiante   │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│ Controlador: _cargar_carreras()            │
│ SELECT * FROM vw_carreras_estudiante       │
│ WHERE id_estudiante = ?                    │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ Usuario Selecciona Carrera      │
└─────────────┬───────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────┐
│ Controlador: _cargar_asignaturas()              │
│ SELECT * FROM vw_asignaturas_estudiante_completo│
│ WHERE id_estudiante = ? AND id_carrera = ?     │
│ ORDER BY semestre                              │
└─────────────┬────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Frame Agrupa por Semestre        │
│ {1: [asig1, asig2, ...],         │
│  2: [asig3, asig4, ...]}         │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Frame Crea Tarjetas:             │
│ Semestre 1 | Asignatura 1        │
│            | Asignatura 2        │
│            | Asignatura 3        │
│            |                      │
│ Semestre 2 | Asignatura 4        │
│            | Asignatura 5        │
└──────────────────────────────────┘
```

---

## 💾 Campos Disponibles por Tarjeta

### Tarjeta de Semestre
```
numero_semestre: a.semestre
progreso_semestre: PROMEDIO(nota_final de asignaturas del semestre)
```

### Tarjeta de Asignatura
**De vw_asignaturas_estudiante_completo**:
```
Encabezado:
  • nombre_asignatura
  • estado (icono + texto)
  • nota_final

Contenido:
  • cantidad_ejes_tematicos (🎯 Ejes: X)
  • cantidad_actividades (✔️ Actividades: X)

Barra de Progreso:
  • progreso_actividades (0-100%)

Prerequisitos:
  • prerequisitos (si != '-')
  • cantidad_prerequisitos
```

---

## 🚀 Implementación Recomendada

### Paso 1: Actualizar Controlador
```python
def _cargar_asignaturas_carrera(self, id_estudiante: int, id_carrera: int):
    dao = AsignaturaDAO(ruta_db=None)
    sql = """
    SELECT * FROM vw_asignaturas_estudiante_completo
    WHERE id_estudiante = ? AND id_carrera = ?
    ORDER BY semestre, nombre_asignatura
    """
    resultados = dao.ejecutar_consulta(sql, (id_estudiante, id_carrera))
    
    # Agrupar por semestre
    for asig in resultados:
        semestre = asig['semestre']
        # Calcular progreso del semestre
        # Crear lista de asignaturas por semestre
```

### Paso 2: Frame usa datos del controlador
```python
def mostrar_asignaturas(self):
    asignaturas = self.controlador.obtener_asignaturas_carrera()
    
    for semestre, asignaturas_lista in asignaturas.items():
        self.crear_semestre_con_asignaturas(
            numero_semestre=semestre,
            porcentaje=calcular_progreso(asignaturas_lista),
            asignaturas=asignaturas_lista
        )
```

### Paso 3: Mapear campos del diccionario
```python
asignatura_dict = {
    'nombre': resultado['nombre_asignatura'],
    'ejes_tematicos': resultado['cantidad_ejes_tematicos'],
    'actividades': resultado['cantidad_actividades'],
    'nota': resultado['nota_final'],
    'prerequisitos': resultado['prerequisitos'],
    'estado': resultado['estado'],
    'progreso_actividades': resultado['progreso_actividades']
}
```

---

## ✅ Resumen de Vistas Disponibles

| Vista                                  | Propósito                        | Filas |
| -------------------------------------- | -------------------------------- | ----- |
| `vw_carreras_estudiante`               | Carreras del estudiante          | 1-N   |
| `vw_asignaturas_estudiante_completo`   | Asignaturas con todos los datos  | 1-N   |
| `vw_asignatura_prerequisitos`          | Prerequisitos concatenados       | 1-N   |
| `vw_progreso_actividades_estudiante`   | % Progreso por asignatura        | 1-N   |
| `vw_asignaturas_semestre_detalle`      | Asignaturas agrupadas            | 1-N   |
| `vw_estudiante_actividades_detalladas` | Actividades completas            | 1-N   |
| `vw_estudiante_asignatura_carrera`     | Relación E-A-C                   | 1-N   |
| `vw_eventos_unificados`                | Eventos calendario + actividades | 1-N   |

---

## 📝 Próximos Pasos

1. ✅ Vistas creadas en BD
2. ⏳ Actualizar `ControladorCarreras` para usar vistas
3. ⏳ Modificar Frame para cargar datos reales
4. ⏳ Remover tarjetas de prueba
5. ⏳ Integrar eventos de cambio de estudiante/carrera

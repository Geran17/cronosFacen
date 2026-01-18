# Vistas SQL para Frame Carreras

Este documento describe las vistas creadas específicamente para soportar el frame de carreras y la visualización de información del estudiante, carreras y asignaturas.

---

## 📋 Vistas Creadas

### 1. `vw_carreras_estudiante`
**Propósito**: Obtener todas las carreras de un estudiante con información agregada.

**Columnas principales**:
- `id_estudiante`: ID del estudiante
- `id_carrera`: ID de la carrera
- `nombre_carrera`: Nombre de la carrera
- `plan`: Plan de estudios
- `modalidad`: Modalidad de la carrera
- `estado_carrera`: Estado (activa, inactiva, completada, etc.)
- `es_carrera_principal`: 1 si es carrera principal, 0 si no
- `total_asignaturas`: Total de asignaturas en la carrera
- `porcentaje_progreso_carrera`: % de progreso completado

**Consulta de ejemplo**:
```sql
SELECT * FROM vw_carreras_estudiante 
WHERE id_estudiante = 1 AND es_carrera_principal = 1;
```

---

### 2. `vw_asignaturas_estudiante_completo`
**Propósito**: Obtener todas las asignaturas de un estudiante con detalles completos para mostrar en tarjetas.

**Columnas principales**:
- `id_estudiante`: ID del estudiante
- `id_asignatura`: ID de la asignatura
- `nombre_asignatura`: Nombre de la asignatura
- `semestre`: Número de semestre (1-8)
- `estado`: Estado de la asignatura (cursando, aprobada, reprobada, etc.)
- `nota_final`: Nota obtenida (0-100)
- `cantidad_ejes_tematicos`: Número de ejes temáticos
- `cantidad_actividades`: Número total de actividades
- `prerequisitos`: Asignaturas prerequisitos separadas por coma
- `progreso_actividades`: % de actividades completadas (0-100)

**Consulta de ejemplo**:
```sql
SELECT * FROM vw_asignaturas_estudiante_completo 
WHERE id_estudiante = 1 AND id_carrera = 1
ORDER BY semestre;
```

---

### 3. `vw_asignatura_prerequisitos`
**Propósito**: Obtener los prerequisitos de cada asignatura de forma agregada.

**Columnas principales**:
- `id_asignatura`: ID de la asignatura
- `prerequisitos`: String con nombres de prerequisitos separados por coma
- `cantidad_prerequisitos`: Número de prerequisitos

**Consulta de ejemplo**:
```sql
SELECT prerequisitos FROM vw_asignatura_prerequisitos 
WHERE id_asignatura = 5;
```

---

### 4. `vw_progreso_actividades_estudiante`
**Propósito**: Calcular el porcentaje de progreso de actividades por estudiante y asignatura.

**Columnas principales**:
- `id_estudiante`: ID del estudiante
- `id_asignatura`: ID de la asignatura
- `total_actividades`: Número total de actividades
- `actividades_entregadas`: Actividades completadas/entregadas
- `porcentaje_progreso`: % de progreso (0-100)

**Consulta de ejemplo**:
```sql
SELECT * FROM vw_progreso_actividades_estudiante 
WHERE id_estudiante = 1 AND id_asignatura = 10;
```

---

### 5. `vw_asignaturas_semestre_detalle`
**Propósito**: Obtener asignaturas agrupadas por semestre con información detallada.

**Columnas principales**:
- `id_asignatura`: ID de la asignatura
- `id_carrera`: ID de la carrera
- `nombre_asignatura`: Nombre de la asignatura
- `semestre`: Número de semestre
- `cantidad_ejes_tematicos`: Número de ejes
- `cantidad_actividades`: Número de actividades
- `estado_asignatura`: Estado de la asignatura
- `nota_final`: Nota obtenida

---

## 🔧 Cómo usar en el Controlador

### Cargar Asignaturas por Carrera y Estudiante

```python
from modelos.daos.asignatura_dao import AsignaturaDAO

def cargar_asignaturas_carrera(id_estudiante: int, id_carrera: int) -> Dict[int, List[Dict]]:
    """
    Carga todas las asignaturas agrupadas por semestre.
    
    Returns:
        Dict con semestre como clave y lista de asignaturas como valor
    """
    dao = AsignaturaDAO(ruta_db=None)
    
    sql = """
    SELECT 
        semestre,
        id_asignatura,
        nombre_asignatura,
        codigo,
        tipo,
        creditos,
        estado,
        nota_final,
        cantidad_ejes_tematicos,
        cantidad_actividades,
        prerequisitos,
        progreso_actividades
    FROM vw_asignaturas_estudiante_completo
    WHERE id_estudiante = ? AND id_carrera = ?
    ORDER BY semestre, nombre_asignatura
    """
    
    resultados = dao.ejecutar_consulta(sql, (id_estudiante, id_carrera))
    
    # Agrupar por semestre
    asignaturas_por_semestre = {}
    for asig in resultados:
        semestre = asig['semestre']
        if semestre not in asignaturas_por_semestre:
            asignaturas_por_semestre[semestre] = []
        asignaturas_por_semestre[semestre].append(asig)
    
    return asignaturas_por_semestre
```

### Obtener Información Completa del Estudiante y Carrera

```python
def obtener_carrera_estudiante_completa(id_estudiante: int, id_carrera: int) -> Dict:
    """
    Obtiene información completa de la carrera del estudiante.
    
    Returns:
        Dict con información de la carrera, progreso y asignaturas por semestre
    """
    dao = CarreraDAO(ruta_db=None)
    
    # 1. Obtener información de la carrera
    sql_carrera = """
    SELECT * FROM vw_carreras_estudiante
    WHERE id_estudiante = ? AND id_carrera = ?
    LIMIT 1
    """
    carrera = dao.ejecutar_consulta(sql_carrera, (id_estudiante, id_carrera))
    
    if not carrera:
        return None
    
    carrera_info = carrera[0]
    
    # 2. Obtener asignaturas agrupadas por semestre
    asignaturas_por_semestre = cargar_asignaturas_carrera(id_estudiante, id_carrera)
    
    return {
        'carrera': carrera_info,
        'asignaturas_por_semestre': asignaturas_por_semestre
    }
```

---

## 📊 Información para las Tarjetas

### Tarjeta de Semestre
- Número del semestre (de la asignatura)
- Porcentaje de progreso general del semestre

### Tarjeta de Asignatura
Datos obtenidos de `vw_asignaturas_estudiante_completo`:
- `nombre_asignatura`: Nombre
- `estado`: Estado
- `nota_final`: Nota
- `cantidad_ejes_tematicos`: Ejes
- `cantidad_actividades`: Actividades totales
- `prerequisitos`: Prerrequisitos
- `progreso_actividades`: % de progreso

---

## 🔄 Flujo de Datos Recomendado

```
Usuario selecciona Estudiante
    ↓
Cargar carreras del estudiante (vw_carreras_estudiante)
    ↓
Usuario selecciona Carrera
    ↓
Cargar asignaturas completas (vw_asignaturas_estudiante_completo)
    ↓
Agrupar por semestre
    ↓
Mostrar tarjetas de semestres con asignaturas
```

---

## ⚠️ Notas Importantes

1. Las vistas usan `LEFT JOIN` para asegurar que se muestren asignaturas aunque no haya actividades registradas.
2. El `progreso_actividades` se calcula como: (actividades_entregadas / total_actividades) * 100
3. Los prerequisitos se concatenan en un string separado por comas.
4. Las vistas filtran automáticamente por estado y calculan automáticamente porcentajes.

---

## 🚀 Crear las Vistas

Para crear todas las vistas ejecutar:

```bash
python -m src.scripts.crear_views
```

Esto creará/actualizará todas las vistas en la base de datos SQLite.

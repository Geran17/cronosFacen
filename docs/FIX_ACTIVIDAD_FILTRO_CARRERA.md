# Fix: Filtro de Carrera en Administrador de Actividades

## Problemas Corregidos

### 1. Error: 'EjeTematicoDAO' object has no attribute 'obtener_por_id'
**Causa:** El método `obtener_por_id` no existía en `EjeTematicoDAO`

**Solución:** Agregado método `obtener_por_id` en:
- `/src/modelos/daos/eje_tematico_dao.py`
- `/src/modelos/daos/asignatura_dao.py`
- `/src/modelos/daos/carrera_dao.py`

```python
def obtener_por_id(self, id_xxx: int) -> Optional[XXXDTO]:
    """Obtiene un registro por su ID."""
    dto = XXXDTO(id_xxx=id_xxx)
    if self.instanciar(dto):
        return dto
    return None
```

### 2. Error: no such column: a.id_eje_tematico
**Causa:** La consulta SQL usaba nombres de columna incorrectos

**Corrección en:** `/src/controladores/controlar_administrar_actividad.py`

**Antes:**
```sql
INNER JOIN eje_tematico et ON a.id_eje_tematico = et.id_eje_tematico
```

**Después:**
```sql
INNER JOIN eje_tematico et ON a.id_eje = et.id_eje
```

### 3. Error al usar .get() en DTOs
**Causa:** El método `obtener_por_id` devuelve DTOs, no diccionarios

**Corrección en:** `_obtener_nombre_carrera()`

**Antes:**
```python
id_asignatura = eje.get('id_asignatura')
id_carrera = asignatura.get('id_carrera')
return carrera.get('nombre', 'N/A')
```

**Después:**
```python
id_asignatura = eje.id_asignatura
id_carrera = asignatura.id_carrera
return carrera.nombre
```

## Archivos Modificados

1. `/src/modelos/daos/eje_tematico_dao.py` - Agregado `obtener_por_id()`
2. `/src/modelos/daos/asignatura_dao.py` - Agregado `obtener_por_id()`
3. `/src/modelos/daos/carrera_dao.py` - Agregado `obtener_por_id()`
4. `/src/controladores/controlar_administrar_actividad.py` - Corregida consulta SQL y uso de DTOs

## Funcionalidad Implementada

✅ Filtro de actividades por carrera funcional
✅ Muestra nombre de carrera en la tabla de actividades
✅ Opción "Todas las carreras" para ver sin filtrar
✅ Métodos `obtener_por_id` disponibles en todos los DAOs necesarios

## Pruebas

El filtro ahora funciona correctamente:
- Seleccionar "Todas las carreras" muestra todas las actividades
- Seleccionar una carrera específica filtra solo las actividades de esa carrera
- La columna "Carrera" muestra el nombre correcto obtenido a través de: Actividad → Eje → Asignatura → Carrera

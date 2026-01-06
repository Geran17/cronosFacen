# ⚠️ CAMBIOS IMPORTANTES: Eliminación de id_carrera de Estudiante

## 📋 Resumen de Cambios

Se ha eliminado el campo `id_carrera` de la tabla `estudiante`. Ahora todas las relaciones entre estudiantes y carreras se gestionan exclusivamente a través de la tabla `estudiante_carrera`, que permite:

✅ Múltiples carreras por estudiante  
✅ Historial completo de cambios de carrera  
✅ Estados de inscripción (activa, suspendida, completada, etc.)  
✅ Gestión de carrera principal y secundarias  

---

## 🔄 Estructura Anterior vs Nueva

### ❌ ANTES (obsoleto)

```sql
CREATE TABLE estudiante (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    id_carrera INTEGER NOT NULL,  -- ❌ ELIMINADO
    FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera)
);
```

### ✅ AHORA (actual)

```sql
-- Tabla estudiante simplificada
CREATE TABLE estudiante (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE
);

-- Nueva tabla para gestionar carreras
CREATE TABLE estudiante_carrera (
    id_estudiante INTEGER NOT NULL,
    id_carrera INTEGER NOT NULL,
    estado TEXT NOT NULL,
    fecha_inscripcion TEXT NOT NULL,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    es_carrera_principal INTEGER DEFAULT 1,
    periodo_ingreso TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_estudiante, id_carrera),
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_carrera) REFERENCES carrera(id_carrera) ON DELETE RESTRICT
);
```

---

## 📝 Archivos Modificados

### DTOs
- ✅ `src/modelos/dtos/estudiante_dto.py` - Eliminado campo `id_carrera`

### DAOs
- ✅ `src/modelos/daos/estudiante_dao.py` - Actualizado CREATE TABLE, INSERT y UPDATE

### Documentación
- ✅ `docs/modelo_sql_sqlite_3_organizacion_academica.md` - Actualizada estructura
- ✅ `docs/modelo_sql_estudiante_carrera.md` - Documentación de migración
- ✅ `docs/README_estudiante_carrera.md` - Guía de uso actualizada
- ✅ `docs/CAMBIOS_IMPORTANTES.md` - Este documento

### Scripts
- ✅ `scripts/migrar_estudiante_carrera.py` - Migra datos a nueva tabla
- ✅ `scripts/eliminar_id_carrera_estudiante.py` - Elimina campo obsoleto

---

## 🚀 Migración para Proyectos Existentes

### Si tu base de datos tiene la estructura ANTIGUA:

#### 1️⃣ Migrar datos

```bash
python scripts/migrar_estudiante_carrera.py
```

Esto copiará los datos de `estudiante.id_carrera` a `estudiante_carrera`.

#### 2️⃣ Eliminar campo obsoleto

```bash
python scripts/eliminar_id_carrera_estudiante.py
```

⚠️ Crea un backup automático antes de proceder.

---

## 💻 Actualizar Código Existente

### ❌ Código que dejará de funcionar:

```python
# Ya no se puede asignar id_carrera en el DTO
estudiante = EstudianteDTO(
    nombre="Juan Pérez",
    correo="juan@email.com",
    id_carrera=5  # ❌ Este atributo ya no existe
)
estudiante_dao.insertar(estudiante)

# Ya no se puede leer id_carrera
print(estudiante.id_carrera)  # ❌ AttributeError
```

### ✅ Código correcto (nuevo):

```python
from modelos.services.estudiante_service import EstudianteService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.dtos.estudiante_dto import EstudianteDTO
from modelos.dtos.estudiante_carrera_dto import EstudianteCarreraDTO

# 1. Crear estudiante (sin carrera)
estudiante_service = EstudianteService()
estudiante = EstudianteDTO(
    nombre="Juan Pérez",
    correo="juan@email.com"
)
id_estudiante = estudiante_service.insertar(estudiante)

# 2. Asignar carrera usando EstudianteCarreraService
ec_service = EstudianteCarreraService()
dto_carrera = EstudianteCarreraDTO(
    id_estudiante=id_estudiante,
    id_carrera=5,
    estado='activa',
    fecha_inscripcion='2024-03-01',
    es_carrera_principal=1,
    periodo_ingreso='2024-1'
)
ec_service.inscribir_estudiante(dto_carrera)

# 3. Consultar carreras del estudiante
carreras = ec_service.obtener_carreras_estudiante(id_estudiante)
for carrera in carreras:
    print(f"Carrera: {carrera['nombre_carrera']} - Estado: {carrera['estado']}")

# 4. Obtener solo la carrera principal
carrera_principal = ec_service.obtener_carrera_principal(id_estudiante)
if carrera_principal:
    print(f"Carrera principal: {carrera_principal['nombre_carrera']}")
```

---

## 🔍 Buscar y Reemplazar en tu Código

### Patrones a buscar:

1. **En DTOs:**
   ```python
   # Buscar: id_carrera en EstudianteDTO
   EstudianteDTO(..., id_carrera=X, ...)
   
   # Reemplazar: Crear estudiante + asignar carrera separadamente
   ```

2. **En consultas:**
   ```sql
   -- Buscar: SELECT con id_carrera de estudiante
   SELECT e.nombre, e.id_carrera FROM estudiante e
   
   -- Reemplazar: JOIN con estudiante_carrera
   SELECT e.nombre, ec.id_carrera 
   FROM estudiante e
   JOIN estudiante_carrera ec ON e.id_estudiante = ec.id_estudiante
   WHERE ec.estado = 'activa'
   ```

3. **En lógica de negocio:**
   ```python
   # Buscar: Acceso directo a id_carrera
   estudiante.id_carrera
   
   # Reemplazar: Consultar via EstudianteCarreraService
   carrera = ec_service.obtener_carrera_principal(estudiante.id_estudiante)
   id_carrera = carrera['id_carrera'] if carrera else None
   ```

---

## 🎯 Ventajas del Nuevo Modelo

### ✅ Lo que ahora es posible:

1. **Doble titulación**
   ```python
   # Inscribir en primera carrera
   ec_service.inscribir_estudiante(EstudianteCarreraDTO(
       id_estudiante=1, id_carrera=3, estado='activa',
       fecha_inscripcion='2023-03-01', es_carrera_principal=1
   ))
   
   # Inscribir en segunda carrera
   ec_service.inscribir_estudiante(EstudianteCarreraDTO(
       id_estudiante=1, id_carrera=7, estado='activa',
       fecha_inscripcion='2024-03-01', es_carrera_principal=0
   ))
   ```

2. **Historial de cambios de carrera**
   ```python
   # Todas las carreras (historial completo)
   historial = ec_service.obtener_carreras_estudiante(id_estudiante=1)
   for registro in historial:
       print(f"{registro['nombre_carrera']} - {registro['estado']}")
   ```

3. **Estados de inscripción**
   ```python
   # Suspender una carrera
   ec_service.cambiar_estado(id_estudiante=1, id_carrera=3, nuevo_estado='suspendida')
   
   # Graduar
   ec_service.completar_carrera(id_estudiante=1, id_carrera=3, fecha_fin='2024-12-20')
   ```

---

## 📚 Documentación Adicional

- **Documentación técnica completa:** `docs/modelo_sql_estudiante_carrera.md`
- **Guía de uso:** `docs/README_estudiante_carrera.md`
- **Modelo SQL general:** `docs/modelo_sql_sqlite_3_organizacion_academica.md`

---

## ⚠️ Advertencias Importantes

1. **No se puede revertir fácilmente:** Una vez eliminado `id_carrera`, es difícil volver atrás
2. **Actualizar todo el código:** Buscar todas las referencias a `estudiante.id_carrera`
3. **Backup obligatorio:** Siempre hacer backup antes de ejecutar los scripts de migración
4. **Tests:** Ejecutar todos los tests después de la migración

---

## 🆘 Soporte

Si encuentras problemas durante la migración:

1. **Verificar logs:** `logs/` contiene información detallada
2. **Restaurar backup:** Los scripts crean backups automáticos
3. **Revisar documentación:** Consultar archivos en `docs/`

---

## 📅 Historial

- **2024-01-06:** Eliminación de `id_carrera` de tabla `estudiante`
- **2024-01-06:** Implementación de tabla `estudiante_carrera`
- **2024-01-06:** Scripts de migración creados

---

✅ **Actualiza tu código para usar EstudianteCarreraService en lugar de acceder directamente a id_carrera**

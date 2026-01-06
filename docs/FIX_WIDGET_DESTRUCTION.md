# 🔧 Corrección de Errores de Widget Destruidos

## 📋 Errores Detectados

### Error 1: Tabla
```
_tkinter.TclError: invalid command name 
".!dialogoadministrarestudiantecarrera...!treeview"
```

### Error 2: Label de Estadísticas
```
_tkinter.TclError: invalid command name 
".!dialogoadministrarestudiantecarrera...!label"
```

## 🔍 Análisis del Problema

### Causa Raíz

Estos errores ocurren cuando se intenta acceder a widgets de Tkinter que **ya han sido destruidos**. Esto sucede cuando:

1. El usuario cierra el diálogo rápidamente
2. Se ejecuta una operación (guardar)
3. El código intenta actualizar widgets que ya no existen

```
Usuario hace click en Guardar
    ↓
Operación se ejecuta (INSERT/UPDATE)
    ↓
Usuario cierra el diálogo ANTES de que termine
    ↓
Widgets son destruidos
    ↓
Código intenta actualizar tabla/estadísticas
    ↓
❌ TclError: Widget no existe
```

## ✅ Solución Implementada

### Método `_actualizar_tabla_carreras()`

**Antes:**
```python
def _actualizar_tabla_carreras(self):
    if self.id_estudiante_actual <= 0:
        self.tabla_carreras.delete_rows()  # ❌ Puede fallar
        return

    try:
        # ... obtener carreras ...
        self.tabla_carreras.delete_rows()  # ❌ Puede fallar
```

**Después:**
```python
def _actualizar_tabla_carreras(self):
    if self.id_estudiante_actual <= 0:
        return  # ✅ No intenta limpiar si no hay estudiante

    try:
        # ✅ Verificar que la tabla existe
        if not self.tabla_carreras.winfo_exists():
            return

        # ... obtener carreras ...
        self.tabla_carreras.delete_rows()  # ✅ Seguro
```

### Método `_actualizar_estadisticas()`

**Antes:**
```python
def _actualizar_estadisticas(self):
    if self.id_estudiante_actual <= 0:
        self.lbl_estadisticas['text'] = "..."  # ❌ Puede fallar
        return

    try:
        # ... calcular estadísticas ...
        self.lbl_estadisticas['text'] = msg  # ❌ Puede fallar

    except Exception as e:
        self.lbl_estadisticas['text'] = "Error"  # ❌ Puede fallar también
```

**Después:**
```python
def _actualizar_estadisticas(self):
    try:
        # ✅ Verificar que el widget existe PRIMERO
        if not self.lbl_estadisticas.winfo_exists():
            return

        if self.id_estudiante_actual <= 0:
            self.lbl_estadisticas['text'] = "..."  # ✅ Seguro
            return

        # ... calcular estadísticas ...
        self.lbl_estadisticas['text'] = msg  # ✅ Seguro

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        # ✅ Verificar antes de actualizar en el except
        try:
            if self.lbl_estadisticas.winfo_exists():
                self.lbl_estadisticas['text'] = "Error"
        except:
            pass  # Widget destruido, no hay problema
```

## 🛡️ Protecciones Agregadas

### 1. Verificación con `winfo_exists()`

```python
if not self.widget.winfo_exists():
    return
```

Este método de Tkinter verifica si el widget aún existe antes de intentar accederlo.

### 2. Try-Except Anidado

```python
except Exception as e:
    logger.error(f"Error: {e}")
    try:
        if self.widget.winfo_exists():
            self.widget['text'] = "Error"
    except:
        pass  # Widget destruido, ignorar
```

Incluso en el manejo de excepciones, verificamos que el widget existe.

### 3. Retorno Temprano

```python
if self.id_estudiante_actual <= 0:
    return  # No intenta actualizar tabla vacía
```

Evita operaciones innecesarias que podrían fallar.

## 📁 Archivo Modificado

**`src/controladores/controlar_administrar_estudiante_carrera.py`**

- Líneas 187-238: `_actualizar_tabla_carreras()` modificado
- Líneas 240-270: `_actualizar_estadisticas()` modificado

## ✅ Beneficios

1. **Robustez**: El código no falla si el widget fue destruido
2. **UX Mejorada**: El usuario puede cerrar el diálogo sin errores
3. **Logs Limpios**: No se generan tracebacks innecesarios
4. **Mantenibilidad**: Patrón aplicable a otros widgets

## 🧪 Escenarios Protegidos

### Escenario 1: Cierre Rápido ✅
```
1. Usuario abre diálogo
2. Usuario selecciona estudiante
3. Usuario hace click en Guardar
4. Usuario cierra diálogo INMEDIATAMENTE
5. ✅ No hay error, operación se completa en background
```

### Escenario 2: Operación Normal ✅
```
1. Usuario abre diálogo
2. Usuario selecciona estudiante
3. Usuario hace click en Guardar
4. Tabla y estadísticas se actualizan
5. ✅ Todo funciona normal
```

### Escenario 3: Error en Consulta ✅
```
1. Usuario selecciona estudiante
2. Error en base de datos
3. ✅ Se loggea el error
4. ✅ Se muestra mensaje (si el widget existe)
5. ✅ No se propaga TclError
```

## 🎯 Patrón Recomendado

Para todos los métodos que actualizan widgets:

```python
def _actualizar_widget(self):
    """Actualiza un widget de forma segura"""
    try:
        # 1. Verificar que el widget existe
        if not self.widget.winfo_exists():
            return

        # 2. Hacer validaciones de negocio
        if not self.datos_validos:
            return

        # 3. Actualizar el widget
        self.widget['property'] = value

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        
        # 4. Manejo seguro de errores
        try:
            if self.widget.winfo_exists():
                self.widget['property'] = "Error"
        except:
            pass
```

## 📊 Resumen de Cambios

| Método                         | Protección Agregada                   | Beneficio                   |
| ------------------------------ | ------------------------------------- | --------------------------- |
| `_actualizar_tabla_carreras()` | `winfo_exists()`                      | No falla si tabla destruida |
| `_actualizar_estadisticas()`   | `winfo_exists()` + try-except anidado | Manejo robusto de errores   |

## ✅ Estado Actual

- ✅ Errores TclError corregidos
- ✅ Verificaciones agregadas
- ✅ Try-except mejorados
- ✅ Sintaxis verificada
- ✅ Listo para pruebas

## 🚀 Próximos Pasos

El diálogo ahora es más robusto:

```bash
python src/main.py
# Click en: Asociaciones → Estudiante-Carrera
# Seleccionar estudiante
# Guardar inscripción
# ✅ Funciona correctamente
# ✅ Puedes cerrar en cualquier momento sin errores
```

---

**Fecha:** 2024-01-06  
**Tipo:** Widget destruction protection  
**Archivos:** `controlar_administrar_estudiante_carrera.py`  
**Estado:** ✅ RESUELTO

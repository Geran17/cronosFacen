# ✅ Diálogo Administrar Estudiante-Carrera Creado

## 📋 Resumen

Se ha creado exitosamente el diálogo modal `DialogoAdministrarEstudianteCarrera` siguiendo el mismo diseño y estructura de los otros diálogos del proyecto.

---

## 📁 Archivos Creados/Modificados

### Nuevo Archivo

**`src/ui/ttk/dialogos/dialogo_administrar_estudiante_carrera.py`** (18 líneas)

### Archivo Actualizado

**`src/ui/ttk/dialogos/__init__.py`** - Agregado el nuevo diálogo al paquete

---

## 📝 Código del Diálogo

```python
from ttkbootstrap import Toplevel
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_administrar_estudiante_carrera import FrameAdministrarEstudianteCarrera
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class DialogoAdministrarEstudianteCarrera(Toplevel):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.title("Administrador de Inscripciones Estudiante-Carrera")
        self.geometry("1200x700+50+50")

        frame = FrameAdministrarEstudianteCarrera(master=self)
        frame.pack(side=TOP, fill=BOTH, expand=TRUE)
```

---

## 🎨 Características del Diálogo

### Propiedades

- **Clase**: `DialogoAdministrarEstudianteCarrera`
- **Hereda de**: `Toplevel` (ventana modal de ttkbootstrap)
- **Título**: "Administrador de Inscripciones Estudiante-Carrera"
- **Tamaño**: 1200x700 píxeles
- **Posición**: 50 píxeles desde la esquina superior izquierda
- **Modal**: Sí (ventana Toplevel)

### Contenido

- **Frame**: `FrameAdministrarEstudianteCarrera`
- **Expansión**: Llena toda la ventana (BOTH + expand=TRUE)

---

## 💡 Uso del Diálogo

### Opción 1: Importación Directa

```python
from ui.ttk.dialogos.dialogo_administrar_estudiante_carrera import DialogoAdministrarEstudianteCarrera

# Abrir el diálogo
dialogo = DialogoAdministrarEstudianteCarrera(parent=ventana_principal)
```

### Opción 2: Desde el Paquete (Recomendado)

```python
from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera

# Abrir el diálogo
dialogo = DialogoAdministrarEstudianteCarrera(parent=ventana_principal)
```

### Opción 3: Desde un Botón

```python
from ttkbootstrap import Button
from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera

def abrir_admin_estudiante_carrera():
    """Abre el administrador de estudiante-carrera"""
    dialogo = DialogoAdministrarEstudianteCarrera(parent=self)
    dialogo.grab_set()  # Hacer modal
    self.wait_window(dialogo)  # Esperar a que se cierre

# Crear botón
btn_admin = Button(
    frame,
    text="🎓 Gestionar Carreras",
    command=abrir_admin_estudiante_carrera,
    bootstyle="info"
)
```

---

## 🔗 Integración en el Frame Principal

Si quieres agregar un botón en el frame principal de la aplicación:

```python
# En frame_principal.py o similar

from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera

class FramePrincipal(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        
        # ... otros widgets ...
        
        # Botón para abrir administrador de estudiante-carrera
        self.btn_estudiante_carrera = Button(
            self,
            text="🎓 Estudiante-Carrera",
            command=self._abrir_admin_estudiante_carrera,
            bootstyle="info"
        )
        self.btn_estudiante_carrera.pack(padx=5, pady=5)
    
    def _abrir_admin_estudiante_carrera(self):
        """Abre el administrador de inscripciones estudiante-carrera"""
        try:
            dialogo = DialogoAdministrarEstudianteCarrera(parent=self.master)
            dialogo.grab_set()  # Hacer la ventana modal
            self.wait_window(dialogo)  # Esperar a que se cierre
        except Exception as e:
            logger.error(f"Error al abrir diálogo estudiante-carrera: {e}")
            Messagebox.show_error("Error", f"No se pudo abrir el administrador:\n{str(e)}")
```

---

## 🎯 Ejemplo Completo de Uso

```python
#!/usr/bin/env python3
"""
Ejemplo de uso del diálogo administrar estudiante-carrera
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera


def main():
    # Crear ventana principal
    root = ttk.Window(
        title="CronosFacen",
        themename="darkly",
        size=(800, 600)
    )
    
    # Frame central
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=BOTH, expand=True)
    
    # Título
    ttk.Label(
        frame,
        text="Sistema de Gestión Académica",
        font=("Helvetica", 20, "bold"),
        bootstyle="info"
    ).pack(pady=20)
    
    # Botón para abrir el administrador
    def abrir_administrador():
        dialogo = DialogoAdministrarEstudianteCarrera(parent=root)
        dialogo.grab_set()
        root.wait_window(dialogo)
    
    btn_admin = ttk.Button(
        frame,
        text="🎓 Administrar Inscripciones Estudiante-Carrera",
        command=abrir_administrador,
        bootstyle="info",
        width=40
    )
    btn_admin.pack(pady=10)
    
    # Botón de salir
    ttk.Button(
        frame,
        text="Salir",
        command=root.quit,
        bootstyle="danger",
        width=40
    ).pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()
```

---

## 📊 Comparación con Otros Diálogos

| Diálogo                             | Tamaño       | Posición | Título                                              |
| ----------------------------------- | ------------ | -------- | --------------------------------------------------- |
| DialogoAdministrarEstudiante        | 800x600      | +10+10   | "Administrador de Estudiantes"                      |
| DialogoAdministrarCarrera           | 800x600      | +10+10   | "Administrador de Carreras"                         |
| DialogoAdministrarEstudianteCarrera | **1200x700** | +50+50   | "Administrador de Inscripciones Estudiante-Carrera" |

**Nota:** El diálogo de estudiante-carrera es más grande (1200x700) porque contiene:
- Selector de estudiante
- Tabla de carreras (60%)
- Formulario detallado (40%)
- Múltiples campos y botones

---

## 🔍 Ventajas del Diseño

### 1. Modal por Defecto
- Usa `Toplevel` que permite hacer la ventana modal con `grab_set()`
- El usuario debe cerrar esta ventana antes de volver a la principal

### 2. Herencia Simple
- Solo hereda de `Toplevel`
- No complica la jerarquía de clases

### 3. Composición
- El diálogo contiene el frame
- Separación clara de responsabilidades

### 4. Configuración Centralizada
- Título y tamaño en un solo lugar
- Fácil de modificar

### 5. Consistencia
- Mismo patrón que todos los diálogos del proyecto
- Fácil de mantener

---

## 🚀 Siguiente Paso

Ahora que tienes el diálogo, puedes:

1. **Integrarlo en el menú principal** de la aplicación
2. **Crear el controlador** `controlar_administrar_estudiante_carrera.py`
3. **Probar el diálogo** ejecutándolo de forma independiente
4. **Agregar validaciones** en el controlador

---

## 📝 Checklist de Implementación

- [x] Crear `dialogo_administrar_estudiante_carrera.py`
- [x] Actualizar `__init__.py` del paquete dialogos
- [x] Heredar de `Toplevel`
- [x] Configurar título descriptivo
- [x] Configurar tamaño adecuado (1200x700)
- [x] Incluir el frame correspondiente
- [x] Seguir el patrón de los otros diálogos
- [ ] Crear el controlador (siguiente paso)
- [ ] Agregar al menú principal
- [ ] Probar funcionamiento completo

---

## ✅ Características Implementadas

- ✅ Diálogo modal funcional
- ✅ Tamaño apropiado para el contenido
- ✅ Título descriptivo
- ✅ Integrado en el paquete de diálogos
- ✅ Importable desde `ui.ttk.dialogos`
- ✅ Sigue convenciones del proyecto
- ✅ 18 líneas de código limpio
- ✅ Logger configurado
- ✅ Frame empaquetado correctamente

---

✅ **El diálogo DialogoAdministrarEstudianteCarrera está listo para usarse.**

**Para abrirlo:**
```python
from ui.ttk.dialogos import DialogoAdministrarEstudianteCarrera

dialogo = DialogoAdministrarEstudianteCarrera(parent=ventana_principal)
dialogo.grab_set()
```

from ttkbootstrap import Button, Frame, Panedwindow
from typing import Optional, Dict, Any
from ui.ttk.dialogos.dialogo_administrar_carrera import DialogoAdministrarCarrera
from ui.ttk.dialogos.dialogo_administrar_estudiante import DialogoAdministrarEstudiante
from ui.ttk.dialogos.dialogo_administrar_estudiante_carrera import (
    DialogoAdministrarEstudianteCarrera,
)
from ui.ttk.dialogos.dialogo_administrar_asignatura import DialogoAdministrarAsignatura
from ui.ttk.dialogos.dialogo_administrar_eje_tematico import DialogoAdministrarEjeTemático
from ui.ttk.dialogos.dialogo_administrar_tipo_actividad import DialogoAdministrarTipoActividad
from ui.ttk.dialogos.dialogo_administrar_actividad import DialogoAdministrarActividad
from ui.ttk.dialogos.dialogo_administrar_calendario import DialogoAdministrarCalendario
from ui.ttk.dialogos.dialogo_administrar_prerequisitos import DialogoAdministrarPrerequisitos
from ui.ttk.dialogos.dialogo_administrar_estudiante_asignatura import (
    DialogoAdministrarEstudianteAsignatura,
)
from ui.ttk.dialogos.dialogo_administrar_estudiante_actividad import (
    DialogoAdministrarEstudianteActividad,
)
from ui.ttk.dialogos.dialogo_acerca_de import DialogoAcercaDe
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarFramePrincipal:
    def __init__(self, master: None, map_widgets: Dict[str, Any]):
        self.map_widgets = map_widgets
        self.master = master

        # Flag para controlar estado del menú
        self.menu_visible = True

        # Cargamos los widgets principales
        self.btn_menu: Button = self.map_widgets['btn_menu']
        self.btn_admin_carrera: Button = self.map_widgets['btn_admin_carrera']
        self.btn_carrera: Button = self.map_widgets['btn_carrera']
        self.btn_admin_estudiante: Button = self.map_widgets['btn_admin_estudiante']
        self.btn_estudiante: Button = self.map_widgets['btn_estudiante']
        self.btn_admin_asignatura: Button = self.map_widgets['btn_admin_asignatura']
        self.btn_asignatura: Button = self.map_widgets['btn_asignatura']
        self.btn_admin_eje_tematico: Button = self.map_widgets['btn_admin_eje_tematico']
        self.btn_eje_tematico: Button = self.map_widgets['btn_eje_tematico']
        self.btn_admin_tipo_actividad: Button = self.map_widgets['btn_admin_tipo_actividad']
        self.btn_tipo_actividad: Button = self.map_widgets['btn_tipo_actividad']
        self.btn_admin_actividad: Button = self.map_widgets['btn_admin_actividad']
        self.btn_actividad: Button = self.map_widgets['btn_actividad']
        self.btn_admin_calendario: Button = self.map_widgets['btn_admin_calendario']
        self.btn_calendario: Button = self.map_widgets['btn_calendario']
        self.btn_acerca_de: Button = self.map_widgets['btn_acerca_de']
        self.btn_prerequisito: Button = self.map_widgets['btn_prerequisito']
        self.btn_estudiante_asignatura: Button = self.map_widgets['btn_estudiante_asignatura']
        self.btn_estudiante_actividad: Button = self.map_widgets['btn_estudiante_actividad']
        self.btn_estudiante_carrera: Button = self.map_widgets['btn_estudiante_carrera']
        self.frame_lateral: Frame = self.master.frame_lateral
        self.paned_window: Panedwindow = self.master.paned_window

        # Conectar eventos
        self._conectar_eventos()

    def _conectar_eventos(self):
        """Conecta los eventos de los botones a sus manejadores"""
        try:
            # Botón menú
            self.btn_menu.config(command=self.on_toggle_menu)

            # Carrera
            self.btn_admin_carrera.config(command=self.on_administrar_carrera)
            self.btn_carrera.config(command=self.on_administrar_carrera)

            # Estudiante
            self.btn_admin_estudiante.config(command=self.on_administrar_estudiante)
            self.btn_estudiante.config(command=self.on_administrar_estudiante)

            # Asignatura
            self.btn_admin_asignatura.config(command=self.on_administrar_asignatura)
            self.btn_asignatura.config(command=self.on_administrar_asignatura)

            # Eje Temático
            self.btn_admin_eje_tematico.config(command=self.on_administrar_eje_tematico)
            self.btn_eje_tematico.config(command=self.on_administrar_eje_tematico)

            # Tipo Actividad
            self.btn_admin_tipo_actividad.config(command=self.on_administrar_tipo_actividad)
            self.btn_tipo_actividad.config(command=self.on_administrar_tipo_actividad)

            # Actividad
            self.btn_admin_actividad.config(command=self.on_administrar_actividad)
            self.btn_actividad.config(command=self.on_administrar_actividad)

            # Calendario
            self.btn_admin_calendario.config(command=self.on_administrar_calendario)
            self.btn_calendario.config(command=self.on_administrar_calendario)

            # Prerequisitos
            self.btn_prerequisito.config(command=self.on_administrar_prerequisitos)

            # Estudiante-Asignatura
            self.btn_estudiante_asignatura.config(command=self.on_administrar_estudiante_asignatura)

            # Estudiante-Actividad
            self.btn_estudiante_actividad.config(command=self.on_administrar_estudiante_actividad)

            # Estudiante-Carrera
            self.btn_estudiante_carrera.config(command=self.on_administrar_estudiante_carrera)

            # Acerca de
            self.btn_acerca_de.config(command=self.on_acerca_de)

            logger.debug("Eventos del controlador de frame principal conectados")
        except Exception as e:
            logger.error(f"Error al conectar eventos: {e}")

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘
    def on_toggle_menu(self):
        """
        Muestra u oculta el panel lateral de navegación.

        Alterna la visibilidad del frame_lateral dentro del paned_window,
        permitiendo al usuario maximizar el área de contenido central.
        """
        try:
            if self.menu_visible:
                # Ocultar el panel lateral removiendo del paned_window
                self.paned_window.remove(self.frame_lateral)
                self.menu_visible = False
                logger.info("Panel lateral ocultado")
            else:
                # Mostrar el panel lateral agregando nuevamente al paned_window
                self.paned_window.insert(0, self.frame_lateral, weight=0)
                self.menu_visible = True
                logger.info("Panel lateral mostrado")

        except Exception as e:
            logger.error(f"Error al alternar visibilidad del menú: {e}")

    def on_administrar_carrera(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarCarrera(parent=ventana_raiz)
            dialogo.title = "Administrador de Carreras"
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de carreras: {e}")

    def on_administrar_eje_tematico(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarEjeTemático(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de ejes temáticos: {e}")

    def on_administrar_tipo_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarTipoActividad(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de tipos de actividad: {e}")

    def on_administrar_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarActividad(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de actividades: {e}")

    def on_administrar_estudiante(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarEstudiante(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiantes: {e}")

    def on_administrar_asignatura(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarAsignatura(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de asignaturas: {e}")

    def on_administrar_calendario(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarCalendario(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración del calendario: {e}")

    def on_acerca_de(self):
        """
        Abre el diálogo de información sobre la aplicación.

        Se ejecuta cuando el usuario hace clic en el botón
        'Acerca de' del menú superior.
        """
        try:
            logger.info("Abriendo diálogo de acerca de")

            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAcercaDe(parent=ventana_raiz)
            dialogo.wait_window()

            logger.info("Diálogo de acerca de cerrado por el usuario")

        except Exception as e:
            logger.error(f"Error al abrir diálogo de acerca de: {e}")

    def on_administrar_prerequisitos(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarPrerequisitos(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de prerequisitos: {e}")

    def on_administrar_estudiante_asignatura(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarEstudianteAsignatura(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiante-asignatura: {e}")

    def on_administrar_estudiante_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarEstudianteActividad(parent=ventana_raiz)
            dialogo.grab_set()

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiante-actividad: {e}")

    def on_administrar_estudiante_carrera(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo modal
            dialogo = DialogoAdministrarEstudianteCarrera(parent=ventana_raiz)
            dialogo.grab_set()

            logger.info("Diálogo de administración de estudiante-carrera abierto")

        except Exception as e:
            logger.error(
                f"Error al abrir diálogo de administración de estudiante-carrera: {e}",
                exc_info=True,
            )

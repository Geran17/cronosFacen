from ttkbootstrap import Button, Frame, Panedwindow
from ttkbootstrap.constants import NORMAL, DISABLED
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
from ui.ttk.dialogos.dialogo_tema import DialogoTema
from ui.ttk.dialogos.dialogo_pin import DialogoPin
from configuracion.config_app import get_pin_hash
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
        self.btn_alertas: Button = self.map_widgets['btn_alertas']
        self.btn_dashboard: Button = self.map_widgets['btn_dashboard']
        self.btn_cuellos: Button = self.map_widgets['btn_cuellos']
        self.btn_acerca_de: Button = self.map_widgets['btn_acerca_de']
        self.btn_prerequisito: Button = self.map_widgets['btn_prerequisito']
        self.btn_estudiante_asignatura: Button = self.map_widgets['btn_estudiante_asignatura']
        self.btn_estudiante_actividad: Button = self.map_widgets['btn_estudiante_actividad']
        self.btn_estudiante_carrera: Button = self.map_widgets['btn_estudiante_carrera']
        self.btn_tema: Button = self.map_widgets['btn_tema']
        self.btn_pin_config: Button = self.map_widgets['btn_pin_config']
        self.btn_pin_clear: Button = self.map_widgets['btn_pin_clear']
        self.frame_lateral: Frame = self.master.frame_lateral
        self.paned_window: Panedwindow = self.master.paned_window
        self.notebook_central = self.map_widgets.get('notebook_central')
        self.frame_calendario = self.map_widgets.get('frame_calendario')
        self.frame_actividades = self.map_widgets.get('frame_actividades')
        self.frame_carreras = self.map_widgets.get('frame_carreras')
        self.frame_alertas = self.map_widgets.get('frame_alertas')
        self.frame_dashboard = self.map_widgets.get('frame_dashboard')
        self.frame_cuellos = self.map_widgets.get('frame_cuellos')

        # Conectar eventos
        self._conectar_eventos()

    def _conectar_eventos(self):
        """Conecta los eventos de los botones a sus manejadores"""
        try:
            # Botón menú
            self.btn_menu.config(command=self.on_toggle_menu)

            # Carrera
            self.btn_admin_carrera.config(command=self.on_administrar_carrera)
            self.btn_carrera.config(command=self.on_ir_carreras)

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
            self.btn_actividad.config(command=self.on_ir_actividades)

            # Calendario
            self.btn_admin_calendario.config(command=self.on_administrar_calendario)
            self.btn_calendario.config(command=self.on_ir_calendario)
            self.btn_alertas.config(command=self.on_ir_alertas)
            self.btn_dashboard.config(command=self.on_ir_dashboard)
            self.btn_cuellos.config(command=self.on_ir_cuellos)

            # Prerequisitos
            self.btn_prerequisito.config(command=self.on_administrar_prerequisitos)

            # Estudiante-Asignatura
            self.btn_estudiante_asignatura.config(command=self.on_administrar_estudiante_asignatura)

            # Estudiante-Actividad
            self.btn_estudiante_actividad.config(command=self.on_administrar_estudiante_actividad)

            # Estudiante-Carrera
            self.btn_estudiante_carrera.config(command=self.on_administrar_estudiante_carrera)

            # Tema
            self.btn_tema.config(command=self.on_tema)
            self.btn_pin_config.config(command=self.on_pin_config)
            self.btn_pin_clear.config(command=self.on_pin_clear)

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
            # desactiva auto menú si el usuario decide manualmente
            if hasattr(self.master, "auto_menu"):
                self.master.auto_menu = False

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

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarCarrera(parent=ventana_raiz)
            dialogo.title = "Administrador de Carreras"

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de carreras: {e}")

    def on_administrar_eje_tematico(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarEjeTemático(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de ejes temáticos: {e}")

    def on_administrar_tipo_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarTipoActividad(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de tipos de actividad: {e}")

    def on_administrar_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarActividad(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de actividades: {e}")

    def on_administrar_estudiante(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarEstudiante(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiantes: {e}")

    def on_administrar_asignatura(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarAsignatura(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de asignaturas: {e}")

    def _seleccionar_tab(self, frame_tab: Frame):
        try:
            if self.notebook_central and frame_tab:
                self.notebook_central.select(frame_tab)
        except Exception as e:
            logger.error(f"Error al seleccionar tab: {e}")

    def on_ir_carreras(self):
        self._seleccionar_tab(self.frame_carreras)

    def on_ir_actividades(self):
        self._seleccionar_tab(self.frame_actividades)

    def on_ir_calendario(self):
        self._seleccionar_tab(self.frame_calendario)

    def on_ir_alertas(self):
        self._seleccionar_tab(self.frame_alertas)

    def on_ir_dashboard(self):
        self._seleccionar_tab(self.frame_dashboard)

    def on_ir_cuellos(self):
        self._seleccionar_tab(self.frame_cuellos)

    def on_administrar_calendario(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarCalendario(parent=ventana_raiz)

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

    def on_tema(self):
        try:
            DialogoTema(parent=self.master.winfo_toplevel())
        except Exception as e:
            logger.error(f"Error al abrir selector de tema: {e}")

    def on_pin_config(self):
        try:
            DialogoPin(parent=self.master.winfo_toplevel(), mode="config")
            if hasattr(self.master, "lbl_pin_estado"):
                self.master.lbl_pin_estado.config(
                    text="🔒 PIN activo" if get_pin_hash() else "🔓 PIN no configurado"
                )
            if hasattr(self.master, "btn_pin_clear"):
                self.master.btn_pin_clear.config(
                    state=NORMAL if get_pin_hash() else DISABLED
                )
        except Exception as e:
            logger.error(f"Error al abrir configuración de PIN: {e}")

    def on_pin_clear(self):
        try:
            from configuracion.config_app import set_pin_hash
            from configuracion.config_app import get_pin_hash

            set_pin_hash(None)
            if hasattr(self.master, "lbl_pin_estado"):
                self.master.lbl_pin_estado.config(
                    text="🔒 PIN activo" if get_pin_hash() else "🔓 PIN no configurado"
                )
            if hasattr(self.master, "btn_pin_clear"):
                self.master.btn_pin_clear.config(state=DISABLED)
            logger.info("PIN eliminado")
        except Exception as e:
            logger.error(f"Error al eliminar PIN: {e}")

    def on_administrar_prerequisitos(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarPrerequisitos(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de prerequisitos: {e}")

    def on_administrar_estudiante_asignatura(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarEstudianteAsignatura(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiante-asignatura: {e}")

    def on_administrar_estudiante_actividad(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarEstudianteActividad(parent=ventana_raiz)

        except Exception as e:
            logger.error(f"Error al abrir diálogo de administración de estudiante-actividad: {e}")

    def on_administrar_estudiante_carrera(self):
        try:
            # Obtener la ventana raíz
            ventana_raiz = self.master.winfo_toplevel()

            # Crear y abrir el diálogo (no modal, permite interacción con frame_principal)
            dialogo = DialogoAdministrarEstudianteCarrera(parent=ventana_raiz)

            logger.info("Diálogo de administración de estudiante-carrera abierto")

        except Exception as e:
            logger.error(
                f"Error al abrir diálogo de administración de estudiante-carrera: {e}",
                exc_info=True,
            )

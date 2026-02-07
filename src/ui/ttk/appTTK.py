from ttkbootstrap import Window
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_principal import FramePrincipal
from ui.ttk.styles.estilos import apply_styles
from configuracion.config_app import get_tema, get_pin_hash
from ui.ttk.dialogos.dialogo_pin import DialogoPin
from utilidades.backup import crear_backup_al_cerrar
from utilidades.notificaciones_locales import revisar_y_notificar, obtener_intervalo_ms
from modelos.daos.conexion_sqlite import ConexionSQLite


class AppTTK(Window):
    def __init__(self, title="CronosFacen by Geran", **kwargs):
        tema = get_tema() or "darkly"
        super().__init__(title=title, **kwargs, themename=tema)

        apply_styles(self)

        # Tamaño adaptativo según resolución
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        if screen_w < 1100 or screen_h < 700:
            # Compactar ligeramente la UI en pantallas pequeñas
            try:
                self.tk.call("tk", "scaling", 0.9)
            except Exception:
                pass
        pad_w, pad_h = 40, 80
        target_w = max(800, min(1300, screen_w - pad_w))
        target_h = max(600, min(1000, screen_h - pad_h))
        min_w = min(900, target_w)
        min_h = min(600, target_h)

        self.minsize(min_w, min_h)
        x = max(0, (screen_w - target_w) // 2)
        y = max(0, (screen_h - target_h) // 2)
        self.geometry(f"{target_w}x{target_h}+{x}+{y}")

        self.frame_prinicipal = FramePrincipal(master=self)
        self.frame_prinicipal.pack(side=TOP, fill=BOTH, expand=TRUE)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._programar_notificaciones()

        # PIN opcional de acceso
        if get_pin_hash():
            dialog = DialogoPin(parent=self, mode="verify")
            self.wait_window(dialog)
            if not dialog.autenticado:
                self.destroy()

    def on_close(self):
        try:
            crear_backup_al_cerrar()
        finally:
            ConexionSQLite.cerrar_todas()
            self.destroy()

    def _programar_notificaciones(self):
        intervalo_ms = obtener_intervalo_ms()

        def _tick():
            try:
                revisar_y_notificar(parent=self)
            finally:
                self.after(intervalo_ms, _tick)

        self.after(3000, _tick)

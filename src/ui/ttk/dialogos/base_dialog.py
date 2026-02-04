from ttkbootstrap import Toplevel


class BaseDialog(Toplevel):
    def __init__(
        self,
        parent=None,
        title: str | None = None,
        geometry: str | None = None,
        minsize: tuple[int, int] | None = None,
        modal: bool = False,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        if title:
            self.title(title)
        if geometry:
            self.geometry(geometry)
        self._minsize = minsize
        if minsize:
            self.minsize(*minsize)

        if parent is not None:
            self.transient(parent)

        # cerrar seguro
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # centrar y ajustar tamaño según pantalla
        self.after(0, self._center_on_parent)

        if modal:
            self.grab_set()

        self.lift()
        self.focus_force()

    def _on_close(self):
        self.destroy()

    def _center_on_parent(self):
        try:
            self.update_idletasks()
            w = self.winfo_width()
            h = self.winfo_height()

            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            max_w = max(600, screen_w - 40)
            max_h = max(400, screen_h - 80)
            w = min(w, max_w)
            h = min(h, max_h)

            if self.master is not None:
                self.master.update_idletasks()
                x = self.master.winfo_rootx() + (self.master.winfo_width() - w) // 2
                y = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
            else:
                x = (screen_w - w) // 2
                y = (screen_h - h) // 2

            if self._minsize:
                min_w = min(self._minsize[0], max_w)
                min_h = min(self._minsize[1], max_h)
                self.minsize(min_w, min_h)

            self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

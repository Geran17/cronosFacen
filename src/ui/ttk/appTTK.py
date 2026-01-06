from ttkbootstrap import Window
from ttkbootstrap.constants import *
from ui.ttk.frames.frame_principal import FramePrincipal


class AppTTK(Window):
    def __init__(self, title="CronosFacen by Geran", **kwargs):
        super().__init__(title=title, **kwargs)

        self.geometry("1000x800+5+5")

        self.frame_prinicipal = FramePrincipal(master=self)
        self.frame_prinicipal.pack(side=TOP, fill=BOTH, expand=TRUE)

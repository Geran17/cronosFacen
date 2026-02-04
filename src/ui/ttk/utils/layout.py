from ttkbootstrap import Label, Separator
from ttkbootstrap.constants import TOP, X, TRUE
from ui.ttk.styles.estilos import PADDING_SM


def build_header(frame, titulo: str, subtitulo: str | None = None, bootstyle: str = "info"):
    label_info = Label(
        frame,
        text=titulo,
        bootstyle=bootstyle,
        style="Title.TLabel",
    )
    label_info.pack(side=TOP, fill=X, padx=PADDING_SM, pady=PADDING_SM, expand=TRUE)

    if subtitulo:
        lbl_subtitulo = Label(
            frame,
            text=subtitulo,
            bootstyle="secondary",
            style="Subtitle.TLabel",
        )
        lbl_subtitulo.pack(side=TOP, fill=X, padx=PADDING_SM, pady=(0, PADDING_SM))

    Separator(frame).pack(side=TOP, fill=X, expand=TRUE, padx=PADDING_SM, pady=PADDING_SM)

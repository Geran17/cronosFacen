from ttkbootstrap.constants import NORMAL


def bind_required(entry, normal_bootstyle: str = "info") -> None:
    """Marca visualmente un Entry requerido cuando está vacío."""

    def _validate(_event=None):
        value = entry.get().strip()
        bootstyle = normal_bootstyle if value else "danger"
        try:
            entry.config(bootstyle=bootstyle)
        except Exception:
            pass

    entry.bind("<KeyRelease>", _validate)
    entry.bind("<FocusOut>", _validate)
    # inicial
    _validate()

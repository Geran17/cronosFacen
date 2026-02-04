"""
Estilos globales para la UI (ttkbootstrap).
Centraliza tipografías, tamaños y estilos básicos.
"""

from ttkbootstrap import Style

# Tokens de estilo (se pueden ajustar en un solo lugar)
FONT_FAMILY = "Helvetica"
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 11)
FONT_SECTION = (FONT_FAMILY, 12, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)
FONT_FORM_LABEL = (FONT_FAMILY, 10, "bold")
FONT_HINT = (FONT_FAMILY, 9, "italic")
FONT_HERO = (FONT_FAMILY, 48)
FONT_DISPLAY = (FONT_FAMILY, 24, "bold")

# Espaciados consistentes
PADDING_XS = 2
PADDING_SM = 5
PADDING_MD = 10
PADDING_LG = 15
PADDING_XL = 20
PADDING_XXL = 40


def apply_styles(root=None) -> None:
    """
    Aplica estilos globales de ttkbootstrap.
    """
    style = Style()

    # Labels
    style.configure("Title.TLabel", font=FONT_TITLE)
    style.configure("Subtitle.TLabel", font=FONT_SUBTITLE)
    style.configure("Section.TLabel", font=FONT_SECTION)
    style.configure("Body.TLabel", font=FONT_BODY)
    style.configure("Small.TLabel", font=FONT_SMALL)
    style.configure("FormLabel.TLabel", font=FONT_FORM_LABEL)
    style.configure("Hint.TLabel", font=FONT_HINT)
    style.configure("Hero.TLabel", font=FONT_HERO)
    style.configure("Display.TLabel", font=FONT_DISPLAY)

    # Labelframes
    style.configure("Section.TLabelframe.Label", font=FONT_SECTION)
    style.configure("Stats.TLabelframe.Label", font=FONT_SECTION)

    # Buttons
    style.configure("Toolbar.TButton", font=FONT_BODY)
    style.configure("Primary.TButton", font=FONT_BODY)
    style.configure("Secondary.TButton", font=FONT_BODY)

    # Inputs
    style.configure("TEntry", font=FONT_BODY)
    style.configure("TCombobox", font=FONT_BODY)

    # Treeview
    style.configure("Treeview", font=FONT_BODY, rowheight=24)
    style.configure("Treeview.Heading", font=FONT_SECTION)

    # Tk widgets (Text/Listbox) - use global defaults when root is available
    if root is not None:
        # Tipografía base
        root.option_add("*Text*Font", FONT_BODY)
        root.option_add("*Listbox*Font", FONT_BODY)

        # Colores consistentes con el tema para widgets Tk
        colors = style.colors
        input_bg = getattr(colors, "inputbg", None) or getattr(colors, "bg", None)
        input_fg = getattr(colors, "inputfg", None) or getattr(colors, "fg", None)
        select_bg = getattr(colors, "selectbg", None) or getattr(colors, "primary", None)
        select_fg = getattr(colors, "selectfg", None) or getattr(colors, "fg", None)
        border = getattr(colors, "border", None) or input_bg

        if input_bg:
            root.option_add("*Text*background", input_bg)
            root.option_add("*Listbox*background", input_bg)
        if input_fg:
            root.option_add("*Text*foreground", input_fg)
            root.option_add("*Listbox*foreground", input_fg)
            root.option_add("*Text*insertbackground", input_fg)
        if select_bg:
            root.option_add("*Text*selectbackground", select_bg)
            root.option_add("*Listbox*selectbackground", select_bg)
        if select_fg:
            root.option_add("*Text*selectforeground", select_fg)
            root.option_add("*Listbox*selectforeground", select_fg)
        if border:
            root.option_add("*Text*highlightbackground", border)
            root.option_add("*Text*highlightcolor", border)
            root.option_add("*Listbox*highlightbackground", border)
            root.option_add("*Listbox*highlightcolor", border)

        # Bordes y padding consistentes con el tema
        root.option_add("*Text*borderwidth", 1)
        root.option_add("*Text*relief", "solid")
        root.option_add("*Text*highlightthickness", 1)
        root.option_add("*Listbox*borderwidth", 1)
        root.option_add("*Listbox*relief", "solid")
        root.option_add("*Listbox*highlightthickness", 1)

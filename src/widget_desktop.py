import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk

# Agregar el directorio src al path para importaciones relativas.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.services.actividad_service import ActividadService
from modelos.services.asignatura_service import AsignaturaService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.services.estudiante_service import EstudianteService
from configuracion.config_app import get_tema
from scripts.crear_indices import crear_todos_los_indices, hay_indices_faltantes
from scripts.crear_views import crear_todas_las_views, hay_views_faltantes
from scripts.logging_config import obtener_logger_modulo
from utilidades.config import inicializar_directorios, RUTA_CONFIG

try:
    from ttkbootstrap import Style as TbStyle
except Exception:  # pragma: no cover
    TbStyle = None

logger = obtener_logger_modulo(__name__)


class DesktopDashboardWidget(tk.Tk):
    REFRESH_MS = 60_000
    THEME_REFRESH_MS = 3_000
    WIDTH = 430
    HEIGHT = 520
    MIN_WIDTH = 360
    MIN_HEIGHT = 380

    def __init__(self):
        super().__init__()
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._student_id: Optional[int] = None
        self._student_name = "Sin estudiante"
        self._state_path = Path(RUTA_CONFIG) / "widget_window_state.json"
        self._save_after_id: Optional[str] = None
        self._ttk_style = None
        self._colors = self._default_colors()
        self._current_theme_name = ""
        self._last_subject_progress: List[Dict[str, Any]] = []

        self._init_theme()
        self._build_window()
        self._build_ui()
        self._bootstrap_data()
        self._load_data()
        self.after(self.THEME_REFRESH_MS, self._theme_refresh_loop)
        self.after(self.REFRESH_MS, self._refresh_loop)

    def _build_window(self) -> None:
        self.title("cronosFacen Widget")
        self.overrideredirect(False)
        self.attributes("-topmost", False)
        self.configure(bg=self._colors["window_bg"])
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        width, height, x, y = self._load_window_state()
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.bind("<Configure>", self._on_configure)

    def _build_ui(self) -> None:
        self.container = tk.Frame(
            self,
            bg=self._colors["window_bg"],
            bd=1,
            relief="solid",
            highlightthickness=0,
        )
        self.container.pack(fill="both", expand=True, padx=1, pady=1)

        self.header = tk.Frame(self.container, bg=self._colors["header_bg"], height=34)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.header_title = tk.Label(
            self.header,
            text="cronosFacen Dashboard",
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            font=("DejaVu Sans", 10, "bold"),
        )
        self.header_title.pack(side="left", padx=10)

        self.refresh_btn = tk.Button(
            self.header,
            text="↻",
            command=self._load_data,
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            relief="flat",
            activebackground=self._colors["button_hover_bg"],
            activeforeground=self._colors["header_fg"],
            cursor="hand2",
        )
        self.refresh_btn.pack(side="right", padx=(0, 6), pady=4)

        self.close_btn = tk.Button(
            self.header,
            text="✕",
            command=self._on_close,
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            relief="flat",
            activebackground=self._colors["close_hover_bg"],
            activeforeground=self._colors["header_fg"],
            cursor="hand2",
        )
        self.close_btn.pack(side="right", padx=(0, 2), pady=4)

        self.header.bind("<ButtonPress-1>", self._start_drag)
        self.header.bind("<B1-Motion>", self._drag)
        self.header.bind("<ButtonRelease-1>", self._end_drag)

        self.body = tk.Frame(self.container, bg=self._colors["window_bg"])
        self.body.pack(fill="both", expand=True, padx=12, pady=10)

        self.var_student = tk.StringVar(value="Estudiante: -")
        self.var_update = tk.StringVar(value="Actualizado: -")
        self.var_total = tk.StringVar(value="Total actividades: -")
        self.var_pending = tk.StringVar(value="Pendientes: -")
        self.var_expired = tk.StringVar(value="Vencidas: -")
        self.var_next = tk.StringVar(value="Próxima entrega: -")
        self.var_subject_summary = tk.StringVar(value="Asignaturas activas: - | Progreso prom.: -")

        self.info_labels: List[tk.Label] = []
        for var in (
            self.var_student,
            self.var_update,
            self.var_total,
            self.var_pending,
            self.var_expired,
            self.var_next,
            self.var_subject_summary,
        ):
            label = tk.Label(
                self.body,
                textvariable=var,
                anchor="w",
                justify="left",
                bg=self._colors["window_bg"],
                fg=self._colors["text_fg"],
                font=("DejaVu Sans", 9),
            )
            label.pack(fill="x", pady=1)
            self.info_labels.append(label)

        self.upcoming_title = tk.Label(
            self.body,
            text="Próximos 5:",
            anchor="w",
            bg=self._colors["window_bg"],
            fg=self._colors["accent_fg"],
            font=("DejaVu Sans", 9, "bold"),
        )
        self.upcoming_title.pack(fill="x", pady=(8, 2))

        self.list_upcoming = tk.Listbox(
            self.body,
            height=4,
            bg=self._colors["panel_bg"],
            fg=self._colors["list_fg"],
            highlightthickness=0,
            relief="flat",
            selectbackground=self._colors["list_sel_bg"],
            activestyle="none",
            font=("DejaVu Sans", 9),
        )
        self.list_upcoming.pack(fill="both", expand=True)

        self.subjects_title = tk.Label(
            self.body,
            text="Asignaturas (progreso entregas):",
            anchor="w",
            bg=self._colors["window_bg"],
            fg=self._colors["accent_fg"],
            font=("DejaVu Sans", 9, "bold"),
        )
        self.subjects_title.pack(fill="x", pady=(8, 2))

        self.subjects_frame = tk.Frame(
            self.body, bg=self._colors["panel_bg"], bd=0, highlightthickness=0
        )
        self.subjects_frame.pack(fill="x", pady=(0, 4))

    def _bootstrap_data(self) -> None:
        inicializar_directorios()
        if hay_indices_faltantes():
            crear_todos_los_indices()
        if hay_views_faltantes():
            crear_todas_las_views()

    def _refresh_loop(self) -> None:
        self._load_data()
        self.after(self.REFRESH_MS, self._refresh_loop)

    def _theme_refresh_loop(self) -> None:
        self._refresh_theme_if_changed()
        self.after(self.THEME_REFRESH_MS, self._theme_refresh_loop)

    def _load_data(self) -> None:
        try:
            self._refresh_theme_if_changed()
            self._resolve_student()
            activities = self._get_activities(self._student_id)
            subject_progress = self._get_subject_progress(self._student_id, activities)
            self._last_subject_progress = subject_progress
            total, pending, expired, next_text, upcoming = self._summarize(activities)

            self.var_student.set(f"Estudiante: {self._student_name}")
            self.var_update.set(f"Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.var_total.set(f"Total actividades: {total}")
            self.var_pending.set(f"Pendientes: {pending}")
            self.var_expired.set(f"Vencidas: {expired}")
            self.var_next.set(f"Próxima entrega: {next_text}")
            self.var_subject_summary.set(self._build_subject_summary(subject_progress))

            self.list_upcoming.delete(0, tk.END)
            if not upcoming:
                self.list_upcoming.insert(tk.END, "No hay entregas próximas.")
            else:
                for item in upcoming:
                    self.list_upcoming.insert(tk.END, item)

            self._render_subject_progress(subject_progress)
        except Exception as ex:
            logger.error(f"Error cargando widget: {ex}", exc_info=True)
            self.var_update.set("Actualizado: error")
            self.list_upcoming.delete(0, tk.END)
            self.list_upcoming.insert(tk.END, "Error al cargar datos.")
            self._render_subject_progress([])

    def _resolve_student(self) -> None:
        students = EstudianteService(ruta_db=None).obtener_id_nombre_correo()
        if not students:
            self._student_id = None
            self._student_name = "Sin estudiantes"
            return

        env_student_id = os.getenv("CRONOS_WIDGET_ESTUDIANTE_ID", "").strip()
        selected = None
        if env_student_id.isdigit():
            target_id = int(env_student_id)
            selected = next((s for s in students if s["id_estudiante"] == target_id), None)

        if selected is None:
            selected = students[0]

        self._student_id = selected["id_estudiante"]
        correo = selected.get("correo", "")
        self._student_name = f"{selected.get('nombre', 'N/A')} ({correo})"

    def _get_activities(self, student_id: Optional[int]) -> List[Dict[str, Any]]:
        if not student_id:
            return []
        return ActividadService(ruta_db=None).obtener_detalladas_filtradas(
            id_estudiante=student_id,
            id_carrera=None,
        )

    def _get_subject_progress(
        self, student_id: Optional[int], activities: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        if not student_id:
            return []

        try:
            carreras = EstudianteCarreraService(ruta_db=None).obtener_carreras_estudiante(
                student_id, "activa"
            )
            if not carreras:
                carreras = EstudianteCarreraService(ruta_db=None).obtener_carreras_estudiante(
                    student_id, None
                )

            id_carreras = {
                int(c.get("id_carrera"))
                for c in carreras
                if c.get("id_carrera") is not None
            }

            service = AsignaturaService(ruta_db=None)
            collected: List[Dict[str, Any]] = []
            seen = set()
            for id_carrera in sorted(id_carreras):
                rows = service.obtener_asignaturas_estudiante_completo(student_id, id_carrera)
                for row in rows:
                    if self._is_approved_subject(row):
                        continue
                    key = (row.get("id_carrera"), row.get("id_asignatura"))
                    if key in seen:
                        continue
                    seen.add(key)
                    collected.append(row)

            # En el widget, "en_progreso" no cuenta como actividad completada.
            # Recalculamos el porcentaje usando solo estado "entregada".
            delivered_by_subject: Dict[int, int] = {}
            for act in activities or []:
                if str(act.get("actividad_estado", "")).strip().lower() != "entregada":
                    continue
                subject_id = act.get("id_asignatura")
                if subject_id is None:
                    continue
                try:
                    sid = int(subject_id)
                except (TypeError, ValueError):
                    continue
                delivered_by_subject[sid] = delivered_by_subject.get(sid, 0) + 1

            for item in collected:
                subject_id = item.get("id_asignatura")
                try:
                    sid = int(subject_id) if subject_id is not None else None
                except (TypeError, ValueError):
                    sid = None
                total_activities = int(item.get("cantidad_actividades") or 0)
                delivered = delivered_by_subject.get(sid, 0) if sid is not None else 0
                pct = 0.0 if total_activities <= 0 else round((delivered * 100.0) / total_activities, 1)
                item["progreso_actividades"] = pct

            # Priorizar asignaturas incompletas con actividades y luego el resto.
            def _sort_key(item: Dict[str, Any]) -> Tuple[int, float, str]:
                pct = float(item.get("progreso_actividades", 0.0) or 0.0)
                has_activities = int((item.get("cantidad_actividades") or 0) > 0)
                return (0 if has_activities else 1, pct, str(item.get("nombre_asignatura", "")))

            collected.sort(key=_sort_key)
            return collected
        except Exception as ex:
            logger.error(f"Error cargando progreso por asignatura: {ex}", exc_info=True)
            return []

    def _is_approved_subject(self, subject_row: Dict[str, Any]) -> bool:
        estado = str(subject_row.get("estado", "")).strip().lower()
        if estado in ("aprobada", "completada"):
            return True
        nota = subject_row.get("nota_final")
        try:
            return nota is not None and float(nota) > 0
        except (TypeError, ValueError):
            return False

    def _summarize(self, activities: List[Dict[str, Any]]) -> Tuple[int, int, int, str, List[str]]:
        total = len(activities)
        pending = 0
        expired = 0
        upcoming_raw: List[Tuple[int, str, str]] = []

        for act in activities:
            state = act.get("actividad_estado")
            if state in ("pendiente", "en_progreso"):
                pending += 1
            if state == "vencida":
                expired += 1

            days_since_end = act.get("dias_desde_fin")
            if days_since_end is None:
                continue
            if days_since_end < 0:
                days_left = abs(days_since_end)
                title = str(act.get("titulo", "Sin título"))
                end_date = str(act.get("fecha_fin", ""))
                upcoming_raw.append((days_left, title, end_date))

        upcoming_raw.sort(key=lambda item: item[0])
        upcoming_text = [
            f"{days}d · {title} ({end_date})" for days, title, end_date in upcoming_raw[:5]
        ]

        if upcoming_raw:
            first = upcoming_raw[0]
            next_text = f"{first[0]}d · {first[1]}"
        else:
            next_text = "Sin próximas entregas"

        return total, pending, expired, next_text, upcoming_text

    def _build_subject_summary(self, subjects: List[Dict[str, Any]]) -> str:
        if not subjects:
            return "Asignaturas activas: 0 | Progreso prom.: 0%"

        filtered = [
            float(s.get("progreso_actividades", 0.0) or 0.0)
            for s in subjects
            if (s.get("cantidad_actividades") or 0) > 0
        ]
        if not filtered:
            return f"Asignaturas activas: {len(subjects)} | Progreso prom.: 0%"
        avg = sum(filtered) / len(filtered)
        return f"Asignaturas activas: {len(subjects)} | Progreso prom.: {avg:.0f}%"

    def _render_subject_progress(self, subjects: List[Dict[str, Any]]) -> None:
        for child in self.subjects_frame.winfo_children():
            child.destroy()

        if not subjects:
            tk.Label(
                self.subjects_frame,
                text="Sin datos de asignaturas.",
                anchor="w",
                bg=self._colors["panel_bg"],
                fg=self._colors["muted_fg"],
                font=("DejaVu Sans", 9),
            ).pack(fill="x", padx=8, pady=6)
            return

        for row in subjects[:4]:
            name = str(row.get("nombre_asignatura", "Asignatura"))
            pct = float(row.get("progreso_actividades", 0.0) or 0.0)
            pct = max(0.0, min(100.0, pct))

            row_frame = tk.Frame(self.subjects_frame, bg=self._colors["panel_bg"])
            row_frame.pack(fill="x", padx=8, pady=4)

            tk.Label(
                row_frame,
                text=name,
                anchor="w",
                bg=self._colors["panel_bg"],
                fg=self._colors["list_fg"],
                font=("DejaVu Sans", 9),
            ).pack(fill="x")

            bar_row = tk.Frame(row_frame, bg=self._colors["panel_bg"])
            bar_row.pack(fill="x", pady=(2, 0))

            progress = ttk.Progressbar(bar_row, maximum=100, value=pct, mode="determinate")
            progress.pack(side="left", fill="x", expand=True)

            tk.Label(
                bar_row,
                text=f"{pct:.0f}%",
                bg=self._colors["panel_bg"],
                fg=self._colors["muted_fg"],
                width=4,
                anchor="e",
                font=("DejaVu Sans", 8),
            ).pack(side="left", padx=(6, 0))

    def _default_colors(self) -> Dict[str, str]:
        return {
            "window_bg": "#0f172a",
            "panel_bg": "#111827",
            "header_bg": "#1e3a8a",
            "header_fg": "#ffffff",
            "text_fg": "#e2e8f0",
            "muted_fg": "#d1d5db",
            "accent_fg": "#93c5fd",
            "list_fg": "#e5e7eb",
            "list_sel_bg": "#1d4ed8",
            "button_hover_bg": "#1d4ed8",
            "close_hover_bg": "#dc2626",
        }

    def _init_theme(self) -> None:
        theme_name = (get_tema() or "").strip() or "darkly"
        self._current_theme_name = theme_name
        colors = self._default_colors()

        if TbStyle is None:
            self._colors = colors
            return

        try:
            self._ttk_style = TbStyle(theme=theme_name)
            c = self._ttk_style.colors
            dark_mode = self._is_dark_color(c.bg)
            colors.update(
                {
                    "window_bg": c.bg,
                    "panel_bg": c.selectbg if dark_mode else c.light,
                    "header_bg": c.primary,
                    "header_fg": c.selectfg if c.selectfg else "#ffffff",
                    "text_fg": c.fg,
                    "muted_fg": c.secondary,
                    "accent_fg": c.info,
                    "list_fg": c.fg,
                    "list_sel_bg": c.primary,
                    "button_hover_bg": c.info,
                    "close_hover_bg": c.danger,
                }
            )
            self._colors = colors
        except Exception as ex:
            logger.warning(f"No se pudo aplicar tema '{theme_name}' al widget: {ex}")
            self._colors = colors

    def _refresh_theme_if_changed(self) -> None:
        new_theme = (get_tema() or "").strip() or "darkly"
        if new_theme == self._current_theme_name:
            return
        self._init_theme()
        self._apply_theme_to_ui()
        self._render_subject_progress(self._last_subject_progress)

    def _apply_theme_to_ui(self) -> None:
        self.configure(bg=self._colors["window_bg"])
        self.container.configure(bg=self._colors["window_bg"])
        self.header.configure(bg=self._colors["header_bg"])
        self.header_title.configure(bg=self._colors["header_bg"], fg=self._colors["header_fg"])
        self.refresh_btn.configure(
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            activebackground=self._colors["button_hover_bg"],
            activeforeground=self._colors["header_fg"],
        )
        self.close_btn.configure(
            bg=self._colors["header_bg"],
            fg=self._colors["header_fg"],
            activebackground=self._colors["close_hover_bg"],
            activeforeground=self._colors["header_fg"],
        )
        self.body.configure(bg=self._colors["window_bg"])
        for label in self.info_labels:
            label.configure(bg=self._colors["window_bg"], fg=self._colors["text_fg"])
        self.upcoming_title.configure(bg=self._colors["window_bg"], fg=self._colors["accent_fg"])
        self.subjects_title.configure(bg=self._colors["window_bg"], fg=self._colors["accent_fg"])
        self.list_upcoming.configure(
            bg=self._colors["panel_bg"],
            fg=self._colors["list_fg"],
            selectbackground=self._colors["list_sel_bg"],
        )
        self.subjects_frame.configure(bg=self._colors["panel_bg"])

    def _is_dark_color(self, color_hex: str) -> bool:
        value = color_hex.lstrip("#")
        if len(value) != 6:
            return False
        r = int(value[0:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        return luminance < 128

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_offset_x = event.x
        self._drag_offset_y = event.y

    def _drag(self, event: tk.Event) -> None:
        x = self.winfo_pointerx() - self._drag_offset_x
        y = self.winfo_pointery() - self._drag_offset_y
        self.geometry(f"+{x}+{y}")

    def _end_drag(self, _event: tk.Event) -> None:
        self._save_window_state()

    def _on_close(self) -> None:
        self._save_window_state()
        self.destroy()

    def _default_window_state(self) -> Tuple[int, int, int, int]:
        x = max(self.winfo_screenwidth() - self.WIDTH - 20, 0)
        y = 50
        return self.WIDTH, self.HEIGHT, x, y

    def _load_window_state(self) -> Tuple[int, int, int, int]:
        default_w, default_h, default_x, default_y = self._default_window_state()
        try:
            if not self._state_path.exists():
                return default_w, default_h, default_x, default_y
            with open(self._state_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            width = int(data.get("width", default_w))
            height = int(data.get("height", default_h))
            x = int(data.get("x", default_x))
            y = int(data.get("y", default_y))
            width = max(width, self.MIN_WIDTH)
            height = max(height, self.MIN_HEIGHT)
            max_x = max(self.winfo_screenwidth() - width, 0)
            max_y = max(self.winfo_screenheight() - height, 0)
            x = min(max(x, 0), max_x)
            y = min(max(y, 0), max_y)
            return width, height, x, y
        except Exception as ex:
            logger.warning(f"No se pudo cargar estado de ventana: {ex}")
            return default_w, default_h, default_x, default_y

    def _save_window_state(self) -> None:
        try:
            self.update_idletasks()
            if self.state() != "normal":
                return
            width = int(self.winfo_width())
            height = int(self.winfo_height())
            x = int(self.winfo_x())
            y = int(self.winfo_y())
            self._state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._state_path, "w", encoding="utf-8") as file:
                json.dump({"x": x, "y": y, "width": width, "height": height}, file)
        except Exception as ex:
            logger.warning(f"No se pudo guardar estado de ventana: {ex}")

    def _on_configure(self, _event: tk.Event) -> None:
        if self._save_after_id is not None:
            self.after_cancel(self._save_after_id)
        self._save_after_id = self.after(400, self._save_window_state)


def main() -> None:
    app = DesktopDashboardWidget()
    app.mainloop()


if __name__ == "__main__":
    main()

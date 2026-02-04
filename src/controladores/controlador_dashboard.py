from __future__ import annotations

from datetime import date, datetime
from typing import Dict, Any, List

from ttkbootstrap import Label, Frame, Progressbar
from ttkbootstrap.constants import *

from modelos.services.estudiante_service import EstudianteService
from modelos.services.estudiante_carrera_service import EstudianteCarreraService
from modelos.services.actividad_service import ActividadService
from modelos.services.asignatura_service import AsignaturaService
from modelos.services.consulta_service import EventosUnificadosService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControladorDashboard:
    def __init__(self, map_widgets: Dict[str, Any], map_vars: Dict[str, Any]):
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        self.dict_estudiantes: Dict[str, int] = {}
        self.dict_carreras: Dict[str, int] = {}

        self._cargar_widgets()
        self._cargar_estudiantes()
        self._vincular_eventos()

    def _cargar_widgets(self):
        self.cbx_estudiante = self.map_widgets.get("cbx_estudiante")
        self.cbx_carrera = self.map_widgets.get("cbx_carrera")
        self.btn_refrescar = self.map_widgets.get("btn_refrescar")
        self.tree_eventos = self.map_widgets.get("tree_eventos")
        self.frame_progreso = self.map_widgets.get("frame_progreso")

        self.lbl_prog = self.map_widgets.get("lbl_prog")
        self.lbl_prog_hint = self.map_widgets.get("lbl_prog_hint")
        self.lbl_asig = self.map_widgets.get("lbl_asig")
        self.lbl_asig_hint = self.map_widgets.get("lbl_asig_hint")
        self.lbl_act = self.map_widgets.get("lbl_act")
        self.lbl_act_hint = self.map_widgets.get("lbl_act_hint")
        self.lbl_prox = self.map_widgets.get("lbl_prox")
        self.lbl_prox_hint = self.map_widgets.get("lbl_prox_hint")

    def _vincular_eventos(self):
        if self.cbx_estudiante:
            self.cbx_estudiante.bind("<<ComboboxSelected>>", self._on_estudiante)
        if self.cbx_carrera:
            self.cbx_carrera.bind("<<ComboboxSelected>>", self._refrescar)
        if self.btn_refrescar:
            self.btn_refrescar.config(command=self._refrescar)

    def _cargar_estudiantes(self):
        try:
            servicio = EstudianteService(ruta_db=None)
            lista = servicio.obtener_id_nombre_correo()
            labels = []
            self.dict_estudiantes.clear()
            for item in lista:
                label = f"{item['nombre']} - {item.get('correo', '')}".strip()
                labels.append(label)
                self.dict_estudiantes[label] = item["id_estudiante"]
            if self.cbx_estudiante:
                self.cbx_estudiante["values"] = labels
                if labels:
                    self.cbx_estudiante.current(0)
                    self._on_estudiante()
        except Exception as e:
            logger.error(f"Error al cargar estudiantes: {e}", exc_info=True)

    def _on_estudiante(self, _event=None):
        try:
            label = self.map_vars["var_estudiante"].get()
            id_est = self.dict_estudiantes.get(label)
            if not id_est:
                return
            servicio = EstudianteCarreraService(ruta_db=None)
            carreras = servicio.obtener_carreras_estudiante(id_est, None)
            labels = ["Todas"]
            self.dict_carreras.clear()
            for c in carreras:
                nombre = c.get("nombre_carrera") or c.get("nombre")
                if not nombre:
                    continue
                labels.append(nombre)
                self.dict_carreras[nombre] = c.get("id_carrera")
            if self.cbx_carrera:
                self.cbx_carrera["values"] = labels
                self.cbx_carrera.current(0)
            self._refrescar()
        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}", exc_info=True)

    def _refrescar(self, _event=None):
        id_est = self._get_estudiante_id()
        if not id_est:
            return
        id_carrera = self._get_carrera_id()
        nombre_carrera = self._get_carrera_nombre()

        actividades = self._obtener_actividades(id_est, id_carrera)
        self._actualizar_resumen_actividades(actividades)
        self._actualizar_proxima_entrega(actividades)
        self._actualizar_eventos(nombre_carrera)
        self._actualizar_progreso_semestres(id_est, id_carrera)

    def _get_estudiante_id(self) -> int:
        label = self.map_vars["var_estudiante"].get()
        return self.dict_estudiantes.get(label, 0)

    def _get_carrera_id(self) -> int:
        label = self.map_vars["var_carrera"].get()
        if label == "Todas":
            return 0
        return self.dict_carreras.get(label, 0)

    def _get_carrera_nombre(self) -> str:
        label = self.map_vars["var_carrera"].get()
        return "" if label == "Todas" else label

    def _obtener_actividades(self, id_estudiante: int, id_carrera: int) -> List[Dict[str, Any]]:
        try:
            servicio = ActividadService(ruta_db=None)
            return servicio.obtener_detalladas_filtradas(
                id_estudiante=id_estudiante, id_carrera=id_carrera or None
            )
        except Exception as e:
            logger.error(f"Error al obtener actividades: {e}", exc_info=True)
            return []

    def _actualizar_resumen_actividades(self, actividades: List[Dict[str, Any]]):
        total = len(actividades)
        pendientes = 0
        vencidas = 0
        for a in actividades:
            estado = a.get("actividad_estado")
            if estado in ("pendiente", "en_progreso"):
                pendientes += 1
            if estado == "vencida":
                vencidas += 1

        self.lbl_act.config(text=str(total))
        self.lbl_act_hint.config(text=f"Pendientes: {pendientes} • Vencidas: {vencidas}")

    def _actualizar_proxima_entrega(self, actividades: List[Dict[str, Any]]):
        proxima = None
        dias = None
        for a in actividades:
            d = a.get("dias_desde_fin")
            if d is None:
                continue
            if d < 0:
                restantes = abs(d)
                if dias is None or restantes < dias:
                    dias = restantes
                    proxima = a

        if proxima:
            self.lbl_prox.config(text=f"{dias}d")
            self.lbl_prox_hint.config(text=proxima.get("titulo", "—"))
        else:
            self.lbl_prox.config(text="—")
            self.lbl_prox_hint.config(text="Sin próximas entregas")

    def _actualizar_eventos(self, carrera_nombre: str):
        if not self.tree_eventos:
            return
        for item in self.tree_eventos.get_children():
            self.tree_eventos.delete(item)
        try:
            servicio = EventosUnificadosService(ruta_db=None)
            eventos = servicio.obtener_actividades()
            hoy = date.today()
            items = []
            for e in eventos:
                if carrera_nombre and e.carrera != carrera_nombre:
                    continue
                fecha_fin = datetime.strptime(e.fecha_fin, "%Y-%m-%d").date()
                dias = (fecha_fin - hoy).days
                if 0 <= dias <= 7:
                    items.append((fecha_fin.isoformat(), e.titulo, dias))
            for fecha, titulo, dias in sorted(items, key=lambda x: x[2]):
                self.tree_eventos.insert("", "end", values=(fecha, titulo, dias))
        except Exception as e:
            logger.error(f"Error al actualizar eventos: {e}", exc_info=True)

    def _actualizar_progreso_semestres(self, id_estudiante: int, id_carrera: int):
        if not self.frame_progreso:
            return
        for w in self.frame_progreso.winfo_children():
            w.destroy()
        if not id_carrera:
            Label(
                self.frame_progreso,
                text="Seleccione una carrera para ver el progreso por semestre",
                style="Small.TLabel",
            ).pack(anchor=W)
            self.lbl_prog.config(text="—")
            self.lbl_prog_hint.config(text="Sin carrera seleccionada")
            self.lbl_asig.config(text="—")
            self.lbl_asig_hint.config(text="")
            return

        try:
            servicio = AsignaturaService(ruta_db=None)
            plan = servicio.obtener_plan_carrera(id_carrera)
            cursadas = servicio.obtener_asignaturas_estudiante_completo(
                id_estudiante, id_carrera
            )
            cursadas_map = {a["id_asignatura"]: a for a in cursadas}

            semestres: Dict[int, Dict[str, int]] = {}
            for asig in plan:
                semestre = int(asig.get("semestre", 0))
                sem = semestres.setdefault(semestre, {"total": 0, "ok": 0})
                sem["total"] += 1
                id_asig = asig.get("id_asignatura")
                estado = cursadas_map.get(id_asig, {}).get("estado")
                if estado in ("completada", "aprobada"):
                    sem["ok"] += 1

            for semestre in sorted(semestres.keys()):
                data = semestres[semestre]
                total = data["total"]
                ok = data["ok"]
                pct = (ok / total * 100) if total else 0

                row = Frame(self.frame_progreso)
                row.pack(fill=X, pady=2)
                Label(row, text=f"Sem {semestre}", width=7).pack(side=LEFT)
                pb = Progressbar(row, value=pct, maximum=100)
                pb.pack(side=LEFT, fill=X, expand=TRUE, padx=(5, 5))
                Label(row, text=f"{pct:.0f}%", width=5).pack(side=LEFT)

            ok_total = sum(v["ok"] for v in semestres.values())
            total_asig = sum(v["total"] for v in semestres.values())
            pct_total = (ok_total / total_asig * 100) if total_asig else 0
            self.lbl_prog.config(text=f"{pct_total:.0f}%")
            self.lbl_prog_hint.config(text=f"Completadas: {ok_total}/{total_asig}")
            self.lbl_asig.config(text=str(total_asig))
            self.lbl_asig_hint.config(text=f"Cursadas: {ok_total}")
        except Exception as e:
            logger.error(f"Error al actualizar progreso: {e}", exc_info=True)

from __future__ import annotations

from datetime import date
from typing import Dict, Any, List

from ttkbootstrap import Button, Label
from ttkbootstrap.constants import DISABLED, NORMAL, READONLY

from modelos.services.consulta_service import EventosUnificadosService
from modelos.dtos.consulta_dto import EventosUnificadosDTO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControladorAlertasActividades:
    def __init__(self, map_widgets: Dict[str, Any], map_vars: Dict[str, Any]):
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        self.eventos: List[EventosUnificadosDTO] = []

        self._cargar_widgets()
        self._cargar_vars()
        self._cargar_filtros()
        self._cargar_alertas()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Carga inicial
    # └────────────────────────────────────────────────────────────┘
    def _cargar_widgets(self):
        self.cbx_carrera = self.map_widgets.get('cbx_carrera')
        self.cbx_asignatura = self.map_widgets.get('cbx_asignatura')
        self.cbx_tipo_actividad = self.map_widgets.get('cbx_tipo_actividad')
        self.cbx_rango = self.map_widgets.get('cbx_rango')

        self.btn_aplicar = self.map_widgets.get('btn_aplicar')
        self.btn_refrescar = self.map_widgets.get('btn_refrescar')
        self.btn_limpiar = self.map_widgets.get('btn_limpiar')

        self.tree_alertas = self.map_widgets.get('tree_alertas')
        self.lbl_stats: Label | None = self.map_widgets.get('lbl_stats')

        if self.btn_aplicar:
            self.btn_aplicar.config(command=self._aplicar_filtros)
        if self.btn_refrescar:
            self.btn_refrescar.config(command=self._refrescar)
        if self.btn_limpiar:
            self.btn_limpiar.config(command=self._resetear_filtros)

    def _cargar_vars(self):
        self.var_carrera = self.map_vars.get('var_carrera')
        self.var_asignatura = self.map_vars.get('var_asignatura')
        self.var_tipo_actividad = self.map_vars.get('var_tipo_actividad')
        self.var_rango = self.map_vars.get('var_rango')

    # ┌────────────────────────────────────────────────────────────┐
    # │ Utilidades
    # └────────────────────────────────────────────────────────────┘
    def _set_loading(self, loading: bool, message: str = "Cargando..."):
        btn_state = DISABLED if loading else NORMAL
        cbx_state = DISABLED if loading else READONLY

        for btn in (self.btn_aplicar, self.btn_refrescar, self.btn_limpiar):
            if btn:
                btn.config(state=btn_state)

        for cbx in (self.cbx_carrera, self.cbx_asignatura, self.cbx_tipo_actividad, self.cbx_rango):
            if cbx:
                cbx.config(state=cbx_state)

        if self.lbl_stats and loading:
            self.lbl_stats.config(text=message, bootstyle="info")

    def _parse_fecha(self, fecha_iso: str) -> date | None:
        try:
            return date.fromisoformat(fecha_iso)
        except Exception:
            return None

    def _dias_restantes(self, evento: EventosUnificadosDTO) -> int:
        fecha_fin = self._parse_fecha(evento.fecha_fin)
        if not fecha_fin:
            return 0
        return (fecha_fin - date.today()).days

    def _estado_alerta(self, dias: int) -> str:
        if dias < 0:
            return "Vencida"
        if dias == 0:
            return "Hoy"
        if dias <= 3:
            return "Próxima (0-3d)"
        if dias <= 7:
            return "Próxima (4-7d)"
        if dias <= 14:
            return "Próxima (8-14d)"
        return "Lejana (15+d)"

    def _matches_rango(self, dias: int, rango: str) -> bool:
        if rango == "Todas":
            return True
        if rango == "Vencidas":
            return dias < 0
        if rango == "Hoy":
            return dias == 0
        if rango == "0-3 días":
            return 0 < dias <= 3
        if rango == "4-7 días":
            return 3 < dias <= 7
        if rango == "8-14 días":
            return 7 < dias <= 14
        if rango == "15+ días":
            return dias > 14
        return True

    # ┌────────────────────────────────────────────────────────────┐
    # │ Filtros y carga de datos
    # └────────────────────────────────────────────────────────────┘
    def _cargar_filtros(self):
        self._set_loading(True, "Cargando filtros...")
        try:
            servicio = EventosUnificadosService(ruta_db=None)
            self.eventos = servicio.obtener_actividades()

            carreras = sorted({e.carrera for e in self.eventos if e.carrera})
            asignaturas = sorted({e.asignatura for e in self.eventos if e.asignatura})
            tipos = sorted({e.tipo_actividad for e in self.eventos if e.tipo_actividad})

            if self.cbx_carrera:
                self.cbx_carrera['values'] = ["Todos"] + carreras
                self.cbx_carrera.current(0)
            if self.cbx_asignatura:
                self.cbx_asignatura['values'] = ["Todos"] + asignaturas
                self.cbx_asignatura.current(0)
            if self.cbx_tipo_actividad:
                self.cbx_tipo_actividad['values'] = ["Todos"] + tipos
                self.cbx_tipo_actividad.current(0)
            if self.cbx_rango:
                self.cbx_rango['values'] = [
                    "Todas",
                    "Vencidas",
                    "Hoy",
                    "0-3 días",
                    "4-7 días",
                    "8-14 días",
                    "15+ días",
                ]
                self.cbx_rango.current(0)
        except Exception as e:
            logger.error(f"Error al cargar filtros de alertas: {e}", exc_info=True)
        finally:
            self._set_loading(False)

    def _aplicar_filtros(self):
        self._cargar_alertas()

    def _resetear_filtros(self):
        try:
            for cbx in (self.cbx_carrera, self.cbx_asignatura, self.cbx_tipo_actividad, self.cbx_rango):
                if cbx and cbx['values']:
                    cbx.current(0)
        finally:
            self._cargar_alertas()

    def _refrescar(self):
        self._cargar_filtros()
        self._cargar_alertas()

    def _cargar_alertas(self):
        if not self.tree_alertas:
            return

        self._set_loading(True, "Cargando alertas...")

        try:
            for item in self.tree_alertas.get_children():
                self.tree_alertas.delete(item)

            if not self.eventos:
                self._set_stats(0, 0, 0, 0, 0)
                return

            carrera = self.var_carrera.get() if self.var_carrera else "Todos"
            asignatura = self.var_asignatura.get() if self.var_asignatura else "Todos"
            tipo = self.var_tipo_actividad.get() if self.var_tipo_actividad else "Todos"
            rango = self.var_rango.get() if self.var_rango else "Todas"

            filtrados: List[EventosUnificadosDTO] = []
            for evento in self.eventos:
                if carrera != "Todos" and evento.carrera != carrera:
                    continue
                if asignatura != "Todos" and evento.asignatura != asignatura:
                    continue
                if tipo != "Todos" and evento.tipo_actividad != tipo:
                    continue

                dias = self._dias_restantes(evento)
                if not self._matches_rango(dias, rango):
                    continue
                filtrados.append(evento)

            for evento in sorted(filtrados, key=self._dias_restantes):
                dias = self._dias_restantes(evento)
                estado = self._estado_alerta(dias)
                self.tree_alertas.insert(
                    "",
                    "end",
                    values=(
                        evento.titulo,
                        evento.carrera or "Sin carrera",
                        evento.asignatura or "Sin asignatura",
                        evento.tipo_actividad,
                        evento.fecha_fin,
                        dias,
                        estado,
                    ),
                )

            self._actualizar_stats(filtrados)
        except Exception as e:
            logger.error(f"Error al cargar alertas: {e}", exc_info=True)
        finally:
            self._set_loading(False)

    def _actualizar_stats(self, eventos: List[EventosUnificadosDTO]):
        vencidas = 0
        hoy = 0
        prox_3 = 0
        prox_7 = 0
        lejanas = 0
        for evento in eventos:
            dias = self._dias_restantes(evento)
            if dias < 0:
                vencidas += 1
            elif dias == 0:
                hoy += 1
            elif dias <= 3:
                prox_3 += 1
            elif dias <= 7:
                prox_7 += 1
            else:
                lejanas += 1

        self._set_stats(len(eventos), vencidas, hoy, prox_3 + prox_7, lejanas)

    def _set_stats(self, total: int, vencidas: int, hoy: int, proximas: int, lejanas: int):
        if not self.lbl_stats:
            return
        self.lbl_stats.config(
            text=(
                f"Total: {total}  |  "
                f"Vencidas: {vencidas}  |  "
                f"Hoy: {hoy}  |  "
                f"Próximas: {proximas}  |  "
                f"Lejanas: {lejanas}"
            ),
            bootstyle="secondary",
        )

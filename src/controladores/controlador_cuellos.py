from typing import Dict, Any, List, Set
from ttkbootstrap import Combobox
from tkinter.messagebox import showwarning

from modelos.services.carrera_service import CarreraService
from modelos.services.asignatura_service import AsignaturaService
from modelos.services.prerequisito_service import PrerrequisitoService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControladorCuellos:
    """Controlador para el panel de cuellos de botella estructurales."""

    def __init__(self, map_vars: Dict[str, Any], map_widgets: Dict[str, Any]):
        self.map_vars = map_vars
        self.map_widgets = map_widgets

        self.dict_carreras: Dict[int, str] = {}
        self.dict_carreras_inv: Dict[str, int] = {}
        self.id_carrera_actual: int = 0
        self.detalle_por_id: Dict[int, Dict[str, Any]] = {}

        self._cargar_widgets()
        self._cargar_carreras()
        self._vincular_eventos()

    def _cargar_widgets(self) -> None:
        try:
            self.cbx_carrera: Combobox = self.map_widgets.get('cbx_carrera')
        except Exception as e:
            logger.error(f"Error al cargar widgets: {e}")
            showwarning("Error", f"Error al cargar widgets: {e}")

    def _cargar_carreras(self) -> None:
        try:
            service = CarreraService(ruta_db=None)
            carreras = service.obtener_id_nombre_plan()

            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()
            labels: List[str] = []

            for dato in carreras:
                id_carrera = dato['id_carrera']
                nombre = dato['nombre']
                plan = dato.get('plan') or ""
                label = f"{nombre} ({plan})" if plan else nombre
                labels.append(label)
                self.dict_carreras[id_carrera] = label
                self.dict_carreras_inv[label] = id_carrera

            self.cbx_carrera.config(values=labels)
            if labels:
                self.cbx_carrera.current(0)
                self._on_change_carrera()
        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}", exc_info=True)
            self.cbx_carrera.config(values=[])

    def _vincular_eventos(self) -> None:
        try:
            self.cbx_carrera.bind('<<ComboboxSelected>>', self._on_change_carrera)
            cbx_top = self.map_widgets.get('cbx_top')
            if cbx_top:
                cbx_top.bind('<<ComboboxSelected>>', self._on_change_carrera)
            btn_refrescar = self.map_widgets.get('btn_refrescar')
            if btn_refrescar:
                btn_refrescar.config(command=self._on_change_carrera)
            tabla = self.map_widgets.get('tabla_cuellos')
            if tabla:
                tabla.view.bind('<<TreeviewSelect>>', self._on_select_row)
        except Exception as e:
            logger.error(f"Error al vincular eventos: {e}", exc_info=True)

    def _on_change_carrera(self, event=None) -> None:
        try:
            nombre = self.map_vars.get('var_carrera').get()
            self.id_carrera_actual = self.dict_carreras_inv.get(nombre, 0)
            if not self.id_carrera_actual:
                return
            resultados = self._calcular_cuellos(self.id_carrera_actual)
            frame = self.map_widgets.get('frame_cuellos')
            if frame:
                top_n = self._leer_top()
                frame.mostrar_resultados(resultados[:top_n] if top_n else resultados)
                frame.limpiar_detalle()
        except Exception as e:
            logger.error(f"Error al cambiar carrera: {e}", exc_info=True)

    def _leer_top(self) -> int:
        valor = self.map_vars.get('var_top').get()
        if not valor or str(valor).strip().lower() == "todos":
            return 0
        try:
            return max(0, int(valor))
        except ValueError:
            return 0

    def _on_select_row(self, _event=None) -> None:
        try:
            tabla = self.map_widgets.get('tabla_cuellos')
            frame = self.map_widgets.get('frame_cuellos')
            if not tabla or not frame:
                return
            seleccion = tabla.view.selection()
            if not seleccion:
                frame.limpiar_detalle()
                return
            item = tabla.view.item(seleccion[0])
            valores = item.get('values') or []
            if not valores:
                frame.limpiar_detalle()
                return
            id_asignatura = int(valores[0])
            detalle = self.detalle_por_id.get(id_asignatura, {})
            frame.mostrar_detalle(
                detalle.get('nombre', ''),
                detalle.get('directos', []),
                detalle.get('totales', []),
            )
        except Exception as e:
            logger.error(f"Error al seleccionar fila: {e}", exc_info=True)

    def _calcular_cuellos(self, id_carrera: int) -> List[Dict[str, Any]]:
        """Calcula el impacto estructural (bloqueo directo y total)."""
        asignatura_service = AsignaturaService(ruta_db=None)
        prereq_service = PrerrequisitoService(ruta_db=None)

        asignaturas = asignatura_service.obtener_basico_por_carrera(id_carrera)
        edges = prereq_service.obtener_edges_por_carrera(id_carrera)

        # Mapas básicos
        id_to_info = {
            a['id_asignatura']: {
                'id_asignatura': a['id_asignatura'],
                'codigo': a['codigo'],
                'nombre': a['nombre'],
                'semestre': a.get('semestre'),
            }
            for a in asignaturas
        }

        # Grafo: prereq -> [dependientes]
        graph: Dict[int, List[int]] = {}
        for edge in edges:
            prereq_id = edge['prereq_id']
            asig_id = edge['asig_id']
            graph.setdefault(prereq_id, []).append(asig_id)

        # Conteo directo
        direct_count = {k: len(v) for k, v in graph.items()}

        # Conteo total (transitivo)
        memo: Dict[int, Set[int]] = {}

        def dfs(node: int, stack: Set[int]) -> Set[int]:
            if node in memo:
                return memo[node]
            if node in stack:
                return set()
            stack.add(node)
            deps = set()
            for nxt in graph.get(node, []):
                deps.add(nxt)
                deps.update(dfs(nxt, stack))
            stack.remove(node)
            memo[node] = deps
            return deps

        total_count: Dict[int, int] = {}
        for node in id_to_info.keys():
            total_count[node] = len(dfs(node, set()))

        resultados = []
        self.detalle_por_id.clear()
        for asig_id, info in id_to_info.items():
            direct_ids = graph.get(asig_id, [])
            total_ids = list(dfs(asig_id, set()))
            def _label(asig_id: int) -> str:
                info_item = id_to_info.get(asig_id, {})
                codigo = info_item.get('codigo') or ""
                nombre = info_item.get('nombre') or ""
                if codigo:
                    return f"{codigo} - {nombre}"
                return nombre

            def _sort_key(asig_id: int):
                info_item = id_to_info.get(asig_id, {})
                semestre = info_item.get('semestre')
                try:
                    semestre_val = int(semestre)
                except Exception:
                    semestre_val = 9999
                nombre = info_item.get('nombre') or ""
                return (semestre_val, nombre)

            direct_ids_sorted = sorted(
                [i for i in direct_ids if i in id_to_info], key=_sort_key
            )
            total_ids_sorted = sorted(
                [i for i in total_ids if i in id_to_info], key=_sort_key
            )

            direct_names = [_label(i) for i in direct_ids_sorted]
            total_names = [_label(i) for i in total_ids_sorted]

            self.detalle_por_id[asig_id] = {
                'nombre': info['nombre'],
                'directos': direct_names,
                'totales': total_names,
            }
            resultados.append(
                {
                    **info,
                    'bloquea_directo': direct_count.get(asig_id, 0),
                    'bloquea_total': total_count.get(asig_id, 0),
                }
            )

        resultados.sort(
            key=lambda x: (x['bloquea_total'], x['bloquea_directo'], x['nombre']),
            reverse=True,
        )
        return resultados

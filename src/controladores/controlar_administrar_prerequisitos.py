from typing import Dict, Any, List
from tkinter.messagebox import askyesno, showinfo, showwarning
from tkinter import Listbox, END as TK_END
from ttkbootstrap import Button, Entry, StringVar, IntVar, Label, Combobox
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from modelos.services.prerequisito_service import PrerrequisitoService
from modelos.services.asignatura_service import AsignaturaService
from modelos.services.carrera_service import CarreraService
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControlarAdministrarPrerequisitos:

    def __init__(
        self,
        master=None,
        map_widgets: Dict[str, Any] = None,
        map_vars: Dict[str, Any] = None,
    ):
        # Variables y Widgets del Frame
        self.master = master
        self.map_widgets = map_widgets
        self.map_vars = map_vars

        # Diccionarios para carreras
        self.dict_carreras: Dict[int, str] = {}
        self.dict_carreras_inv: Dict[str, int] = {}

        # Diccionarios para asignaturas completas
        self.dict_asignaturas: Dict[int, Dict[str, Any]] = {}  # id -> {codigo, nombre, id_carrera}
        self.lista_asignaturas_filtradas: List[int] = []  # IDs de asignaturas filtradas

        # ID de la asignatura seleccionada actualmente
        self.id_asignatura_actual: int = 0

        # cargar widgets
        self._cargar_widgets()

        # cargar los vars
        self._cargar_vars()

        # cargar las carreras en el filtro
        self._cargar_carreras()

        # cargar todas las asignaturas
        self._cargar_asignaturas()

        # mostrar las estadisticas en el panel inferior
        self._actualizar_estadisticas()

        # vincular los eventos
        self._vincular_eventos()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos Privados
    # └────────────────────────────────────────────────────────────┘
    def _vincular_eventos(self):
        # Evento de selección en el listbox de asignaturas
        self.listbox_asignaturas.bind("<<ListboxSelect>>", self._on_asignatura_seleccionada)

        # Evento de cambio en el filtro de carrera
        self.cbx_carrera_filtro.bind("<<ComboboxSelected>>", self._on_carrera_filtro_cambiada)

        # Evento de búsqueda rápida
        self.entry_buscar_asignatura.bind("<KeyRelease>", self._on_buscar_asignatura)

        # Botón agregar prerequisito
        self.btn_agregar_prerequisito.config(command=self._on_agregar_prerequisito)

        # Doble click en tabla de prerequisitos para eliminar
        self.tabla_prerequisitos_actuales.view.bind(
            "<Double-Button-1>", self._on_eliminar_prerequisito
        )

    def _cargar_vars(self):
        self.var_id_asignatura_seleccionada: IntVar = self.map_vars[
            'var_id_asignatura_seleccionada'
        ]
        self.var_nombre_asignatura_seleccionada: StringVar = self.map_vars[
            'var_nombre_asignatura_seleccionada'
        ]
        self.var_id_carrera_filtro: IntVar = self.map_vars['var_id_carrera_filtro']
        self.var_nombre_carrera_filtro: StringVar = self.map_vars['var_nombre_carrera_filtro']
        self.var_prerequisito_seleccionado: StringVar = self.map_vars[
            'var_prerequisito_seleccionado'
        ]

    def _cargar_widgets(self):
        self.listbox_asignaturas: Listbox = self.map_widgets['listbox_asignaturas']
        self.entry_buscar_asignatura: Entry = self.map_widgets['entry_buscar_asignatura']
        self.cbx_carrera_filtro: Combobox = self.map_widgets['cbx_carrera_filtro']
        self.lbl_asignatura_seleccionada: Label = self.map_widgets['lbl_asignatura_seleccionada']
        self.tabla_prerequisitos_actuales: Tableview = self.map_widgets[
            'tabla_prerequisitos_actuales'
        ]
        self.cbx_prerequisito_agregar: Combobox = self.map_widgets['cbx_prerequisito_agregar']
        self.btn_agregar_prerequisito: Button = self.map_widgets['btn_agregar_prerequisito']
        self.lbl_estadisticas: Label = self.map_widgets['lbl_estadisticas']

    def _cargar_carreras(self):
        """Carga todas las carreras para el filtro."""
        try:
            self.dict_carreras.clear()
            self.dict_carreras_inv.clear()

            servicio_carrera = CarreraService(ruta_db=None)
            lista_aux = servicio_carrera.obtener_id_codigo_nombre()

            if lista_aux:
                labels_carreras = ["Todas las Carreras"]
                self.dict_carreras[0] = "Todas las Carreras"
                self.dict_carreras_inv["Todas las Carreras"] = 0

                for data in lista_aux:
                    id_carrera = data.get('id_carrera')
                    codigo = data.get('codigo')
                    nombre = data.get('nombre')
                    label_carrera = f"{codigo} - {nombre}"
                    self.dict_carreras[id_carrera] = label_carrera
                    self.dict_carreras_inv[label_carrera] = id_carrera
                    labels_carreras.append(label_carrera)

                self.cbx_carrera_filtro['values'] = labels_carreras
                self.var_nombre_carrera_filtro.set("Todas las Carreras")
                logger.info(f"Se cargaron {len(labels_carreras)-1} carreras en el filtro")
            else:
                self.cbx_carrera_filtro['values'] = ["Todas las Carreras"]
                self.var_nombre_carrera_filtro.set("Todas las Carreras")

        except Exception as e:
            logger.error(f"Error al cargar carreras: {e}")
            self.cbx_carrera_filtro['values'] = ["Todas las Carreras"]

    def _cargar_asignaturas(self):
        """Carga todas las asignaturas en memoria."""
        try:
            self.dict_asignaturas.clear()

            servicio_asignatura = AsignaturaService(ruta_db=None)
            lista_aux = servicio_asignatura.obtener_id_codigo_nombre_carrera()

            if lista_aux:
                for data in lista_aux:
                    id_asignatura = data.get('id_asignatura')
                    self.dict_asignaturas[id_asignatura] = {
                        'codigo': data.get('codigo'),
                        'nombre': data.get('nombre'),
                        'id_carrera': data.get('id_carrera'),
                    }
                logger.info(f"Se cargaron {len(self.dict_asignaturas)} asignaturas")

                # Actualizar el listbox con todas las asignaturas
                self._actualizar_listbox_asignaturas()
            else:
                logger.warning("No se encontraron asignaturas")

        except Exception as e:
            logger.error(f"Error al cargar asignaturas: {e}")

    def _actualizar_listbox_asignaturas(self, filtro_texto: str = ""):
        """Actualiza el listbox con las asignaturas filtradas."""
        try:
            # Limpiar listbox
            self.listbox_asignaturas.delete(0, TK_END)
            self.lista_asignaturas_filtradas.clear()

            # Obtener filtro de carrera
            id_carrera_filtro = self.var_id_carrera_filtro.get()

            # Filtrar y agregar asignaturas
            for id_asig, datos in sorted(
                self.dict_asignaturas.items(), key=lambda x: x[1]['codigo']
            ):
                # Filtro por carrera
                if id_carrera_filtro != 0 and datos['id_carrera'] != id_carrera_filtro:
                    continue

                # Filtro por texto de búsqueda
                if filtro_texto:
                    texto_busqueda = f"{datos['codigo']} {datos['nombre']}".lower()
                    if filtro_texto.lower() not in texto_busqueda:
                        continue

                # Agregar al listbox
                label = f"{datos['codigo']:8s} - {datos['nombre']}"
                self.listbox_asignaturas.insert(TK_END, label)
                self.lista_asignaturas_filtradas.append(id_asig)

            logger.debug(
                f"Listbox actualizado con {len(self.lista_asignaturas_filtradas)} asignaturas"
            )

        except Exception as e:
            logger.error(f"Error al actualizar listbox: {e}")

    def _cargar_prerequisitos_actuales(self, id_asignatura: int):
        """Carga los prerequisitos de la asignatura seleccionada."""
        try:
            # Limpiar tabla
            self.tabla_prerequisitos_actuales.delete_rows()

            if id_asignatura == 0:
                return

            # Consultar prerequisitos
            servicio_prereq = PrerrequisitoService(ruta_db=None)
            lista_aux = servicio_prereq.obtener_por_asignatura(id_asignatura)

            if lista_aux:
                for data in lista_aux:
                    id_prereq = data.get('id_asignatura_prerrequisito')
                    if id_prereq in self.dict_asignaturas:
                        datos_prereq = self.dict_asignaturas[id_prereq]
                        self.tabla_prerequisitos_actuales.insert_row(
                            index=END,
                            values=(datos_prereq['codigo'], datos_prereq['nombre'], "🗑️ Eliminar"),
                        )

                self.tabla_prerequisitos_actuales.autofit_columns()
                logger.debug(
                    f"Se cargaron {len(lista_aux)} prerequisitos para asignatura {id_asignatura}"
                )

        except Exception as e:
            logger.error(f"Error al cargar prerequisitos actuales: {e}")

    def _cargar_combobox_prerequisitos_disponibles(self, id_asignatura: int):
        """Carga asignaturas disponibles para agregar como prerequisito."""
        try:
            if id_asignatura == 0:
                self.cbx_prerequisito_agregar['values'] = []
                return

            # Obtener prerequisitos actuales
            servicio_prereq = PrerrequisitoService(ruta_db=None)
            prerequisitos_actuales = servicio_prereq.obtener_por_asignatura(id_asignatura)

            ids_prerequisitos_actuales = set()
            if prerequisitos_actuales:
                ids_prerequisitos_actuales = {
                    p.get('id_asignatura_prerrequisito') for p in prerequisitos_actuales
                }

            # Filtrar asignaturas disponibles
            asignaturas_disponibles = []
            id_carrera_actual = self.dict_asignaturas[id_asignatura]['id_carrera']

            for id_asig, datos in sorted(
                self.dict_asignaturas.items(), key=lambda x: x[1]['codigo']
            ):
                # No puede ser prerequisito de sí misma
                if id_asig == id_asignatura:
                    continue

                # No agregar si ya es prerequisito
                if id_asig in ids_prerequisitos_actuales:
                    continue

                # Solo asignaturas de la misma carrera
                if datos['id_carrera'] != id_carrera_actual:
                    continue

                label = f"{datos['codigo']} - {datos['nombre']}"
                asignaturas_disponibles.append(label)

            self.cbx_prerequisito_agregar['values'] = asignaturas_disponibles
            logger.debug(
                f"{len(asignaturas_disponibles)} asignaturas disponibles para agregar (misma carrera)"
            )

        except Exception as e:
            logger.error(f"Error al cargar asignaturas disponibles: {e}")
            self.cbx_prerequisito_agregar['values'] = []

    def _actualizar_estadisticas(self):
        """Actualiza las estadísticas en el panel inferior."""
        try:
            total_asignaturas = len(self.dict_asignaturas)
            filtradas = len(self.lista_asignaturas_filtradas)

            msg = f"Total: {total_asignaturas} asignaturas"

            if filtradas != total_asignaturas:
                msg += f" | Mostrando: {filtradas}"

            if self.id_asignatura_actual > 0:
                datos = self.dict_asignaturas[self.id_asignatura_actual]
                msg += f" | Seleccionada: {datos['codigo']} - {datos['nombre']}"

            self.lbl_estadisticas['text'] = msg

        except Exception as e:
            logger.error(f"Error al actualizar estadísticas: {e}")
            self.lbl_estadisticas['text'] = "Error al cargar estadísticas"

    # ┌────────────────────────────────────────────────────────────┐
    # │ Eventos
    # └────────────────────────────────────────────────────────────┘

    def _on_carrera_filtro_cambiada(self, event=None):
        """Maneja el cambio de filtro de carrera."""
        try:
            label_carrera = self.var_nombre_carrera_filtro.get()
            id_carrera = self.dict_carreras_inv.get(label_carrera, 0)
            self.var_id_carrera_filtro.set(id_carrera)

            # Actualizar listbox
            self._actualizar_listbox_asignaturas()
            self._actualizar_estadisticas()

            logger.info(f"Filtro de carrera cambiado a: {label_carrera}")

        except Exception as e:
            logger.error(f"Error al cambiar filtro de carrera: {e}")

    def _on_buscar_asignatura(self, event=None):
        """Maneja la búsqueda en tiempo real."""
        try:
            texto_busqueda = self.entry_buscar_asignatura.get()
            self._actualizar_listbox_asignaturas(filtro_texto=texto_busqueda)
            self._actualizar_estadisticas()

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")

    def _on_asignatura_seleccionada(self, event=None):
        """Maneja la selección de una asignatura en el listbox."""
        try:
            seleccion = self.listbox_asignaturas.curselection()
            if not seleccion:
                return

            indice = seleccion[0]
            if indice >= len(self.lista_asignaturas_filtradas):
                return

            # Obtener ID de la asignatura seleccionada
            id_asignatura = self.lista_asignaturas_filtradas[indice]
            self.id_asignatura_actual = id_asignatura
            self.var_id_asignatura_seleccionada.set(id_asignatura)

            # Actualizar UI
            datos = self.dict_asignaturas[id_asignatura]
            label = f"{datos['codigo']} - {datos['nombre']}"
            self.var_nombre_asignatura_seleccionada.set(label)

            # Cargar prerequisitos actuales
            self._cargar_prerequisitos_actuales(id_asignatura)

            # Cargar asignaturas disponibles para agregar
            self._cargar_combobox_prerequisitos_disponibles(id_asignatura)

            # Actualizar estadísticas
            self._actualizar_estadisticas()

            logger.info(f"Asignatura seleccionada: {label}")

        except Exception as e:
            logger.error(f"Error al seleccionar asignatura: {e}")

    def _on_agregar_prerequisito(self):
        """Agrega un prerequisito a la asignatura seleccionada."""
        try:
            if self.id_asignatura_actual == 0:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar una asignatura primero",
                )
                return

            label_prerequisito = self.var_prerequisito_seleccionado.get()
            if not label_prerequisito:
                showwarning(
                    parent=self.master,
                    title="Advertencia",
                    message="Debe seleccionar una asignatura para agregar como prerequisito",
                )
                return

            # Extraer código de la asignatura prerequisito
            codigo_prereq = label_prerequisito.split(" - ")[0]

            # Buscar ID del prerequisito
            id_prerequisito = None
            for id_asig, datos in self.dict_asignaturas.items():
                if datos['codigo'] == codigo_prereq:
                    id_prerequisito = id_asig
                    break

            if not id_prerequisito:
                showwarning(
                    parent=self.master,
                    title="Error",
                    message="No se encontró la asignatura seleccionada",
                )
                return

            # Crear y guardar prerequisito
            prerequisito = PrerrequisitoService(ruta_db=None)
            prerequisito.id_asignatura = self.id_asignatura_actual
            prerequisito.id_asignatura_prerrequisito = id_prerequisito

            resultado = prerequisito.insertar()
            if resultado:
                showinfo(
                    parent=self.master,
                    title="Éxito",
                    message="Prerequisito agregado correctamente",
                )
                # Recargar prerequisitos
                self._cargar_prerequisitos_actuales(self.id_asignatura_actual)
                self._cargar_combobox_prerequisitos_disponibles(self.id_asignatura_actual)
                self.var_prerequisito_seleccionado.set("")
            else:
                showwarning(
                    parent=self.master,
                    title="Error",
                    message="No se pudo agregar el prerequisito (puede que ya exista)",
                )

        except Exception as e:
            logger.error(f"Error al agregar prerequisito: {e}")
            showwarning(
                parent=self.master,
                title="Error",
                message=f"Error inesperado: {str(e)}",
            )

    def _on_eliminar_prerequisito(self, event=None):
        """Elimina un prerequisito al hacer doble click."""
        try:
            if self.id_asignatura_actual == 0:
                return

            seleccion = self.tabla_prerequisitos_actuales.view.selection()
            if not seleccion:
                return

            # Obtener valores de la fila
            item = self.tabla_prerequisitos_actuales.view.item(seleccion[0])
            valores = item['values']
            codigo_prereq = valores[0]
            nombre_prereq = valores[1]

            # Confirmar eliminación
            confirmacion = askyesno(
                parent=self.master,
                title="Confirmar Eliminación",
                message=f"¿Desea eliminar el prerequisito:\n{codigo_prereq} - {nombre_prereq}?",
            )

            if not confirmacion:
                return

            # Buscar ID del prerequisito
            id_prerequisito = None
            for id_asig, datos in self.dict_asignaturas.items():
                if datos['codigo'] == codigo_prereq:
                    id_prerequisito = id_asig
                    break

            if not id_prerequisito:
                return

            # Eliminar prerequisito
            prerequisito = PrerrequisitoService(ruta_db=None)
            prerequisito.id_asignatura = self.id_asignatura_actual
            prerequisito.id_asignatura_prerrequisito = id_prerequisito

            if prerequisito.eliminar():
                showinfo(
                    parent=self.master,
                    title="Éxito",
                    message="Prerequisito eliminado correctamente",
                )
                # Recargar prerequisitos
                self._cargar_prerequisitos_actuales(self.id_asignatura_actual)
                self._cargar_combobox_prerequisitos_disponibles(self.id_asignatura_actual)
            else:
                showwarning(
                    parent=self.master,
                    title="Error",
                    message="No se pudo eliminar el prerequisito",
                )

        except Exception as e:
            logger.error(f"Error al eliminar prerequisito: {e}")

import calendar
from typing import Dict, Any, List
from ttkbootstrap import Frame, Label, Button, StringVar, Separator
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from datetime import datetime
from modelos.services.consulta_service import EventosUnificadosService
from modelos.dtos.consulta_dto import EventosUnificadosDTO
from scripts.logging_config import obtener_logger_modulo

logger = obtener_logger_modulo(__name__)


class ControladorCalendario:
    def __init__(self, map_vars: Dict[str, Any], map_widgets: Dict[str, Any]):
        self.map_vars: Dict[str, Any] = map_vars
        self.map_widgets: Dict[str, Any] = map_widgets

        # Variables de navegación
        self.mes_actual = datetime.now().month
        self.año_actual = datetime.now().year
        self.dia_actual = datetime.now().day

        # Mapa de dias del mes
        self.map_dias_mes: Dict[int, Label] = {}
        self.map_frame_dias: Dict[int, Frame] = {}
        self.eventos_del_mes: List[EventosUnificadosService] = []
        self.eventos_por_dia: Dict[int, List] = {}  # Almacenar eventos por día

        # cargar los widgets y variables
        self._cargar_widgets()
        self._cargar_vars()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Carga
    # └────────────────────────────────────────────────────────────┘
    def _cargar_widgets(self):
        """Carga los widgets del frame calendario."""
        self.frame_calendario: Frame = self.map_widgets.get('frame_calendario')
        self.frame_agenda: Frame = self.map_widgets.get('frame_agenda')

        # Botones de navegación
        self.btn_anterior: Button = self.map_widgets.get('btn_anterior')
        self.btn_siguiente: Button = self.map_widgets.get('btn_siguiente')
        self.btn_hoy: Button = self.map_widgets.get('btn_hoy')

        # Label de mes/año
        self.lbl_mes_año: Label = self.map_widgets.get('lbl_mes_año')

        # Combobox de filtros
        self.cbx_carrera = self.map_widgets.get('cbx_carrera')
        self.cbx_tipo_actividad = self.map_widgets.get('cbx_tipo_actividad')
        self.cbx_estado_actividad = self.map_widgets.get('cbx_estado_actividad')

        self.treeview_eventos = self.map_widgets.get('treeview_eventos')

        # Conectar eventos
        if self.btn_anterior:
            self.btn_anterior.config(command=self._mes_anterior)
        if self.btn_siguiente:
            self.btn_siguiente.config(command=self._mes_siguiente)
        if self.btn_hoy:
            self.btn_hoy.config(command=self._ir_mes_actual)

        # Actualizar el label con la fecha actual
        self._actualizar_mes_año()

    def _cargar_vars(self):
        """Carga las variables del frame calendario."""
        self.var_carrera: StringVar = self.map_vars.get('var_carrera')
        self.var_tipo_actividad: StringVar = self.map_vars.get('var_tipo_actividad')
        self.var_estado_actividad: StringVar = self.map_vars.get('var_estado_activdad')

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos de Navegación de Meses
    # └────────────────────────────────────────────────────────────┘
    def _obtener_mes_año(self) -> str:
        """Obtiene el formato: Día de la semana, dd de Mes de Año."""
        meses = [
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'Julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre',
        ]
        dias_semana = [
            'Lunes',
            'Martes',
            'Miércoles',
            'Jueves',
            'Viernes',
            'Sábado',
            'Domingo',
        ]

        # Obtener el día de la semana (0=lunes, 6=domingo)
        fecha = datetime(self.año_actual, self.mes_actual, self.dia_actual)
        dia_semana = dias_semana[fecha.weekday()]

        return f"{dia_semana}, {self.dia_actual:02d} de {meses[self.mes_actual - 1]} de {self.año_actual}"

    def _mes_anterior(self):
        """Navega al mes anterior."""
        if self.mes_actual == 1:
            self.mes_actual = 12
            self.año_actual -= 1
        else:
            self.mes_actual -= 1
        self._actualizar_mes_año()

    def _mes_siguiente(self):
        """Navega al mes siguiente."""
        if self.mes_actual == 12:
            self.mes_actual = 1
            self.año_actual += 1
        else:
            self.mes_actual += 1
        self._actualizar_mes_año()

    def _ir_mes_actual(self):
        """Vuelve al mes y año actual."""
        ahora = datetime.now()
        self.mes_actual = ahora.month
        self.año_actual = ahora.year
        self.dia_actual = ahora.day
        self._actualizar_mes_año()

    def _actualizar_mes_año(self):
        """Actualiza el label del mes/año."""
        if self.lbl_mes_año:
            self.lbl_mes_año.config(text=self._obtener_mes_año())
        self._cargar_calendario()
        self._cargar_agenda()
        # cargamos los eventos en la agenda
        self._cargar_eventos_agenda()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Cargar Calendario
    # └────────────────────────────────────────────────────────────┘
    def _cargar_calendario(self):
        """Carga el calendario del mes actual en grid."""
        # Limpiar el frame anterior
        for widget in self.frame_calendario.winfo_children():
            widget.destroy()

        dias_del_mes = calendar.monthcalendar(year=self.año_actual, month=self.mes_actual)

        lista_nom_dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sab", "Dom"]

        # Frame principal para todo el calendario
        frame_calendario = Frame(self.frame_calendario, padding=(1, 1))
        frame_calendario.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        # Configurar columnas para que se expandan (8 columnas: 1 para semana + 7 para días)
        frame_calendario.columnconfigure(0, weight=0)  # Columna de semana (sin expandir)
        for col in range(1, 8):
            frame_calendario.columnconfigure(col, weight=1)

        # Configurar filas para que se expandan
        frame_calendario.rowconfigure(0, weight=0)  # Encabezado
        for fila in range(1, len(dias_del_mes) + 1):
            frame_calendario.rowconfigure(fila, weight=1)

        # Encabezado de número de semana
        lbl_semana = Button(
            frame_calendario,
            text="Sem",
            bootstyle=SECONDARY,
        )
        lbl_semana.grid(row=0, column=0, sticky=NSEW, padx=0, pady=0)

        # Encabezados de días de la semana
        for col, nom_dia in enumerate(lista_nom_dias, start=1):
            lbl_nom_dia = Button(
                frame_calendario,
                text=nom_dia,
                # anchor=CENTER, # solo en caso de que sea un Label
                # justify=CENTER, # solo en caso de que sea un Label
                # font=("Helvetica", 10, "bold"), # solo en caso de que sea un Label
                bootstyle=PRIMARY,
            )
            lbl_nom_dia.grid(row=0, column=col, sticky=NSEW, padx=0, pady=0)

        # Cargar días del mes
        if dias_del_mes:
            for fila, dias in enumerate(dias_del_mes, start=1):
                self._frame_mes(
                    frame=frame_calendario, fila=fila, lista=dias, dia_actual=self.dia_actual
                )

    def _frame_mes(self, frame: Frame, fila: int, lista: List = [], dia_actual: int = None) -> None:
        """Carga una fila de días del mes en grid."""
        if lista:
            # Obtener el número de semana del primer día válido de la semana
            num_semana = None
            for dia in lista:
                if dia != 0:
                    fecha = datetime(self.año_actual, self.mes_actual, dia)
                    num_semana = fecha.isocalendar()[1]
                    break

            # Crear label del número de semana
            if num_semana:
                lbl_semana = Label(
                    frame,
                    text=f"S{num_semana:02d}",
                    anchor=CENTER,
                    justify=CENTER,
                    bootstyle=SECONDARY,
                    font=("Helvetica", 9, "bold"),
                    width=4,
                )
            else:
                lbl_semana = Label(frame, text="", anchor=CENTER, justify=CENTER)

            lbl_semana.grid(row=fila, column=0, sticky=NSEW, padx=2, pady=5)

            # Cargar los días de la semana
            for col, dia in enumerate(lista, start=1):
                if dia == 0:
                    lbl_dia = Label(frame, text="", anchor=CENTER, justify=CENTER)
                else:
                    # Resaltar el día actual
                    if dia == dia_actual:
                        lbl_dia = Label(
                            frame,
                            text=str(dia),
                            anchor=CENTER,
                            justify=CENTER,
                            bootstyle=SUCCESS,
                            font=("Helvetica", 12, "bold"),
                            width=5,
                        )
                    else:
                        lbl_dia = Label(
                            frame,
                            text=str(dia),
                            anchor=CENTER,
                            justify=CENTER,
                            # bootstyle=PRIMARY,
                            font=("Helvetica", 10),
                            width=5,
                        )
                lbl_dia.grid(row=fila, column=col, sticky=NSEW, padx=5, pady=5)
                self.map_dias_mes[dia] = lbl_dia

                # Agregar evento de double-click si el día tiene eventos
                if dia != 0:
                    lbl_dia.bind('<Double-1>', lambda event, d=dia: self._on_dia_doble_click(d))

    # ┌────────────────────────────────────────────────────────────┐
    # │ Cargar Agenda
    # └────────────────────────────────────────────────────────────┘
    def _cargar_agenda(self):
        # Limpiar el frame anterior
        for widget in self.frame_agenda.winfo_children():
            widget.destroy()

        # Scroll Frame
        scroll_frame = ScrolledFrame(self.frame_agenda, autohide=True)
        scroll_frame.pack(side=TOP, fill=BOTH, padx=1, pady=1, expand=True)

        dias_mes = calendar.monthcalendar(year=self.año_actual, month=self.mes_actual)

        self._agenda(dias_mes=dias_mes, scroll_frame=scroll_frame)

    def _agenda(self, dias_mes: List, scroll_frame: ScrolledFrame):
        # limpiamos el frame scroll
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        for semana in dias_mes:
            self._plantilla_agenda(semana=semana, scroll_frame=scroll_frame)

    def _plantilla_agenda(self, semana: List, scroll_frame: ScrolledFrame):
        if semana:
            # Obtener el número de semana del primer día válido
            num_semana = None
            for dia in semana:
                if dia != 0:
                    fecha = datetime(self.año_actual, self.mes_actual, dia)
                    num_semana = fecha.isocalendar()[1]
                    break

            # Agregar encabezado de número de semana
            if num_semana:
                frame_semana = Frame(scroll_frame, padding=(1, 1))
                frame_semana.pack(fill=X, expand=True)
                lbl_semana = Label(
                    frame_semana,
                    text=f"Semana {num_semana:02d}",
                    bootstyle=SECONDARY,
                    font=("Helvetica", 10, "bold"),
                )
                lbl_semana.pack(side=LEFT, padx=5, pady=5)
                Separator(scroll_frame, orient=HORIZONTAL).pack(fill=X, expand=True)

            # Agregar días de la semana
            for dia in semana:
                if dia != 0:
                    frame = Frame(scroll_frame, padding=(1, 1))
                    frame.pack(fill=X, expand=True)
                    lbl_dia = Label(frame, text=str(dia), bootstyle=SECONDARY)
                    lbl_dia.pack(side=LEFT, padx=5, pady=5)
                    Separator(scroll_frame, orient=HORIZONTAL).pack(fill=X, expand=True)
                    self.map_frame_dias[dia] = frame

    def _obtener_eventos_por_mes(self):
        """Obtiene eventos del mes actual desde la base de datos."""
        try:
            eventos_service = EventosUnificadosService(ruta_db=None)
            self.eventos_del_mes.clear()

            self.eventos_del_mes = eventos_service.obtener_por_mes(
                ano=self.año_actual, mes=self.mes_actual
            )

            logger.info(
                f"✅ Obtenidos {len(self.eventos_del_mes)} eventos para "
                f"{self.año_actual}-{self.mes_actual:02d}"
            )

        except Exception as e:
            logger.error(
                f"❌ Error al obtener eventos del mes {self.año_actual}-{self.mes_actual:02d}: {e}",
                exc_info=True,
            )
            self.eventos_del_mes.clear()

    # ┌────────────────────────────────────────────────────────────┐
    # │ Cargamos los eventos en el Calendario y la Agenda
    # └────────────────────────────────────────────────────────────┘
    def _cargar_eventos_agenda(self):
        """Carga eventos en el frame_agenda para cada día del mes."""
        try:
            eventos_service = EventosUnificadosService(ruta_db=None)

            # Obtener todos los eventos del mes
            lista_eventos = eventos_service.obtener_por_mes(
                ano=self.año_actual, mes=self.mes_actual
            )

            if not lista_eventos:
                logger.info(f"No hay eventos para {self.año_actual}-{self.mes_actual:02d}")
                return

            # Agrupar eventos por fecha (incluyendo fecha de inicio y fin)
            eventos_por_fecha = {}
            for evento in lista_eventos:
                # Agregar evento a fecha de inicio
                fecha_inicio = evento.fecha_inicio
                if fecha_inicio not in eventos_por_fecha:
                    eventos_por_fecha[fecha_inicio] = []
                eventos_por_fecha[fecha_inicio].append((evento, 'inicio'))

                # Agregar evento a fecha de fin (si es diferente a la de inicio)
                fecha_fin = evento.fecha_fin
                if fecha_fin and fecha_fin != fecha_inicio:
                    if fecha_fin not in eventos_por_fecha:
                        eventos_por_fecha[fecha_fin] = []
                    eventos_por_fecha[fecha_fin].append((evento, 'fin'))

            logger.info(f"✅ Encontrados eventos para {len(eventos_por_fecha)} fechas")

            # Guardar eventos por día para acceso posterior (solo por fecha de inicio)
            self.eventos_por_dia.clear()
            for evento in lista_eventos:
                fecha = evento.fecha_inicio
                dia = int(fecha.split('-')[2])
                if dia not in self.eventos_por_dia:
                    self.eventos_por_dia[dia] = []
                self.eventos_por_dia[dia].append(evento)

            # Mostrar eventos en la agenda (en los frames creados en _plantilla_agenda)
            for fecha, eventos_con_tipo in eventos_por_fecha.items():
                # Extraer día de la fecha (YYYY-MM-DD)
                dia = int(fecha.split('-')[2])

                # Obtener el frame del día de la agenda
                frame_dia = self.map_frame_dias.get(dia)

                if frame_dia:
                    # Agregar eventos al frame del día
                    for evento, tipo_fecha in eventos_con_tipo:
                        # Construir el texto con asignatura y carrera si es actividad
                        if evento.es_actividad():
                            # Mostrar asignatura y carrera si están disponibles
                            metadata = []
                            if evento.asignatura:
                                metadata.append(evento.asignatura)
                            if evento.carrera:
                                metadata.append(evento.carrera)

                            if metadata:
                                texto = f"• {evento.titulo} ({' - '.join(metadata)})"
                            else:
                                texto = f"• {evento.titulo}"
                        else:
                            texto = f"• {evento.titulo}"

                        # Agregar indicador de inicio/fin y estilos según tipo de evento
                        if evento.es_actividad():
                            # Evento de Actividad
                            if tipo_fecha == 'fin':
                                texto = f"{texto} [FIN]"
                                bootstyle_evento = WARNING
                            else:  # tipo_fecha == 'inicio'
                                texto = f"{texto} [INICIO]"
                                bootstyle_evento = SUCCESS
                        else:
                            # Evento de Calendario
                            bootstyle_evento = INFO

                        lbl_evento = Label(
                            frame_dia,
                            text=texto,
                            font=("Helvetica", 8),
                            bootstyle=bootstyle_evento,
                        )

                        lbl_evento.pack(side=TOP, fill=X, padx=10, pady=2)
                        logger.debug(f"Evento agregado: {texto} en día {dia}")

            # Marcar días con eventos en el calendario
            self._marcar_dias_con_eventos(eventos_por_fecha)

        except Exception as e:
            logger.error(f"❌ Error al cargar eventos en agenda: {e}", exc_info=True)

    def _marcar_dias_con_eventos(self, eventos_por_fecha: Dict[str, List]) -> None:
        """Marca los días en el calendario que tienen eventos.

        Args:
            eventos_por_fecha: Diccionario con fechas como claves y lista de eventos como valores.
                              Las fechas deben estar en formato 'YYYY-MM-DD'.
        """
        try:
            for fecha, eventos in eventos_por_fecha.items():
                # Extraer día de la fecha (YYYY-MM-DD)
                dia = int(fecha.split('-')[2])

                # Obtener el label del día en el calendario
                lbl_dia = self.map_dias_mes.get(dia)

                if lbl_dia:
                    # Cambiar el estilo del día para indicar que tiene eventos
                    num_eventos = len(eventos)

                    # Construir texto con indicador de eventos
                    texto_dia = f"{dia}\n({num_eventos})"

                    lbl_dia.config(
                        text=texto_dia,
                        bootstyle="warning",  # Cambiar a color de advertencia/eventos
                        font=("Helvetica", 10, "bold"),
                    )
                    logger.debug(f"Día {dia} marcado con {num_eventos} evento(s)")

        except Exception as e:
            logger.error(f"❌ Error al marcar días con eventos: {e}", exc_info=True)

    # ┌────────────────────────────────────────────────────────────┐
    # │ Métodos para Manejo de Eventos del Calendario
    # └────────────────────────────────────────────────────────────┘
    def _on_dia_doble_click(self, dia: int) -> None:
        """Maneja el doble click en un día del calendario.

        Args:
            dia: El número del día del mes que fue clickeado.
        """
        # Verificar si el día tiene eventos
        eventos = self.eventos_por_dia.get(dia, [])

        if eventos:
            self._cargar_eventos_treeview(dia, eventos)
            logger.debug(f"Doble click en día {dia} con {len(eventos)} evento(s)")
        else:
            logger.debug(f"Doble click en día {dia} - sin eventos")

    def _cargar_eventos_treeview(self, dia: int, eventos: List) -> None:
        """Carga los eventos de un día específico en el treeview.

        Args:
            dia: El número del día del mes.
            eventos: Lista de eventos del día.
        """
        if not self.treeview_eventos:
            logger.warning("⚠️ treeview_eventos no está disponible")
            return

        try:
            # Limpiar el treeview
            for item in self.treeview_eventos.get_children():
                self.treeview_eventos.delete(item)

            # Configurar las columnas del treeview si es necesario
            columnas = (
                'titulo',
                'tipo',
                'carrera',
                'asignatura',
                'hora_inicio',
                'hora_fin',
                'tipo_actividad',
            )

            # Limpiar columnas existentes
            self.treeview_eventos['columns'] = columnas
            self.treeview_eventos.column('#0', width=0, stretch=False)

            # Configurar encabezados y anchos
            self.treeview_eventos.heading('#0', text='', anchor=CENTER)
            self.treeview_eventos.heading('titulo', text='Título', anchor=CENTER)
            self.treeview_eventos.heading('tipo', text='Tipo', anchor=CENTER)
            self.treeview_eventos.heading('carrera', text='Carrera', anchor=CENTER)
            self.treeview_eventos.heading('asignatura', text='Asignatura', anchor=CENTER)
            self.treeview_eventos.heading('hora_inicio', text='Inicio', anchor=CENTER)
            self.treeview_eventos.heading('hora_fin', text='Fin', anchor=CENTER)
            self.treeview_eventos.heading('tipo_actividad', text='Tipo Actividad', anchor=CENTER)

            self.treeview_eventos.column('titulo', width=150, anchor=W)
            self.treeview_eventos.column('tipo', width=80, anchor=CENTER)
            self.treeview_eventos.column('carrera', width=100, anchor=W)
            self.treeview_eventos.column('asignatura', width=100, anchor=W)
            self.treeview_eventos.column('hora_inicio', width=80, anchor=CENTER)
            self.treeview_eventos.column('hora_fin', width=80, anchor=CENTER)
            self.treeview_eventos.column('tipo_actividad', width=120, anchor=CENTER)

            # Agregar eventos al treeview
            for evento in eventos:
                # Extraer datos importantes sin IDs
                titulo = evento.titulo or ''
                tipo = 'Actividad' if evento.es_actividad() else 'Evento'
                carrera = evento.carrera or '-'
                asignatura = evento.asignatura or '-'

                # Extraer fechas/horas - Si hay espacio, tomar la hora, sino tomar la fecha
                fecha_inicio = evento.fecha_inicio or '-'
                fecha_fin = evento.fecha_fin or '-'

                # Extraer solo la parte de fecha (YYYY-MM-DD)
                if ' ' in fecha_inicio:
                    hora_inicio = fecha_inicio.split(' ')[0]  # Tomar la fecha
                else:
                    hora_inicio = fecha_inicio  # Ya es solo la fecha

                if ' ' in fecha_fin:
                    hora_fin = fecha_fin.split(' ')[0]  # Tomar la fecha
                else:
                    hora_fin = fecha_fin  # Ya es solo la fecha

                tipo_actividad = evento.tipo_actividad or '-'

                # Insertar fila en el treeview
                self.treeview_eventos.insert(
                    '',
                    'end',
                    values=(
                        titulo,
                        tipo,
                        carrera,
                        asignatura,
                        hora_inicio,
                        hora_fin,
                        tipo_actividad,
                    ),
                )

            logger.info(f"✅ Cargados {len(eventos)} eventos en treeview para el día {dia}")

        except Exception as e:
            logger.error(f"❌ Error al cargar eventos en treeview: {e}", exc_info=True)

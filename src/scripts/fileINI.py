from os.path import exists
from io import open
from typing import Dict, List, Optional

"""
Los archivos INI tienen una estructura simple pero efectiva,
diseñada para almacenar configuraciones y ajustes para programas y aplicaciones.
Su estructura se basa en secciones y claves, y se compone de texto sin formato
escrito en código ASCII.
"""


class FileINI:
    """
    Esta clase maneja archivos del tipo INI

    Args:
        pathINI: Ruta del archivo INI a manejar
    """
    # Constantes de clase
    __START_SECTION = "["
    __END_SECTION = "]"
    __SEPARATOR = "="
    __COMMENT = ";"

    def __init__(self, pathINI: str):
        self.__pathINI = pathINI
        self.__fileINI = None  # Variable para almacenar el fichero
        self.__lineas = []
        # Cargamos el archivo
        self.__load()

    def __load(self) -> None:
        """Método privado para cargar los datos del archivo INI"""
        if not self.__pathINI:
            return

        # Verificamos si existe
        if exists(self.__pathINI):
            try:
                with open(self.__pathINI, 'r', encoding='utf-8') as file:
                    # Cargamos las líneas
                    self.__lineas = file.readlines()
            except Exception as e:
                raise IOError(f"Error al leer el archivo INI: {e}")
        else:
            # Creamos el archivo si no existe
            try:
                with open(self.__pathINI, '+a', encoding='utf-8') as file:
                    pass  # Solo creamos el archivo
            except Exception as e:
                raise IOError(f"Error al crear el archivo INI: {e}")

    def __write_to_file(self) -> bool:
        """Método privado para escribir en el archivo"""
        try:
            with open(self.__pathINI, "w", encoding='utf-8') as file:
                file.writelines(self.__lineas)
            return True
        except Exception as e:
            raise IOError(f"Error al escribir en el archivo: {e}")
        finally:
            # Recargamos el archivo después de escribir
            self.__load()

    def sections(self) -> List[str]:
        """
        Lista todas las secciones en el archivo INI

        Returns:
            Lista de nombres de secciones
        """
        values = []
        for linea in self.__lineas:
            if linea.startswith(self.__START_SECTION):
                section_name = linea[1:linea.index(self.__END_SECTION)]
                values.append(section_name)
        return values

    def __index_section(self) -> Dict[str, int]:
        """
        Método privado que devuelve un diccionario con los índices de las secciones

        Returns:
            Diccionario con nombre de sección como clave e índice como valor
        """
        coll = {}
        for i, linea in enumerate(self.__lineas):
            if linea.startswith(self.__START_SECTION):
                section_name = linea[1:linea.index(self.__END_SECTION)]
                coll[section_name] = i
        return coll

    def section_exist(self, section: str) -> bool:
        """
        Verifica si existe una sección

        Args:
            section: Nombre de la sección a verificar

        Returns:
            True si la sección existe, False en caso contrario
        """
        return section in self.sections()

    def section_keys(self, section: str) -> List[str]:
        """
        Lista todas las claves de una sección

        Args:
            section: Nombre de la sección

        Returns:
            Lista de claves en la sección
        """
        lista = []
        seccion_encontrada = False

        for i, linea in enumerate(self.__lineas):
            # Detectar si estamos en la sección buscada
            if linea.startswith(self.__START_SECTION):
                current_section = linea[1:linea.index(self.__END_SECTION)]
                seccion_encontrada = (current_section == section)
                continue

            # Si estamos en la sección correcta
            if seccion_encontrada:
                # Ignorar comentarios y líneas vacías
                if linea.startswith(self.__COMMENT) or linea.strip() == '':
                    continue
                # Si encontramos otra sección, terminamos
                if linea.startswith(self.__START_SECTION):
                    break
                # Si hay un separador, es una clave-valor
                if self.__SEPARATOR in linea:
                    clave = linea.split(self.__SEPARATOR)[0].strip()
                    lista.append(clave)

        return lista

    def section_values(self, section: str) -> List[str]:
        """
        Lista todos los valores de una sección

        Args:
            section: Nombre de la sección

        Returns:
            Lista de valores en la sección
        """
        lista = []
        seccion_encontrada = False

        for linea in self.__lineas:
            # Detectar si estamos en la sección buscada
            if linea.startswith(self.__START_SECTION):
                current_section = linea[1:linea.index(self.__END_SECTION)]
                seccion_encontrada = (current_section == section)
                continue

            # Si estamos en la sección correcta
            if seccion_encontrada:
                # Ignorar comentarios y líneas vacías
                if linea.startswith(self.__COMMENT) or linea.strip() == '':
                    continue
                # Si encontramos otra sección, terminamos
                if linea.startswith(self.__START_SECTION):
                    break
                # Si hay un separador, es una clave-valor
                if self.__SEPARATOR in linea:
                    valor = linea.split(self.__SEPARATOR, 1)[1].strip()
                    lista.append(valor)

        return lista

    def keys(self) -> List[str]:
        """
        Lista todas las claves de todas las secciones

        Returns:
            Lista de strings en formato "seccion|clave"
        """
        lista = []
        for seccion in self.sections():
            for key in self.section_keys(section=seccion):
                lista.append(f"{seccion}|{key}")
        return lista

    def values(self) -> List[str]:
        """
        Lista todos los valores de todas las secciones

        Returns:
            Lista de strings en formato "seccion|valor"
        """
        lista = []
        for seccion in self.sections():
            for value in self.section_values(section=seccion):
                lista.append(f"{seccion}|{value}")
        return lista

    def key_exist(self, section: str, key: str) -> bool:
        """
        Verifica si existe una clave en una sección

        Args:
            section: Nombre de la sección
            key: Nombre de la clave

        Returns:
            True si la clave existe en la sección, False en caso contrario
        """
        comparar = f"{section}|{key}"
        return comparar in self.keys()

    def value_exist(self, section: str, value: str) -> bool:
        """
        Verifica si existe un valor en una sección

        Args:
            section: Nombre de la sección
            value: Valor a buscar

        Returns:
            True si el valor existe en la sección, False en caso contrario
        """
        comparar = f"{section}|{value}"
        return comparar in self.values()

    def __index_key(self, section: str) -> Dict[str, int]:
        """
        Método privado que devuelve un diccionario con los índices de las claves de una sección

        Args:
            section: Nombre de la sección

        Returns:
            Diccionario con clave como key e índice como valor
        """
        coll = {}
        seccion_encontrada = False

        for i, linea in enumerate(self.__lineas):
            # Detectar si estamos en la sección buscada
            if linea.startswith(self.__START_SECTION):
                current_section = linea[1:linea.index(self.__END_SECTION)]
                seccion_encontrada = (current_section == section)
                continue

            # Si estamos en la sección correcta
            if seccion_encontrada:
                # Ignorar comentarios y líneas vacías
                if linea.startswith(self.__COMMENT) or linea.strip() == '':
                    continue
                # Si encontramos otra sección, terminamos
                if linea.startswith(self.__START_SECTION):
                    break
                # Si hay un separador, es una clave-valor
                if self.__SEPARATOR in linea:
                    clave = linea.split(self.__SEPARATOR)[0].strip()
                    coll[clave] = i

        return coll

    def add_section(self, section: str, comment: Optional[str] = None) -> bool:
        """
        Agrega una sección al archivo INI

        Args:
            section: Nombre de la sección
            comment: Comentario opcional para la sección

        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        if not section or self.section_exist(section):
            return False

        # Preparar la sección para agregar
        nuevas_lineas = []

        # Si hay líneas y la última no tiene salto de línea, añadimos uno
        if self.__lineas and not self.__lineas[-1].endswith('\n'):
            nuevas_lineas.append('\n')

        # Si no hay líneas o la última no está vacía, añadimos línea en blanco
        if not self.__lineas or self.__lineas[-1].strip():
            nuevas_lineas.append('\n')

        # Añadir la sección
        nuevas_lineas.append(
            f"{self.__START_SECTION}{section}{self.__END_SECTION}\n")

        # Añadir el comentario si existe
        if comment is not None:
            nuevas_lineas.append(f"{self.__COMMENT} {comment}\n")
        else:
            nuevas_lineas.append(f"{self.__COMMENT} comentario\n")

        # Agregar las nuevas líneas
        self.__lineas.extend(nuevas_lineas)

        # Guardar los cambios
        return self.__write_to_file()

    def add_value(self, section: str, key: str, value: str) -> bool:
        """
        Agrega o actualiza un valor en una sección

        Args:
            section: Nombre de la sección
            key: Nombre de la clave
            value: Valor a asignar

        Returns:
            True si se agregó o actualizó correctamente, False en caso contrario
        """
        # Si la sección no existe, crearla
        if not self.section_exist(section):
            self.add_section(section)

        # Verificar si el key existe para actualizarlo
        if self.key_exist(section=section, key=key):
            # Si la clave existe, reemplazamos su valor
            dict_keys = self.__index_key(section=section)
            index_key = dict_keys[key]
            self.__lineas[index_key] = f"{key}{self.__SEPARATOR}{value}\n"
        else:
            # Si la clave no existe, la agregamos después del comentario de la sección
            dict_sections = self.__index_section()
            index_section = dict_sections[section]

            # Encontrar la posición correcta para insertar
            insert_pos = index_section + 1

            # Saltarse comentarios después de la sección
            while (insert_pos < len(self.__lineas) and
                   (self.__lineas[insert_pos].startswith(self.__COMMENT) or
                   self.__lineas[insert_pos].strip() == '')):
                insert_pos += 1

            # Insertar la nueva clave-valor
            self.__lineas.insert(
                insert_pos, f"{key}{self.__SEPARATOR}{value}\n")

        # Guardar los cambios
        return self.__write_to_file()

    def delete_key(self, section: str, key: str) -> str:
        """
        Borra una clave de una sección

        Args:
            section: Nombre de la sección
            key: Nombre de la clave a borrar

        Returns:
            La línea borrada o cadena vacía si no se borró nada
        """
        if not self.key_exist(section=section, key=key):
            return ""

        dict_keys = self.__index_key(section=section)
        index_key = dict_keys[key]
        val = self.__lineas.pop(index_key)

        # Guardar los cambios
        self.__write_to_file()

        return val

    def get_value(self, section: str, key: str) -> str:
        """
        Obtiene el valor de una clave en una sección

        Args:
            section: Nombre de la sección
            key: Nombre de la clave

        Returns:
            El valor de la clave o cadena vacía si no existe
        """
        if not self.section_exist(section) or not self.key_exist(section=section, key=key):
            return ""

        dict_key = self.__index_key(section=section)
        index = dict_key[key]
        linea = self.__lineas[index]
        valor = linea.split(self.__SEPARATOR, 1)[1].strip()

        return valor

    def delete_section(self, section: str) -> bool:
        """
        Borra una sección completa incluyendo sus claves y valores

        Args:
            section: Nombre de la sección a borrar

        Returns:
            True si se borró correctamente, False en caso contrario
        """
        if not self.section_exist(section):
            return False

        # Obtener el índice de la sección
        section_indices = self.__index_section()
        section_index = section_indices[section]

        # Índices a eliminar (la sección y todo su contenido)
        indices_to_remove = set()
        indices_to_remove.add(section_index)

        # Obtener índices de las claves de la sección
        key_indices = self.__index_key(section)
        indices_to_remove.update(key_indices.values())

        # Añadir índices de comentarios y líneas vacías
        i = section_index + 1
        while (i < len(self.__lineas) and
               not self.__lineas[i].startswith(self.__START_SECTION)):
            indices_to_remove.add(i)
            i += 1

        # Convertir a lista ordenada de mayor a menor
        indices_list = sorted(list(indices_to_remove), reverse=True)

        # Eliminar líneas desde el índice más alto al más bajo
        for idx in indices_list:
            if 0 <= idx < len(self.__lineas):
                self.__lineas.pop(idx)

        # Guardar los cambios
        return self.__write_to_file()

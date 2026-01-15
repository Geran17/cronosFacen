#!/usr/bin/env python3
"""
Script de prueba para verificar que la lógica de filtros funciona correctamente.
"""
import sys

sys.path.insert(0, '/home/geran/MEGA/Workspaces/proyectos/cronosFacen/src')

from modelos.daos.carrera_dao import CarreraDAO
from modelos.daos.asignatura_dao import AsignaturaDAO
from modelos.daos.eje_tematico_dao import EjeTematicoDAO


def test_filtros():
    """Prueba la lógica de filtros de carreras y asignaturas"""

    print("=" * 80)
    print("PRUEBA DE FILTROS - ADMINISTRADOR DE EJES TEMÁTICOS")
    print("=" * 80)

    try:
        # Obtener carreras
        print("\n[1] Obteniendo carreras...")
        carrera_dao = CarreraDAO(ruta_db=None)
        sql_carreras = "SELECT id_carrera, nombre FROM carrera ORDER BY nombre"
        carreras = carrera_dao.ejecutar_consulta(sql=sql_carreras, params=())

        if carreras:
            print(f"✓ Se encontraron {len(carreras)} carreras:")
            for carrera in carreras[:3]:  # Mostrar solo las primeras 3
                print(f"  - ID: {carrera['id_carrera']}, Nombre: {carrera['nombre']}")
        else:
            print("✗ No se encontraron carreras")
            return False

        # Obtener asignaturas
        print("\n[2] Obteniendo asignaturas...")
        asignatura_dao = AsignaturaDAO(ruta_db=None)
        sql_asignaturas = (
            "SELECT id_asignatura, nombre, codigo, id_carrera FROM asignatura ORDER BY nombre"
        )
        asignaturas = asignatura_dao.ejecutar_consulta(sql=sql_asignaturas, params=())

        if asignaturas:
            print(f"✓ Se encontraron {len(asignaturas)} asignaturas:")
            for asig in asignaturas[:3]:  # Mostrar solo las primeras 3
                print(
                    f"  - ID: {asig['id_asignatura']}, Nombre: {asig['nombre']}, Carrera: {asig['id_carrera']}"
                )
        else:
            print("✗ No se encontraron asignaturas")
            return False

        # Probar consulta filtrada por carrera
        print("\n[3] Probando filtro de carrera...")
        if carreras:
            id_carrera = carreras[0]['id_carrera']
            sql_asignaturas_carrera = (
                "SELECT id_asignatura, nombre FROM asignatura WHERE id_carrera = ? ORDER BY nombre"
            )
            asignaturas_carrera = asignatura_dao.ejecutar_consulta(
                sql=sql_asignaturas_carrera, params=(id_carrera,)
            )
            print(f"✓ Carrera {id_carrera}: {len(asignaturas_carrera)} asignaturas")
            for asig in asignaturas_carrera[:3]:
                print(f"  - {asig['nombre']}")

        # Probar consulta filtrada de ejes temáticos por carrera
        print("\n[4] Probando filtro de ejes temáticos por carrera...")
        eje_dao = EjeTematicoDAO(ruta_db=None)
        sql_ejes_carrera = """
            SELECT DISTINCT et.* 
            FROM eje_tematico et
            INNER JOIN asignatura a ON et.id_asignatura = a.id_asignatura
            WHERE a.id_carrera = ?
            ORDER BY a.id_carrera, et.id_asignatura, et.orden
        """

        if carreras:
            id_carrera = carreras[0]['id_carrera']
            ejes_carrera = eje_dao.ejecutar_consulta(sql=sql_ejes_carrera, params=(id_carrera,))
            print(f"✓ Carrera {id_carrera}: {len(ejes_carrera)} ejes temáticos")
            for eje in ejes_carrera[:3]:
                print(
                    f"  - ID: {eje['id_eje']}, Nombre: {eje['nombre']}, Asignatura: {eje['id_asignatura']}"
                )

        # Probar consulta filtrada de ejes por asignatura
        print("\n[5] Probando filtro de ejes temáticos por asignatura...")
        sql_ejes_asignatura = """
            SELECT * FROM eje_tematico 
            WHERE id_asignatura = ?
            ORDER BY orden
        """

        if asignaturas:
            id_asignatura = asignaturas[0]['id_asignatura']
            ejes_asignatura = eje_dao.ejecutar_consulta(
                sql=sql_ejes_asignatura, params=(id_asignatura,)
            )
            print(f"✓ Asignatura {id_asignatura}: {len(ejes_asignatura)} ejes temáticos")
            for eje in ejes_asignatura[:3]:
                print(f"  - {eje['nombre']}")

        print("\n" + "=" * 80)
        print("✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print("=" * 80)
        return True

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_filtros()
    sys.exit(0 if success else 1)

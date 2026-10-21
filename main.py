"""EcoTech Solutions - Sistema de gestión de empleados (consola).
Uso:  python main.py          menú interactivo
      python main.py --demo   demostración automática (base temporal en memoria)"""
import sys
from datetime import date

from dominio import (Credencial, Departamento, DatoInvalidoError, EcoTechError, Empleado, Perfil,
                     ParteDiario, Permiso, Proyecto, ParticipacionProyecto, RegistroDuplicadoError,
                     ReporteExcel, ReportePDF)
from repositorio import ConexionBD, DepartamentoRepositorio, EmpleadoRepositorio


# ---------- Entradas de usuario con validación ----------

def pedir_texto(mensaje, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("  Este dato es obligatorio.")


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  Ingresa un número entero válido.")


def pedir_decimal(mensaje):
    while True:
        try:
            return float(input(mensaje).replace(",", "."))
        except ValueError:
            print("  Ingresa un número válido (ej: 1500000).")


def pedir_fecha(mensaje):
    while True:
        try:
            return date.fromisoformat(input(mensaje).strip())
        except ValueError:
            print("  Fecha inválida. Usa el formato AAAA-MM-DD (ej: 2024-04-01).")


# ---------- Acciones del menú ----------

def registrar_empleado(repo_emp, repo_dep):
    empleado = Empleado(pedir_entero("Id: "), pedir_texto("Nombre completo: "),
                        pedir_texto("Dirección: ", False), pedir_texto("Teléfono: ", False),
                        pedir_texto("Correo: "), pedir_decimal("Sueldo base: "),
                        pedir_fecha("Fecha de ingreso (AAAA-MM-DD): "))
    codigo = pedir_texto("Código de departamento (Enter para ninguno): ", False)
    if codigo:
        empleado.cambiarDepartamento(repo_dep.obtener_por_codigo(int(codigo)))
    repo_emp.guardar(empleado)
    print("Empleado registrado.")


def listar_empleados(repo_emp):
    empleados = repo_emp.listar_activos()
    if not empleados:
        print("No hay empleados registrados.")
    for e in empleados:
        print(" ", e)


def buscar_empleado(repo_emp):
    print(repo_emp.obtener_por_id(pedir_entero("Id a buscar: ")))


def actualizar_empleado(repo_emp):
    empleado = repo_emp.obtener_por_id(pedir_entero("Id del empleado a actualizar: "))
    print("Actual:", empleado)
    empleado.sueldoBase = pedir_decimal("Nuevo sueldo base: ")
    repo_emp.actualizar(empleado)
    print("Empleado actualizado.")


def eliminar_empleado(repo_emp):
    repo_emp.eliminar(pedir_entero("Id del empleado a eliminar: "))
    print("Empleado eliminado.")


def crear_departamento(repo_dep):
    repo_dep.guardar(Departamento(pedir_entero("Código: "), pedir_texto("Nombre: ")))
    print("Departamento creado.")


def listar_departamentos(repo_dep):
    deptos = repo_dep.listar()
    if not deptos:
        print("No hay departamentos registrados.")
    for d in deptos:
        print(" ", d)


def eliminar_departamento(repo_dep):
    repo_dep.eliminar(pedir_entero("Código del departamento a eliminar: "))
    print("Departamento eliminado.")


def registrar_con_credencial(repo_emp):
    empleado = Empleado(pedir_entero("Id: "), pedir_texto("Nombre completo: "), "", "",
                        pedir_texto("Correo: "), pedir_decimal("Sueldo base: "),
                        pedir_fecha("Fecha de ingreso (AAAA-MM-DD): "))
    credencial = Credencial(empleado, pedir_texto("Nombre de usuario: "),
                            pedir_texto("Clave (mínimo 8 caracteres): "), Perfil(pedir_texto("Perfil: ")))
    repo_emp.registrar_con_credencial(empleado, credencial)
    print("Empleado y credencial registrados.")


# ---------- Demostración automática ----------

def titulo(texto):
    print(f"\n>>> {texto}")


def demostracion():
    bd = ConexionBD(":memory:")
    try:
        titulo("1. Conexión a la base de datos")
        print(f"Conexión exitosa a la base de datos (SQLite {bd.probar_conexion()}).")
        bd.inicializar_bd()
        repo_dep, repo_emp = DepartamentoRepositorio(bd), EmpleadoRepositorio(bd)

        titulo("2. CRUD de Departamento y Empleado")
        repo_dep.guardar(Departamento(1, "Sustentabilidad Industrial"))
        repo_dep.guardar(Departamento(2, "Recursos Humanos"))
        marcela = Empleado(1, "Marcela Iturra", "Av. Uno 123", "+56911111111",
                           "marcela@ecotech.cl", 1_500_000, date(2024, 4, 1))
        marcela.cambiarDepartamento(repo_dep.obtener_por_codigo(1))
        repo_emp.guardar(marcela)                                                    # Create
        repo_emp.guardar(Empleado(2, "Luis Pérez", "", "", "luis@ecotech.cl", 1_200_000, date(2023, 8, 15)))
        print("Listado:", *repo_emp.listar_activos(), sep="\n  ")                    # Read (lista)
        print("Búsqueda por id 1:", repo_emp.obtener_por_id(1))                      # Read (uno)
        marcela.sueldoBase = 1_650_000
        repo_emp.actualizar(marcela)                                                 # Update
        print("Sueldo actualizado:", repo_emp.obtener_por_id(1).sueldoBase)
        repo_emp.eliminar(2)                                                         # Delete (lógico)
        print("Activos tras eliminar el id 2:", [e.nombreCompleto for e in repo_emp.listar_activos()])
        repo_dep.eliminar(2)                                                         # Delete (físico)
        print("Departamentos:", [d.nombreDepto for d in repo_dep.listar()])

        titulo("3. Validaciones y manejo de errores (el programa no se interrumpe)")
        pruebas = [
            ("Sueldo negativo", lambda: Empleado(9, "Ana", "", "", "ana@ecotech.cl", -5, date(2024, 1, 1))),
            ("Correo inválido", lambda: Empleado(9, "Ana", "", "", "sin-arroba", 1000, date(2024, 1, 1))),
            ("Id repetido", lambda: repo_emp.guardar(Empleado(1, "Otro", "", "", "otro@ecotech.cl", 1000, date(2024, 1, 1)))),
            ("Empleado inexistente", lambda: repo_emp.obtener_por_id(999)),
        ]
        for nombre, accion in pruebas:
            try:
                accion()
            except EcoTechError as error:
                print(f"  {nombre}: {type(error).__name__} -> {error}")

        titulo("4. Prueba de inyección SQL con ' OR '1'='1")
        payload = "' OR '1'='1"
        resultado = repo_emp.buscar_por_nombre(payload)
        print(f"buscar_por_nombre({payload!r}) devolvió {len(resultado)} resultado(s): la consulta parametrizada "
              "trató el payload como un texto cualquiera.")
        print("Búsqueda legítima 'Marcela Iturra':", len(repo_emp.buscar_por_nombre("Marcela Iturra")), "resultado(s)")

        titulo("5. Transacción atómica (empleado + credencial)")
        ok = Empleado(10, "Jesús Capetillo", "", "", "jesus@ecotech.cl", 1_100_000, date(2025, 2, 1))
        repo_emp.registrar_con_credencial(ok, Credencial(ok, "jcapetillo", "Clave#2026", Perfil("Analista")))
        print("Caso éxito: empleado 10 guardado ->", repo_emp.obtener_por_id(10).nombreCompleto)
        malo = Empleado(11, "Roberto Gajardo", "", "", "roberto@ecotech.cl", 1_100_000, date(2025, 3, 1))
        try:
            repo_emp.registrar_con_credencial(malo, Credencial(malo, "jcapetillo", "Clave#2026", Perfil("Analista")))
        except RegistroDuplicadoError as error:
            print(f"Caso fallo: la 2ª escritura falló ({error})")
        try:
            repo_emp.obtener_por_id(11)
        except EcoTechError:
            print("Rollback comprobado: el empleado 11 NO quedó guardado (la BD sigue consistente).")

        titulo("6. Autenticación con la credencial guardada (la clave se almacena como hash)")
        cred = repo_emp.obtener_credencial("jcapetillo")
        print("Hash guardado:", cred.claveCifrada[:30] + "...")
        print("Clave correcta:", cred.validarAcceso("Clave#2026"), "| incorrecta:", cred.validarAcceso("otra"))

        titulo("7. Polimorfismo: una colección mixta de reportes")
        proyecto = Proyecto(1, "Huerta Urbana Conectada", "Sensores de riego", date(2025, 2, 1))
        ParticipacionProyecto(marcela, proyecto)
        ParteDiario(1, marcela, proyecto, date(2025, 4, 14), 6.5, "Calibración de sensores")
        try:
            ParteDiario(2, marcela, proyecto, date(2025, 4, 15), 30)
        except DatoInvalidoError as error:
            print("Parte diario inválido rechazado:", error)
        for reporte in (ReportePDF("horas por proyecto"), ReporteExcel("horas por proyecto")):
            texto = reporte.construir([marcela.departamento], [proyecto])
            print(f"  {type(reporte).__name__}.exportar() -> {len(reporte.exportar(texto))} bytes")
    except EcoTechError as error:
        print(f"Error inesperado del sistema: {error}")
    finally:
        bd.cerrar()


# ---------- Menú interactivo ----------

def menu():
    bd = ConexionBD()
    try:
        bd.inicializar_bd()
        print(f"Conexión exitosa a la base de datos (SQLite {bd.probar_conexion()}) - {bd.ruta}")
    except EcoTechError as error:
        print(f"No se pudo iniciar el sistema: {error}")
        return
    repo_dep, repo_emp = DepartamentoRepositorio(bd), EmpleadoRepositorio(bd)
    opciones = {
        "1": ("Registrar empleado", lambda: registrar_empleado(repo_emp, repo_dep)),
        "2": ("Listar empleados", lambda: listar_empleados(repo_emp)),
        "3": ("Buscar empleado por id", lambda: buscar_empleado(repo_emp)),
        "4": ("Actualizar sueldo de un empleado", lambda: actualizar_empleado(repo_emp)),
        "5": ("Eliminar empleado", lambda: eliminar_empleado(repo_emp)),
        "6": ("Crear departamento", lambda: crear_departamento(repo_dep)),
        "7": ("Listar departamentos", lambda: listar_departamentos(repo_dep)),
        "8": ("Eliminar departamento", lambda: eliminar_departamento(repo_dep)),
        "9": ("Registrar empleado con credencial (transacción)", lambda: registrar_con_credencial(repo_emp)),
        "10": ("Ejecutar demostración automática", demostracion),
    }
    try:
        while True:
            print("\n=== EcoTech Solutions ===")
            for clave, (texto, _) in opciones.items():
                print(f"{clave:>2}. {texto}")
            print(" 0. Salir")
            eleccion = input("Opción: ").strip()
            if eleccion == "0":
                break
            if eleccion not in opciones:
                print("Opción no válida.")
                continue
            try:
                opciones[eleccion][1]()
            except EcoTechError as error:
                print(f"No se pudo completar la operación: {error}")
            except ValueError as error:
                print(f"Dato inválido: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nSesión finalizada.")
    finally:
        bd.cerrar()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demostracion()
    else:
        menu()

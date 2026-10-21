from dominio.validaciones import entero_positivo, texto_no_vacio


class Departamento:
    """Agrega 1..* Empleados (los empleados existen con independencia del departamento)."""

    def __init__(self, codigoDepto, nombreDepto):
        self.__codigoDepto = entero_positivo(codigoDepto, "El código del departamento")  # -codigoDepto
        self.__nombreDepto = texto_no_vacio(nombreDepto, "El nombre del departamento")   # +nombreDepto
        self.__empleados = []

    @property
    def codigoDepto(self):
        return self.__codigoDepto

    @property
    def nombreDepto(self):
        return self.__nombreDepto

    @nombreDepto.setter
    def nombreDepto(self, valor):
        self.__nombreDepto = texto_no_vacio(valor, "El nombre del departamento")

    def incorporarEmpleado(self, e):
        return e.cambiarDepartamento(self)

    def retirarEmpleado(self, e):
        if e in self.__empleados:
            return e.cambiarDepartamento(None)
        return False

    def nomina(self):
        return list(self.__empleados)

    # Uso interno: los invoca Empleado.cambiarDepartamento
    def _agregar(self, e):
        if e not in self.__empleados:
            self.__empleados.append(e)

    def _quitar(self, e):
        if e in self.__empleados:
            self.__empleados.remove(e)

    def __str__(self):
        return f"Departamento [{self.__codigoDepto}] {self.__nombreDepto} ({len(self.__empleados)} empleados)"

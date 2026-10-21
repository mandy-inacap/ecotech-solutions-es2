"""Validaciones compartidas por todas las clases del dominio."""
from datetime import date

from dominio.excepciones import DatoInvalidoError


def texto_no_vacio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"{campo} no puede estar vacío.")
    return valor.strip()


def entero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise DatoInvalidoError(f"{campo} debe ser un número entero mayor a 0.")
    return valor


def numero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
        raise DatoInvalidoError(f"{campo} debe ser un número mayor a 0.")
    return float(valor)


def correo_valido(valor):
    valor = texto_no_vacio(valor, "El correo")
    usuario, _, dominio = valor.partition("@")
    if not usuario or "." not in dominio:
        raise DatoInvalidoError("El correo no tiene un formato válido (ej: nombre@dominio.cl).")
    return valor


def fecha_valida(valor, campo):
    if not isinstance(valor, date):
        raise DatoInvalidoError(f"{campo} debe ser una fecha.")
    return valor

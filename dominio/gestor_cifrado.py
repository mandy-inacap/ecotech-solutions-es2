import hashlib
import hmac
import os


class GestorCifrado:
    """Toda la lógica de cifrado queda aquí (hash con sal, PBKDF2) usando la librería estándar hashlib."""

    ITERACIONES = 100_000

    @staticmethod
    def encriptar(valor):
        sal = os.urandom(16)
        h = hashlib.pbkdf2_hmac("sha256", valor.encode(), sal, GestorCifrado.ITERACIONES)
        return sal.hex() + ":" + h.hex()

    @staticmethod
    def validar(valor, hash_guardado):
        try:
            sal_hex, h_hex = hash_guardado.split(":")
            h = hashlib.pbkdf2_hmac("sha256", valor.encode(), bytes.fromhex(sal_hex), GestorCifrado.ITERACIONES)
        except ValueError:
            return False   # hash guardado con formato inválido
        return hmac.compare_digest(h.hex(), h_hex)

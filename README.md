# EcoTech Solutions - Sistema de gestión de empleados (ES2 TI3021)

Aplicación de consola en Python (POO) con persistencia en SQLite. Implementa el diagrama UML final de la Unidad 1.

## Estructura
- `dominio/`: clases del modelo (sin SQL) y excepciones propias.
- `repositorio/`: conexión y acceso a datos (todo el SQL, siempre parametrizado).
- `datos/schema.sql`: tablas con llaves primarias y foráneas.
- `main.py`: menú por consola y demostración automática.

## Ejecución
1. `python -m venv venv` y activarlo (`venv\Scripts\activate` en Windows).
2. `pip install -r requirements.txt` (no hay dependencias externas).
3. Copiar `.env.example` a `.env` (opcional; por defecto usa `ecotech.db`).
4. `python main.py` para el menú, o `python main.py --demo` para la demostración automática.

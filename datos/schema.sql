-- Esquema relacional de EcoTech Solutions (SQLite)
-- La integridad referencial se activa en cada conexión con PRAGMA foreign_keys = ON

CREATE TABLE IF NOT EXISTS departamento (
    codigo_depto INTEGER PRIMARY KEY,
    nombre_depto TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS empleado (
    id_persona     INTEGER PRIMARY KEY,
    nombre_completo TEXT NOT NULL,
    direccion      TEXT,
    telefono       TEXT,
    correo         TEXT NOT NULL UNIQUE,
    sueldo_base    REAL NOT NULL CHECK (sueldo_base > 0),
    fecha_ingreso  TEXT NOT NULL,
    codigo_depto   INTEGER,
    activo         INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    FOREIGN KEY (codigo_depto) REFERENCES departamento (codigo_depto) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS credencial (
    nombre_usuario TEXT PRIMARY KEY,
    clave_cifrada  TEXT NOT NULL,
    habilitada     INTEGER NOT NULL DEFAULT 1 CHECK (habilitada IN (0, 1)),
    perfil         TEXT NOT NULL,
    id_persona     INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_persona) REFERENCES empleado (id_persona) ON DELETE CASCADE
);

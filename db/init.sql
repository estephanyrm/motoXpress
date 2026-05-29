CREATE TABLE IF NOT EXISTS Empleado (
    id_empleado SERIAL PRIMARY KEY,
    nombre VARCHAR(48) NOT NULL,
    apellido VARCHAR(48) NOT NULL,
    rol VARCHAR(16) NOT NULL,
    email VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(48) NOT NULL,
    apellido VARCHAR(48) NOT NULL,
    cedula VARCHAR(10) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    email VARCHAR(256) NOT NULL,
    fecha_registro DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Venta (
    id_venta SERIAL,
    fecha_venta DATE NOT NULL DEFAULT CURRENT_DATE,
    precio_final NUMERIC(12,2) NOT NULL,
    tipo_pago VARCHAR(24) NOT NULL,
    id_moto VARCHAR(32) NOT NULL,
    id_cliente INTEGER NOT NULL REFERENCES Cliente (id_cliente)  
        ON DELETE RESTRICT,
    id_empleado INTEGER NOT NULL REFERENCES Empleado (id_empleado) 
        ON DELETE RESTRICT,
    PRIMARY KEY (id_venta, fecha_venta)
) PARTITION BY RANGE (fecha_venta);

CREATE TABLE venta_2024 PARTITION OF Venta FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE venta_2025 PARTITION OF Venta FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE venta_2026 PARTITION OF Venta FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
CREATE TABLE venta_default PARTITION OF Venta DEFAULT;

CREATE TABLE IF NOT EXISTS Financiacion (
    id_financiacion SERIAL PRIMARY KEY,
    cuotas INTEGER,
    interes NUMERIC(5,2) NOT NULL,
    monto_cuota NUMERIC(12,2) NOT NULL,
    id_venta INTEGER NOT NULL,
    fecha_venta DATE NOT NULL,

    FOREIGN KEY (id_venta, fecha_venta)
        REFERENCES Venta (id_venta, fecha_venta)
            ON DELETE CASCADE
);
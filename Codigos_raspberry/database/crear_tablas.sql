CREATE TABLE Usuario (
    usuario_id CHAR(36) PRIMARY KEY,
    usuario_nombre VARCHAR(80) NOT NULL,
    usuario_email VARCHAR(120) NOT NULL,
    usuario_telefono VARCHAR(20),
    usuario_activo BOOLEAN
);

CREATE TABLE Raspberry_PI (
    raspberry_id CHAR(36) PRIMARY KEY,
    usuario_id CHAR(36) NOT NULL,
    raspberry_estado_arduino VARCHAR(20),
    raspberry_estado_pagina_web VARCHAR(20),
    raspberry_nivel_bateria DECIMAL(5,2),

    FOREIGN KEY (usuario_id)
    REFERENCES Usuario(usuario_id)
);

CREATE TABLE Contacto_Emergencia (
    contacto_id CHAR(36) PRIMARY KEY,
    usuario_id CHAR(36) NOT NULL,
    contacto_nombre VARCHAR(80) NOT NULL,
    contacto_apellido VARCHAR(80),
    contacto_telefono VARCHAR(20),
    contacto_creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contacto_estado BOOLEAN,

    FOREIGN KEY (usuario_id)
    REFERENCES Usuario(usuario_id)
);

CREATE TABLE Arduino (
    arduino_id CHAR(36) PRIMARY KEY,
    raspberry_id CHAR(36) NOT NULL,
    arduino_estado VARCHAR(20),

    FOREIGN KEY (raspberry_id)
    REFERENCES Raspberry_PI(raspberry_id)
);

CREATE TABLE Perfil_Wifi (
    perfil_id CHAR(36) PRIMARY KEY,
    raspberry_id CHAR(36) NOT NULL,
    perfil_ssid VARCHAR(100) NOT NULL,
    perfil_contrasena VARCHAR(255) NOT NULL,
    perfil_seguridad VARCHAR(50),

    FOREIGN KEY (raspberry_id)
    REFERENCES Raspberry_PI(raspberry_id)
);

CREATE TABLE Evento_Caida (
    evento_id CHAR(36) PRIMARY KEY,
    raspberry_id CHAR(36) NOT NULL,
    evento_detectado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evento_confirmado BOOLEAN,

    FOREIGN KEY (raspberry_id)
    REFERENCES Raspberry_PI(raspberry_id)
);

CREATE TABLE Evento_Raspberry (
    evento_raspberry_id CHAR(36) PRIMARY KEY,
    raspberry_id CHAR(36) NOT NULL,
    evento_tipo VARCHAR(50),
    evento_detectado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raspberry_id)
    REFERENCES Raspberry_PI(raspberry_id)
);

CREATE TABLE Notificacion (
    notificacion_id CHAR(36) PRIMARY KEY,
    contacto_id CHAR(36) NOT NULL,
    evento_id CHAR(36),
    evento_raspberry_id CHAR(36),

    notificacion_canal VARCHAR(30),
    notificacion_estado VARCHAR(30),
    notificacion_enviada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notificacion_entregada_en TIMESTAMP NULL,

    FOREIGN KEY (contacto_id)
    REFERENCES Contacto_Emergencia(contacto_id),

    FOREIGN KEY (evento_id)
    REFERENCES Evento_Caida(evento_id),

    FOREIGN KEY (evento_raspberry_id)
    REFERENCES Evento_Raspberry(evento_raspberry_id)
);
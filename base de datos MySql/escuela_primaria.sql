-- =============================================
-- BASE DE DATOS: ESCUELA_PRIMARIA 
-- =============================================

DROP DATABASE IF EXISTS Escuela_Primaria;

CREATE DATABASE Escuela_Primaria;

USE Escuela_Primaria;

-- 1. Tabla CURSO
CREATE TABLE Curso (
    ID_Curso INT PRIMARY KEY,
    Nivel VARCHAR(10) NOT NULL,
    Letra CHAR(1) NOT NULL,
    CONSTRAINT UK_Curso_Nivel_Letra UNIQUE (Nivel, Letra),
    CONSTRAINT CK_Nivel_Valido CHECK (Nivel IN ('1ro', '2do', '3ro', '4to', '5to', '6to')),
    CONSTRAINT CK_Letra_Valida CHECK (Letra IN ('A', 'B', 'C', 'D'))
);

-- 2. Tabla ESTUDIANTE
CREATE TABLE Estudiante (
    CI_Estudiante VARCHAR(15) PRIMARY KEY,
    Nombre_Completo VARCHAR(100) NOT NULL,
    Fecha_Nacimiento DATE NOT NULL,
    Direccion VARCHAR(150),
    Telefono VARCHAR(20),
    Celular VARCHAR(20),
    ID_Curso INT NOT NULL,
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
);

-- 3. Tabla PROFESOR
CREATE TABLE Profesor (
    CI_Profesor VARCHAR(15) PRIMARY KEY,
    Nombre_Completo VARCHAR(100) NOT NULL,
    Telefono VARCHAR(20),
    Celular VARCHAR(20),
    Especialidad VARCHAR(50),
    Fecha_Contratacion DATE NOT NULL
);

-- 4. Tabla MATERIA
CREATE TABLE Materia (
    ID_Materia INT PRIMARY KEY,
    Nombre_Materia VARCHAR(50) NOT NULL,
    Carga_Horaria INT NOT NULL,
    CONSTRAINT CK_Carga_Horaria CHECK (Carga_Horaria > 0 AND Carga_Horaria <= 10)
);

-- 5. Tabla ASIGNACION
CREATE TABLE Asignacion (
    ID_Asignacion INT PRIMARY KEY,
    CI_Profesor VARCHAR(15) NOT NULL,
    ID_Materia INT NOT NULL,
    ID_Curso INT NOT NULL,
    Gestion INT NOT NULL,
    CONSTRAINT UK_Asignacion_Unica UNIQUE (CI_Profesor, ID_Materia, ID_Curso, Gestion),
    FOREIGN KEY (CI_Profesor) REFERENCES Profesor(CI_Profesor),
    FOREIGN KEY (ID_Materia) REFERENCES Materia(ID_Materia),
    FOREIGN KEY (ID_Curso) REFERENCES Curso(ID_Curso)
);

-- 6. Tabla HORARIO
CREATE TABLE Horario (
    ID_Horario INT PRIMARY KEY,
    ID_Asignacion INT NOT NULL,
    Dia_Semana VARCHAR(10) NOT NULL,
    Hora_Inicio TIME NOT NULL,
    Hora_Fin TIME NOT NULL,
    Aula VARCHAR(20) NOT NULL,
    FOREIGN KEY (ID_Asignacion) REFERENCES Asignacion(ID_Asignacion),
    CONSTRAINT CK_Dia_Valido CHECK (Dia_Semana IN ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'))
);

-- 7. Tabla ASISTENCIA
CREATE TABLE Asistencia (
    ID_Asistencia INT PRIMARY KEY,
    CI_Estudiante VARCHAR(15) NOT NULL,
    Fecha DATE NOT NULL,
    Presente BOOLEAN NOT NULL,
    Comentario TEXT,
    FOREIGN KEY (CI_Estudiante) REFERENCES Estudiante(CI_Estudiante)
);

-- 8. Tabla NOTA
CREATE TABLE Nota (
    ID_Nota INT PRIMARY KEY,
    CI_Estudiante VARCHAR(15) NOT NULL,
    ID_Materia INT NOT NULL,
    Periodo VARCHAR(20) NOT NULL,
    Nota_Valor DECIMAL(5,2) NOT NULL,
    Comentario TEXT,
    FOREIGN KEY (CI_Estudiante) REFERENCES Estudiante(CI_Estudiante),
    FOREIGN KEY (ID_Materia) REFERENCES Materia(ID_Materia),
    CONSTRAINT CK_Nota_Rango CHECK (Nota_Valor >= 0 AND Nota_Valor <= 100)
);

-- =============================================
-- DATOS DE EJEMPLO
-- =============================================

-- =============================================
--       POBLADO DE DATOS : CURSO
-- =============================================
INSERT INTO Curso VALUES 
(1, '1ro', 'A'),
(2, '1ro', 'B'),
(3, '2do', 'A'),
(4, '2do', 'B'),
(5, '2do', 'C'),
(6, '3ro', 'A'),
(7, '3ro', 'B'),
(8, '4to', 'A'),
(9, '4to', 'B'),
(10, '5to', 'A'),
(11, '5to', 'B'),
(12, '6to', 'A');

-- =============================================
--       POBLADO DE DATOS : ESTUDIANTE 
-- =============================================
INSERT INTO Estudiante (CI_Estudiante, Nombre_Completo, Fecha_Nacimiento, Direccion, Telefono, Celular, ID_Curso) VALUES
('1234567', 'María García', '2016-05-15', 'Calle 123, La Paz', NULL, '78912345', 1),
('17654321', 'Tomás López', '2016-11-22', 'Avenida 456, Cochabamba', '4-654321', '79845612', 2),
('16566543', 'Sofía Martínez', '2015-08-30', 'Plaza Central, Santa Cruz', NULL, '71234567', 3),
('17112223', 'Mateo Rodríguez', '2015-03-15', 'Calle Los Pinos 45, La Paz', '2-789012', '77123456', 4),
('14445556', 'Valentina Mendoza', '2014-07-20', 'Avenida Busch 789, La Paz', NULL, '78234567', 5),
('13998887', 'Lucas Fernández', '2014-10-10', 'Calle 6 de Agosto 123, La Paz', '2-901234', '79345678', 6),
('13334445', 'Emma Gutiérrez', '2013-04-25', 'Calle Pedro Salazar 78, La Paz', '2-123789', '71567890', 7),
('16667778', 'Nicolás Vargas', '2013-09-12', 'Avenida América 234, La Paz', NULL, '72678901', 8),
('11889990', 'Camila Torres', '2013-03-22', 'Avenida San Martín 123, Cochabamba', '4-234567', '76012345', 9),
('11213334', 'Isabella Flores', '2012-12-01', 'Calle Beni 567, Santa Cruz', NULL, '73789012', 10),
('15556667', 'Benjamín Castro', '2012-06-18', 'Avenida Cristóbal de Mendoza 456, Santa Cruz', NULL, '74890123', 11),
('16778889', 'Alejandro Ríos', '2011-08-05', 'Calle 21 de Mayo 890, Santa Cruz', '3-901567', '75901234', 12);

-- =============================================
--       POBLADO DE DATOS : PROFESORES
-- =============================================
INSERT INTO Profesor VALUES 
('10041001', 'Lic. Ana María Quispe Mamani', '2-111222', '70111111', 'Lenguaje', '2020-02-15'),
('11061002', 'Lic. Juan Carlos Torrez Villca', '2-222333', '70222222', 'Matemáticas', '2020-02-15'),
('10161003', 'Lic. María Elena Condori Apaza', '2-333444', '70333333', 'Ciencias Naturales', '2020-02-16'),
('10102001', 'Lic. Carmen Rosa Gutiérrez Flores', '2-777888', '70777777', 'Lenguaje', '2020-02-20'),
('9602002', 'Lic. Luis Alberto Mamani Ticona', '2-888999', '70888888', 'Matemáticas', '2020-02-21'),
('7782003', 'Lic. Ruth Esther Choque Quispe', '2-999000', '70999999', 'Ciencias Naturales', '2020-02-22'),
('5501001', 'Lic. Elizabeth Mamani Apaza', '2-333555', '70333333', 'Lenguaje', '2020-03-01'),
('7451002', 'Lic. Roberto Carlos Fernández Ledezma', '2-444666', '70444444', 'Matemáticas', '2020-03-02'),
('8881003', 'Lic. Gladys Nancy Quispe Huanca', '2-555777', '70555555', 'Ciencias Naturales', '2020-03-03'),
('9861001', 'Lic. Zulema Fernández Quispe', '2-111888', '70616161', 'Lenguaje', '2022-03-01'),
('4561002', 'Lic. Nicolás Mamani Apaza', '2-222999', '70727272', 'Matemáticas', '2022-03-02'),
('11231003', 'Lic. Olga Quispe Fernández', '2-333000', '70838383', 'Ciencias Naturales', '2022-03-03'),
('6002001', 'Lic. Wendy Quispe Mamani', '2-777444', '70393939', 'Lenguaje', '2022-03-07'),
('4502002', 'Lic. Teófila Apaza Fernández', '2-888555', '70404040', 'Matemáticas', '2022-03-08'),
('7802003', 'Lic. Roger Mamani Quispe', '2-999666', '70515151', 'Ciencias Naturales', '2022-03-09'),
('11045569', 'Lic. Juan Pablo Mamani Fernández', '2-333111', '70959595', 'Técnica Tecnológica', '2020-08-10'),
('8777877', 'Tec. María Isabel Quispe Mamani', '2-444222', '70606060', 'Técnica Tecnológica', '2020-08-11'),
('6555874', 'Lic. José Luis Arancibia Ríos', '2-444555', '70444444', 'Valores Espiritualidad y Religiones', '2020-02-17'),
('5666897', 'Lic. Patricia Fernández López', '2-555666', '70555555', 'Música', '2020-02-18'),
('1001006', 'Lic. Rolando Paredes Mamani', '2-666777', '70666666', 'Educación Física', '2020-02-19'),
('4788856', 'Lic. Gregorio Fernández Mamani', '2-444111', '70949494', 'Valores Espiritualidad y Religiones', '2022-03-04'),
('4556879', 'Lic. Raquel Apaza Quispe', '2-555222', '70171717', 'Música', '2022-03-05'),
('6668987', 'Lic. Leonardo Mamani Fernández', '2-666333', '70282828', 'Educación Física', '2022-03-06'),
('10025697', 'Lic. David Fernando Lima Vargas', '2-000111', '70101010', 'Valores Espiritualidad y Religiones', '2020-02-23'),
('1789566', 'Lic. Silvia Beatriz Rojas López', '2-111333', '70111111', 'Música', '2020-02-24'),
('10066998', 'Lic. Fernando René Flores Copa', '2-222444', '70222222', 'Educación Física', '2020-02-25'),
('9998989', 'Lic. Víctor Hugo Mamani Ticona', '2-555444', '70858585', 'Computación', '2020-09-01'),
('8999878', 'Ing. Patricia Fernández López', '2-666555', '70969696', 'Computación', '2020-09-02');

-- =============================================
--       POBLADO DE DATOS : MATERIA
-- =============================================
INSERT INTO Materia VALUES 
(101, 'Matemáticas', 5),
(102, 'Lenguaje', 5),
(103, 'Ciencias Naturales', 5),
(104, 'Valores Espiritualidad y Religiones', 2),
(105, 'Música', 2),
(106, 'Educación Física', 2),
(107, 'Técnica Tecnológica', 3),
(108, 'Computación', 4);

-- =============================================
--       POBLADO DE DATOS : ASIGNACION (GESTIÓN 2026)
-- =============================================
INSERT INTO Asignacion VALUES 
(1, '10041001', 102, 1, 2026),
(4, '10102001', 102, 2, 2026),
(6, '7782003', 103, 2, 2026),
(7, '5501001', 102, 3, 2026),
(9, '8881003', 103, 3, 2026),
(10, '9861001', 102, 4, 2026),
(13, '6002001', 102, 5, 2026),
(14, '4502002', 101, 5, 2026),
(17, '11061002', 101, 6, 2026),
(18, '10161003', 103, 6, 2026),
(19, '10102001', 102, 7, 2026),
(21, '7782003', 103, 7, 2026),
(22, '5501001', 102, 8, 2026),
(25, '9861001', 102, 9, 2026),
(27, '11231003', 103, 9, 2026),
(30, '7802003', 103, 10, 2026),
(31, '10041001', 102, 11, 2026),
(33, '10161003', 103, 11, 2026),
(34, '10102001', 102, 12, 2026),
(35, '9602002', 101, 12, 2026),
(36, '7782003', 103, 12, 2026),
(37, '6555874', 104, 1, 2026),
(38, '6555874', 104, 2, 2026),
(46, '10025697', 104, 10, 2026),
(48, '10025697', 104, 12, 2026),
(49, '5666897', 105, 1, 2026),
(50, '5666897', 105, 2, 2026),
(61, '1001006', 106, 1, 2026),
(68, '6668987', 106, 8, 2026),
(79, '11045569', 107, 7, 2026),
(80, '8777877', 107, 8, 2026),
(82, '8777877', 107, 10, 2026),
(84, '8777877', 107, 12, 2026),
(85, '9998989', 108, 1, 2026),
(86, '9998989', 108, 2, 2026),
(95, '8999878', 108, 11, 2026),
(96, '8999878', 108, 12, 2026);

-- =============================================
--       POBLADO DE DATOS : HORARIO
-- =============================================
INSERT INTO Horario (ID_Horario, ID_Asignacion, Dia_Semana, Hora_Inicio, Hora_Fin, Aula) VALUES
(1, 1, 'Lunes', '08:00:00', '09:30:00', '101'),
(2, 1, 'Miércoles', '08:00:00', '09:30:00', '101'),
(3, 37, 'Viernes', '10:00:00', '11:00:00', '101'),
(4, 49, 'Martes', '11:00:00', '12:00:00', '103'),
(6, 85, 'Miércoles', '14:30:00', '16:00:00', 'Lab_Computacion'),
(7, 4, 'Lunes', '09:30:00', '11:00:00', '102'),
(8, 4, 'Jueves', '09:30:00', '11:00:00', '102'),
(9, 6, 'Martes', '08:00:00', '09:30:00', '102'),
(10, 38, 'Viernes', '11:00:00', '12:00:00', '102'),
(11, 50, 'Miércoles', '13:00:00', '14:00:00', '103'),
(12, 86, 'Viernes', '14:00:00', '15:30:00', 'Lab_Computacion'),
(13, 7, 'Martes', '08:00:00', '09:30:00', '201'),
(14, 7, 'Jueves', '08:00:00', '09:30:00', '201'),
(15, 9, 'Miércoles', '09:30:00', '11:00:00', '201'),
(16, 10, 'Lunes', '10:00:00', '11:30:00', '202'),
(17, 10, 'Viernes', '10:00:00', '11:30:00', '202'),
(18, 13, 'Martes', '10:30:00', '12:00:00', '203'),
(19, 13, 'Jueves', '10:30:00', '12:00:00', '203'),
(20, 14, 'Miércoles', '08:00:00', '09:30:00', '203'),
(21, 14, 'Viernes', '08:00:00', '09:30:00', '203'),
(22, 17, 'Lunes', '13:00:00', '14:30:00', '301'),
(23, 17, 'Miércoles', '13:00:00', '14:30:00', '301'),
(24, 18, 'Martes', '14:30:00', '16:00:00', '301'),
(25, 19, 'Lunes', '08:00:00', '09:30:00', '302'),
(26, 19, 'Miércoles', '08:00:00', '09:30:00', '302'),
(27, 21, 'Viernes', '09:30:00', '11:00:00', '302'),
(28, 79, 'Jueves', '13:00:00', '14:30:00', 'Taller'),
(29, 22, 'Martes', '08:00:00', '09:30:00', '401'),
(30, 22, 'Jueves', '08:00:00', '09:30:00', '401'),
(31, 68, 'Miércoles', '14:30:00', '16:00:00', 'Cancha'),
(32, 80, 'Viernes', '13:00:00', '14:30:00', 'Taller'),
(33, 25, 'Lunes', '14:00:00', '15:30:00', '402'),
(34, 25, 'Miércoles', '14:00:00', '15:30:00', '402'),
(35, 27, 'Martes', '09:30:00', '11:00:00', '402'),
(36, 30, 'Lunes', '08:00:00', '09:30:00', '501'),
(37, 30, 'Jueves', '08:00:00', '09:30:00', '501'),
(38, 46, 'Viernes', '10:00:00', '11:00:00', '501'),
(39, 82, 'Miércoles', '15:00:00', '16:30:00', 'Taller'),
(40, 31, 'Martes', '10:00:00', '11:30:00', '502'),
(41, 31, 'Viernes', '10:00:00', '11:30:00', '502'),
(42, 33, 'Miércoles', '08:00:00', '09:30:00', '502'),
(43, 95, 'Jueves', '14:00:00', '15:30:00', 'Lab_Computacion'),
(44, 34, 'Lunes', '08:00:00', '09:30:00', '601'),
(45, 34, 'Miércoles', '08:00:00', '09:30:00', '601'),
(46, 35, 'Martes', '08:00:00', '09:30:00', '601'),
(47, 35, 'Jueves', '08:00:00', '09:30:00', '601'),
(48, 36, 'Viernes', '08:00:00', '09:30:00', '601'),
(49, 48, 'Viernes', '11:00:00', '12:00:00', '601'),
(50, 84, 'Miércoles', '14:30:00', '16:00:00', 'Taller'),
(51, 96, 'Martes', '14:30:00', '16:00:00', 'Lab_Computacion');

-- =============================================
--       POBLADO DE DATOS : ASISTENCIA (AÑO 2026)
-- =============================================
INSERT INTO Asistencia (ID_Asistencia, CI_Estudiante, Fecha, Presente, Comentario) VALUES
(501, '1234567', '2026-03-04', TRUE, NULL),
(502, '1234567', '2026-03-11', FALSE, 'Permiso médico'),
(504, '16566543', '2026-03-06', FALSE, 'Llegó tarde 15 min'),
(505, '17112223', '2026-03-07', TRUE, NULL),
(506, '14445556', '2026-03-12', TRUE, 'Participó en clase'),
(507, '13998887', '2026-03-13', FALSE, 'No presentó justificación'),
(508, '13334445', '2026-03-14', TRUE, NULL),
(509, '11889990', '2026-03-18', TRUE, 'Tarea entregada'),
(510, '11213334', '2026-03-19', FALSE, 'Enfermedad'),
(511, '15556667', '2026-03-20', TRUE, NULL),
(512, '16778889', '2026-03-21', TRUE, 'Excelente comportamiento');

-- =============================================
--       POBLADO DE DATOS : NOTAS (AÑO 2026)
-- =============================================
INSERT INTO Nota (ID_Nota, CI_Estudiante, ID_Materia, Periodo, Nota_Valor, Comentario) VALUES 
(601, '1234567', 101, 'Trimestre 1', 85.0, 'Buen trabajo'),
(602, '1234567', 102, 'Trimestre 1', 90.0, 'Excelente'),
(603, '17654321', 101, 'Trimestre 1', 67.5, 'Necesita mejorar'),
(604, '16566543', 103, 'Trimestre 1', 75.0, NULL),
(605, '17112223', 101, 'Trimestre 1', 82.5, 'Buen desempeño'),
(606, '14445556', 102, 'Trimestre 2', 87.5, 'Buena redacción'),
(607, '16667778', 103, 'Trimestre 2', 60.0, 'Debe esforzarse más'),
(608, '15556667', 108, 'Trimestre 2', 92.5, 'Excelente proyecto'),
(609, '13334445', 101, 'Trimestre 2', 80.0, 'Progresando'),
(610, '11889990', 102, 'Trimestre 2', 72.5, 'Regular'),
(611, '13998887', 105, 'Trimestre 2', 85.0, 'Participó en festival'),
(612, '11213334', 103, 'Trimestre 3', 97.5, '¡Sobresaliente!'),
(613, '16778889', 108, 'Trimestre 3', 85.0, 'Muy bien'),
(614, '13998887', 101, 'Trimestre 3', 82.5, 'Constante'),
(615, '14445556', 105, 'Trimestre 3', 90.0, 'Talento musical'),
(616, '1234567', 103, 'Trimestre 3', 95.0, 'Mejoró mucho'),
(617, '17654321', 102, 'Trimestre 3', 70.0, 'Necesita practicar'),
(618, '16566543', 101, 'Trimestre 3', 87.5, 'Recuperó');
INSERT INTO CLIENTE
VALUES ('42281439A', 'SOFIA', 'HERNANDEZ GARCIA', 'SOFIA@GMAIL.COM', 628353515);

INSERT INTO CLIENTE
VALUES ('31311746Y', 'CAMILA', 'LOPEZ MARTINEZ', 'CAMILA@GMAIL.COM', 662195188);

INSERT INTO CLIENTE
VALUES ('62035321C', 'XIMENA', 'PEREZ SANCHEZ', 'XIMENA@GMAIL.COM', 617413349);

INSERT INTO CLIENTE
VALUES ('38184036B', 'MATEO', 'MARTIN GOMEZ', 'MATEO@GMAIL.COM', 668948356);

INSERT INTO CLIENTE
VALUES ('48184784Z', 'MATIAS', 'HERNANDEZ GONZALEZ', 'MATIAS@GMAIL.COM', 620520465);

INSERT INTO EMPLEADO
VALUES ('58607694Z', 'ANGELINA', 'MURILLO ALCARAZ', 'ANGELINA@GMAIL.COM', 659407146, 1400, 'MONITOR');

INSERT INTO EMPLEADO
VALUES ('45024479R', 'REBECCA', 'ALVAREZ HOFFMAN', 'REBECCA@GMAIL.COM', 743784284, 1400, 'MONITOR');

INSERT INTO EMPLEADO
VALUES ('82350448Y', 'CESAR', 'TERRON DELGADO', 'CESAR@GMAIL.COM', 653842546, 1400, 'MONITOR');

INSERT INTO EMPLEADO
VALUES ('17236175K', 'ERIC', 'LEVINE HILL', 'ERIC@GMAIL.COM', 686822419, 1400, 'MONITOR');

INSERT INTO EMPLEADO
VALUES ('32354227N', 'ANDREW', 'JORDAN GUTIERREZ', 'ANDREW@GMAIL.COM', 739336821, 1400, 'MONITOR');

INSERT INTO EMPLEADO
VALUES ('47513180X', 'EUGENIA', 'MARINEZ AZNAR', 'EUGENIA@GMAIL.COM', 697302992, 1150, 'RECEPCIONISTA');

INSERT INTO EMPLEADO
VALUES ('12085601K', 'MAURICIO', 'MOYA ESPINOSA', 'MAURICIO@GMAIL.COM', 661770391, 1150, 'RECEPCIONISTA');

INSERT INTO EMPLEADO
VALUES ('31762943N', 'VALERIA', 'PASCUAL CABELLO', 'VALERIA@GMAIL.COM', 632399828, 1000, 'LIMPIADOR');

INSERT INTO EMPLEADO
VALUES ('95705773J', 'AMANCIO', 'VAZQUEZ ARMAS', 'AMANCIO@GMAIL.COM', 626897608, 1000, 'LIMPIADOR');

INSERT INTO ENCARGADOS
VALUES ('33920287W', '31762943N', 'MAYUR UMMAHANI', 'TURK ASLAN', 'MAYUR@GMAIL.COM', 616493628, 1600);

INSERT INTO SALA
VALUES (1, 70, 112);

INSERT INTO SALA
VALUES (2, 40, 64);

INSERT INTO SALA
VALUES (3, 50, 80);

INSERT INTO ACTIVIDAD
VALUES (1, 'YOGA', 25, 1);

INSERT INTO ACTIVIDAD
VALUES (2, 'BOXEO', 12, 2);

INSERT INTO ACTIVIDAD
VALUES (3, 'ZUMBA', 25, 1);

INSERT INTO ACTIVIDAD
VALUES (4, 'PILATES', 30, 1);

INSERT INTO ACTIVIDAD
VALUES (5, 'KARATE', 15, 2);

INSERT INTO HORARIO
VALUES (1, 'M', '09:00:00', '10:30:00');

INSERT INTO HORARIO
VALUES (1, 'J', '09:00:00', '10:30:00');

INSERT INTO HORARIO
VALUES (2, 'L', '16:00:00', '18:00:00');

INSERT INTO HORARIO
VALUES (2, 'X', '17:00:00', '19:30:00');

INSERT INTO HORARIO
VALUES (2, 'V', '16:30:00', '18:00:00');

INSERT INTO HORARIO
VALUES (3, 'L', '10:00:00', '11:30:00');

INSERT INTO HORARIO
VALUES (3, 'X', '10:00:00', '11:30:00');

INSERT INTO HORARIO
VALUES (4, 'X', '15:00:00', '16:30:00');

INSERT INTO HORARIO
VALUES (4, 'V', '17:00:00', '18:00:00');

INSERT INTO HORARIO
VALUES (5, 'L', '09:30:00', '11:45:00');

INSERT INTO HORARIO
VALUES (5, 'J', '08:00:00', '10:00:00');

INSERT INTO HORARIO
VALUES (5, 'V', '08:30:00', '10:30:00');

INSERT INTO MATERIAL
VALUES (1, 1, 'ESTERILLA', 35);

INSERT INTO MATERIAL
VALUES (2, 2, 'GUANTES', 15);

INSERT INTO MATERIAL
VALUES (3, 2, 'CASCO', 15);

INSERT INTO MATERIAL
VALUES (4, 2, 'COMBA', 18);

INSERT INTO MATERIAL
VALUES (5, 1, 'PELOTA DE PILATES', 20);

INSERT INTO MATERIAL
VALUES (6, 1, 'LADRILLO', 25);

INSERT INTO MATERIAL
VALUES (7, 2, 'PETO', 18);

INSERT INTO MATERIAL
VALUES (8, 2, 'ESPINILLERAS', 15);

INSERT INTO PLAN
VALUES (1, 'BASICO YOGA', 25);

INSERT INTO PLAN
VALUES (2, 'BASICO BOXEO', 25);

INSERT INTO PLAN
VALUES (3, 'BASICO ZUMBA', 25);

INSERT INTO PLAN
VALUES (4, 'BASICO PILATES', 25);

INSERT INTO PLAN
VALUES (5, 'BASICO KARATE', 25);

INSERT INTO PLAN
VALUES (6, 'YOGA + PILATES', 40);

INSERT INTO PLAN_ACTIVIDAD
VALUES (1, 1);

INSERT INTO PLAN_ACTIVIDAD
VALUES (2, 2);

INSERT INTO PLAN_ACTIVIDAD
VALUES (3, 3);

INSERT INTO PLAN_ACTIVIDAD
VALUES (4, 4);

INSERT INTO PLAN_ACTIVIDAD
VALUES (5, 5);

INSERT INTO PLAN_ACTIVIDAD
VALUES (6, 1);

INSERT INTO PLAN_ACTIVIDAD
VALUES (6, 4);

INSERT INTO SUBSCRIPCION
VALUES (1, '42281439A');

INSERT INTO SUBSCRIPCION
VALUES (1, '31311746Y');

INSERT INTO SUBSCRIPCION
VALUES (2, '62035321C');

INSERT INTO SUBSCRIPCION
VALUES (3, '38184036B');

INSERT INTO SUBSCRIPCION
VALUES (6, '48184784Z');

INSERT INTO LIMPIADOR_SALA
VALUES ('31762943N', 1);

INSERT INTO LIMPIADOR_SALA
VALUES ('31762943N', 2);

INSERT INTO LIMPIADOR_SALA
VALUES ('95705773J', 1);

INSERT INTO MONITOR_ACTIVIDAD
VALUES ('58607694Z', 1);

INSERT INTO MONITOR_ACTIVIDAD
VALUES ('82350448Y', 2);

INSERT INTO MONITOR_ACTIVIDAD
VALUES ('17236175K', 3);

INSERT INTO MONITOR_ACTIVIDAD
VALUES ('45024479R', 4);

INSERT INTO MONITOR_ACTIVIDAD
VALUES ('32354227N', 5);

--  for create person table and fill 
CREATE TABLE personas VALUES [{"id_persona":"integer", "nombre":"varchar", "ocupacion":"varchar", "edad":"integer"}]
INSERT INTO personas VALUES (1,"Elias Valencia","Ingeniero",32)
INSERT INTO personas VALUES (2,"Omar Salas","Comerciante",47)
INSERT INTO personas VALUES (3,"Arturo Gallegos","Agronomo",52)
INSERT INTO personas VALUES (4,"Leticia Zegarra","Obrero",47)
INSERT INTO personas VALUES (5,"Elias Valencia","Policia",22)
INSERT INTO personas VALUES (6,"Omar Salas","Comerciante",17)

UPDATE personas SET ("nombre"="Antonio Vasquez") WHERE ("id_persona"="3")

SELECT * FROM personas WHERE ("nombre"="leticia zegarra")
SELECT * FROM personas WHERE ("nombre"="antonio") # this sentence doesnt show nothing

DELETE FROM personas WHERE ("nombre"="antonio vasquez")
DELETE FROM personas WHERE ("id_persona"="4")

# the insertion after delete starts from the end, 
# in the next version, we should order this *_QUEUE.csv in ascendent order
INSERT INTO personas VALUES (10,"Michelle Oviedo","Ingeniera",30)
INSERT INTO personas VALUES (11,"Barack Obama","Presidente",63)
INSERT INTO personas VALUES (12,"Donald Trump","Presidente",81)


# the above sql sentences work !!






# examples of table:

-- ID_PERSONA:INTEGER       ,NOMBRE:VARCHAR           ,OCUPACION:VARCHAR        ,EDAD:INTEGER             
-- 1                        ,ELIAS VALENCIA           ,INGENIERO                ,32                       
-- 2                        ,OMAR SALAS               ,COMERCIANTE              ,47                       
-- 3                        ,JOSE HEREDIA             ,AGRONOMO                 ,52                       
-- 11                       ,BARACK OBAMA             ,PRESIDENTE               ,63                       
-- 5                        ,ELIAS VALENCIA           ,POLICIA                  ,22                       
-- 6                        ,OMAR SALAS               ,COMERCIANTE              ,17                       
-- 7                        ,ELIAS VALENCIA           ,INGENIERO                ,32                       
-- 8                        ,OMAR SALAS               ,COMERCIANTE              ,47                       
-- 7                        ,ELIAS VALENCIA           ,INGENIERO                ,32                       
-- 8                        ,OMAR SALAS               ,COMERCIANTE              ,47                       
-- 10                       ,MICHELLE OVIEDO          ,INGENIERA                ,30                       
-- 8                        ,OMAR SALAS               ,COMERCIANTE              ,47                       
-- 12                       ,DONALD TRUMP             ,PRESIDENTE               ,81                       

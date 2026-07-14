SELECT 
    rev, OBSERVACION,
    COUNT(ID) AS cantidad
FROM [Maestro].[dbo].[toa_ahora_CV_estado]
WHERE 
    Fecha = '2026-07-13'
GROUP BY OBSERVACION, REV
ORDER BY cantidad DESC;


SELECT *
FROM [Maestro].[dbo].[toa_ahora_CV_estado]

SELECT Access_ID, Prioridad,
   COUNT(Access_ID) AS cantidad 
FROM [Maestro].[dbo].[toa_ahora_CV_estado]
WHERE 
    Fecha = '2026-07-13' 
    GROUP BY Access_ID, Prioridad
    
SELECT TOP 1 ID, Access_ID
            FROM Maestro.dbo.toa_ahora_CV_estado
            WHERE  
                (OBSERVACION IS NULL OR OBSERVACION = '')
                AND (REV IS NULL OR REV = '')
                AND Access_ID IS NOT NULL
                AND Fecha >= CAST(GETDATE() AS DATE)
                AND Fecha < DATEADD(DAY, 1, CAST(GETDATE() AS DATE))
            ORDER BY 
                Prioridad ASC,
                Inicio ASC,
                ID ASC 
SELECT
    @@SERVERNAME AS servidor,
    DB_NAME() AS base_actual,
    SUSER_NAME() AS usuario;
      



UPDATE [Maestro].[dbo].[toa_ahora_CV_estado]
SET 
    REV = NULL,
    OBSERVACION = NULL
WHERE REV = 'REVISANDO' and Fecha = '2026-07-13'


UPDATE [Maestro].[dbo].[toa_ahora_CV_estado]
SET 
    REV = NULL,
    OBSERVACION = NULL
WHERE REV = 'REVISADO' and Fecha = '2026-07-01' and OBSERVACION is null

UPDATE [Maestro].[dbo].[toa_ahora_CV_estado]
SET 
    REV = NULL,
    OBSERVACION = NULL
WHERE REV is null and Fecha = '2026-04-10' and OBSERVACION = 'BOT 1'


Select "idOT","Rut_Tecnico","Email_Tecnico","observaciones","fecha_realizacion_ot","materialTOA","materialNoS","materialS","Riesgo_Electrico"
from "dbo"."db_ot_digital"





import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=45.239.111.129;"
        "DATABASE=Maestro;"
        "UID=AdolfoP;"
        "PWD=p7@q$rA!sB^tC;"
    )
    
def obtener_access_ids_sql():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT DISTINCT Access_ID
        FROM Maestro.dbo.toa_ahora_CV
        WHERE  
            (OBS IS NULL OR OBS = '')
            AND (REV IS NULL OR REV = '' OR REV = 'NOK')
            AND Access_ID IS NOT NULL
            AND Fecha >= CAST(GETDATE() AS DATE)
            AND Fecha < DATEADD(DAY, 1, CAST(GETDATE() AS DATE))
        """

        cursor.execute(query)

        registros = [{"access_id": row[0]} for row in cursor.fetchall()]

        conn.close()

        return registros

    except Exception as e:
        print("❌ Error SQL:", e)
        return []

def actualizar_comentario_sql(access_id, comentario):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE t
    SET OBS = ?
    FROM Maestro.dbo.toa_ahora_CV t
    WHERE t.Orden_de_Trabajo = (
        SELECT TOP 1 Orden_de_Trabajo
        FROM Maestro.dbo.toa_ahora_CV
        WHERE Access_ID = ?
          AND (OBS IS NULL OR OBS = '')
          AND (REV IS NULL OR REV = '' OR REV = 'NOK')
        ORDER BY Fecha DESC
    )
    """

    cursor.execute(query, comentario, access_id)
    conn.commit()

    if cursor.rowcount > 0:
        print(f"✅ SQL actualizado para {access_id}")
    else:
        print(f"⚠ No se actualizó (no encontrado o ya tenía datos): {access_id}")

    conn.close()
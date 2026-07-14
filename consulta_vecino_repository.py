from sql_reader import get_connection


def existe_access_id(access_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM Maestro.dbo.consulta_ticket_vecino_IDacceso
    WHERE Access_ID = ?
      AND (REV IS NULL OR REV = '')
    """

    cursor.execute(query, access_id)

    existe = cursor.fetchone()[0] > 0

    conn.close()

    return existe


def insertar_access_id(access_id, orden_de_trabajo, observacion):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Maestro.dbo.toa_ahora_CV_estado
    (
        Fecha,
        Access_ID,
        Orden_de_Trabajo,
        REV,
        OBSERVACION,
        Prioridad,
        Inicio
    )
    VALUES
    (
        GETDATE(),
        ?,
        ?,
        '',
        ?,
        1,
        GETDATE()
    )
    """

    cursor.execute(
        query,
        access_id,
        orden_de_trabajo,
        observacion
    )

    conn.commit()

    print(
        f"✅ Consulta Vecino creada | OT: {orden_de_trabajo} | AccessID: {access_id}"
    )

    conn.close()


def registrar_access_id(access_id, orden_de_trabajo, observacion):

    insertar_access_id(
        access_id,
        orden_de_trabajo,
        observacion
    )

    print(
        f"✅ Access_ID registrado | OT: {orden_de_trabajo} | AccessID: {access_id} | Observacion: {observacion} "
    )

    return True
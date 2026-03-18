import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


#FECHA_OBJETIVO = datetime(2026, 3, 17).date()

# ID de tu Google Sheet
SPREADSHEET_ID = "1qDKjlblSkj_UC97SpIP9awKORBRPV1dhFJooKHBksq8"

def obtener_access_ids():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    rows = sheet.get_all_records()

    access_ids = []

    hoy = datetime.now().date()

    for i, row in enumerate(rows):

        fecha = row["FECHA"]
        rev = row["REV"]
        access_id = row["Access_ID"]
        observacion = row["OBSERVACION"]

        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        except:
            continue

        if fecha_dt.date() == hoy:
       

            if (rev == "" or rev == "NOK") and observacion == "":

                access_ids.append({
                    "fila": i + 2,
                    "access_id": access_id
                })

    return access_ids, sheet


if __name__ == "__main__":

    registros, sheet = obtener_access_ids()

    print("Access_ID a revisar:")
    for item in registros:
        print(item)
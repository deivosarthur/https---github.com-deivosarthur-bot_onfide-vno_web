import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ID de tu Google Sheet
SPREADSHEET_ID = "15uAFgW66hhT--WjuhhVB2DRj6Odh-N2ET3aiqhCAEvA"

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

    mes_actual = datetime.now().month
    anio_actual = datetime.now().year

    for i, row in enumerate(rows):

        fecha = row["FECHA"]
        rev = row["REV"]
        access_id = row["Access_ID"]

        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        except:
            continue

        if fecha_dt.month == mes_actual and fecha_dt.year == anio_actual:

            if rev == "" or rev == "NOK":

                access_ids.append({
                    "fila": i + 2,
                    "access_id": access_id
                })

    return access_ids, sheet


if __name__ == "__main__":

    resultado = obtener_access_ids()
    registros = resultado[0]
    sheet = resultado[1]

    print("Access_ID a revisar:")
    for item in ids:
        print(item)
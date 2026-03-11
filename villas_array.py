import pandas as pd
import json

def excel_a_json_archivo(nombre_archivo_excel, nombre_salida="resultado.json"):
    try:
        # 1. Leer el archivo Excel
        df = pd.read_excel(nombre_archivo_excel)
        
        # Limpiar espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()

        lista_final = []

        for _, row in df.iterrows():
            # --- CORRECCIÓN DE DECIMALES ---
            valor_pendiente = str(row['PENDIENTE']).strip().replace(',', '.')
            
            try:
                saldo_float = float(valor_pendiente)
            except ValueError:
                saldo_float = 0.0

            # Lógica Propietario
            propietario_raw = str(row['PROPIETARIO']).strip().lower()
            entregada = "no" if propietario_raw == "no" else "si"

            # --- CORRECCIÓN PARA EL CSS ---
            # Original: "A FAVOR" -> Limpio: "afavor"
            # Original: "CANCELADO" -> Limpio: "cancelado"
            estado_original = str(row['ESTADO']).strip().upper()
            estado_para_css = estado_original.lower().replace(" ", "")

            # Estructura del objeto
            registro = {
                "mz": int(row['Mz']),
                "villa": int(row['Villa']),
                "propietario": entregada,
                "estado": estado_para_css, # <--- Ahora esto enviará "afavor", "adeuda", etc.
                "estado_label": estado_original, # Guardamos el original para el alert() si quieres
                "deuda": saldo_float
            }
            lista_final.append(registro)

        # 2. Guardar archivo
        with open(nombre_salida, 'w', encoding='utf-8') as f:
            json.dump(lista_final, f, indent=4, ensure_ascii=False)

        print(f"✅ Proceso exitoso. Archivo creado: {nombre_salida}")

    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

excel_a_json_archivo('villas.xlsx')
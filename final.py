import pandas as pd
import json

def generar_html(nombre_excel, nombre_html="index.html"):

    df = pd.read_excel(nombre_excel)
    df.columns = df.columns.str.strip()

    lista_final = []

    for _, row in df.iterrows():

        valor_pendiente = str(row['PENDIENTE']).strip().replace(',', '.')

        try:
            saldo_float = float(valor_pendiente)
        except:
            saldo_float = 0.0

        propietario_raw = str(row['PROPIETARIO']).strip().lower()
        entregada = "no" if propietario_raw == "no" else "si"

        estado_original = str(row['ESTADO']).strip().upper()
        estado_css = estado_original.lower().replace(" ", "")

        registro = {
            "mz": int(row['Mz']),
            "villa": int(row['Villa']),
            "propietario": entregada,
            "estado": estado_css,
            "estado_label": estado_original,
            "deuda": saldo_float
        }

        lista_final.append(registro)

    datos_json = json.dumps(lista_final, indent=4, ensure_ascii=False)

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>Mapa Urbanización Villa Geranio 4</title>

<style>

body {{
font-family: Segoe UI;
background:#f0f3f5;
padding:20px;
}}

.mapa {{
display:flex;
flex-wrap:wrap;
gap:25px;
justify-content:center;
}}

.manzana {{
border:1px solid #cfd8dc;
padding:15px;
background:white;
border-radius:10px;
min-width:260px;
}}

.titulo-mz {{
font-weight:bold;
border-bottom:2px solid #3498db;
margin-bottom:10px;
}}

.resumen-mz {{
font-size:12px;
margin-bottom:15px;
background:#f8f9fa;
padding:8px;
}}

.villas-grid {{
display:grid;
grid-template-columns:repeat(6,38px);
gap:5px;
}}

.villa {{
width:38px;
height:38px;
display:flex;
align-items:center;
justify-content:center;
font-size:11px;
cursor:pointer;
border-radius:4px;
font-weight:bold;
}}

.adeuda {{
background:#e74c3c;
color:white;
}}

.cancelado {{
background:#27ae60;
color:white;
}}

.afavor {{
background:#27ae60;
color:white;
}}

.noentregada {{
background:#f39c12;
color:white;
}}

</style>
</head>

<body>

<h2 style="text-align:center">Estado Villas Urbanización</h2>

<div class="mapa" id="mapa"></div>

<script>

const datos = {datos_json}

function resumenMz(mz) {{

const villas = datos.filter(v => v.mz == mz)

return {{

total: villas.length,

alDia: villas.filter(v =>
v.propietario=="si" &&
(v.estado_label=="CANCELADO" || v.estado_label=="A FAVOR")
).length,

adeudan: villas.filter(v =>
v.propietario=="si" && v.estado_label=="ADEUDA"
).length,

noentregadas: villas.filter(v => v.propietario=="no").length

}}

}}

function dibujar() {{

const mapa = document.getElementById("mapa")

const manzanas = [...new Set(datos.map(d => d.mz))].sort()

manzanas.forEach(mz => {{

const r = resumenMz(mz)

let divMz = document.createElement("div")
divMz.className = "manzana"

let titulo = document.createElement("div")
titulo.className = "titulo-mz"
titulo.innerText = "MZ " + mz

let resumen = document.createElement("div")
resumen.className = "resumen-mz"

resumen.innerHTML = `
Villas: <b>${{r.total}}</b><br>
Al día: <b>${{r.alDia}}</b><br>
Adeudan: <b>${{r.adeudan}}</b><br>
No entregadas: <b>${{r.noentregadas}}</b>
`

divMz.appendChild(titulo)
divMz.appendChild(resumen)

let grid = document.createElement("div")
grid.className = "villas-grid"

const villas = datos.filter(v => v.mz == mz)

villas.forEach(v => {{

let clase = ""

if(v.propietario=="no")
clase="noentregada"
else
clase=v.estado

let vDiv = document.createElement("div")
vDiv.className = "villa " + clase
vDiv.innerText = v.villa

vDiv.onclick = () => {{

let det = `MZ: ${{v.mz}} - Villa: ${{v.villa}}\\n`
det += `Propietario: ${{v.propietario}}\\n`
det += `Estado: ${{v.estado_label}}\\n`
det += `Pendiente: $${{v.deuda}}`

alert(det)

}}

grid.appendChild(vDiv)

}})

divMz.appendChild(grid)

mapa.appendChild(divMz)

}})

}}

dibujar()

</script>

</body>
</html>
"""

    with open(nombre_html, "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML generado:", nombre_html)


generar_html("villas.xlsx")
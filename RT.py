import streamlit as st
import sqlite3
from fpdf import FPDF
from datetime import datetime

# Conexión a base local
conn = sqlite3.connect("casos.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre y Apellido TEXT,
    cedula TEXT,
    tienda TEXT,
    problema TEXT,
    responsable TEXT,
    solucion TEXT,
    estado TEXT,
    fecha TEXT
)""")
conn.commit()

st.title("📋 Sistema de Reportes de Tiendas")

# Formulario
with st.form("nuevo_caso"):
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    cedula = st.text_input("Cédula")
    tienda = st.text_input("Nombre de la tienda")
    problema = st.text_area("Problema reportado")
    responsable = st.selectbox(
    "Responsable asignado",
    ["Yofre Rangel", "Simon Meneses", "Andres Changir"]
)
    solucion = st.text_area("Solución (si aplica)")
    estado = st.radio("Estado del caso", ["En proceso", "Resuelto"])
    submit = st.form_submit_button("Guardar caso")

if submit:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO casos (nombre,apellido,cedula,tienda,problema,responsable,solucion,estado,fecha) VALUES (?,?,?,?,?,?,?,?,?)",
          (nombre,apellido,cedula,tienda,problema,responsable,solucion,estado,fecha))
conn.commit()
st.success("✅ Caso guardado correctamente")

# Si está resuelto → generar PDF
if estado == "Resuelto":
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Caso", ln=True, align="C")
    pdf.multi_cell(0, 10, f"""
    ID: {c.lastrowid}
    Nombre: {nombre} {apellido}
    Cédula: {cedula}
    Tienda: {tienda}
    Problema: {problema}
    Responsable: {responsable}
    Solución: {solucion}
    Estado: {estado}
    Fecha: {fecha}
    """)
    pdf.output(f"reporte_{c.lastrowid}.pdf")
    st.success("📄 PDF generado y listo para subir a Drive")

from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_connection

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    conn = get_connection()
    sesiones = conn.execute("SELECT * FROM sesiones ORDER BY fecha DESC").fetchall()
    conn.close()
    return render_template("index.html", sesiones=sesiones)

@app.route("/nueva-sesion", methods=["GET", "POST"])
def nueva_sesion():
    if request.method == "POST":
        fecha = request.form["fecha"]
        notas = request.form["notas"]
        conn = get_connection()
        conn.execute("INSERT INTO sesiones (fecha, notas) VALUES (?, ?)", (fecha, notas))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("nueva_sesion.html")

@app.route("/sesion/<int:sesion_id>")
def ver_sesion(sesion_id):
    conn = get_connection()
    sesion = conn.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,)).fetchone()
    ejercicios = conn.execute("SELECT * FROM ejercicios WHERE sesion_id = ?", (sesion_id,)).fetchall()
    conn.close()
    return render_template("ver_sesion.html", sesion=sesion, ejercicios=ejercicios)

@app.route("/sesion/<int:sesion_id>/agregar-ejercicio", methods=["POST"])
def agregar_ejercicio(sesion_id):
    nombre = request.form["nombre"]
    series = request.form["series"]
    repeticiones = request.form["repeticiones"]
    peso = request.form["peso"]
    conn = get_connection()
    conn.execute(
        "INSERT INTO ejercicios (sesion_id, nombre, series, repeticiones, peso) VALUES (?, ?, ?, ?, ?)",
        (sesion_id, nombre, series, repeticiones, peso)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("ver_sesion", sesion_id=sesion_id))

if __name__ == "__main__":
    app.run(debug=True)
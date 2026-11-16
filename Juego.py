# Pong de una pared, hecho con tkinter (viene incluido con Python, no hay que instalar nada)

import tkinter as tk

# ---------- 1. PREPARACIÓN ----------

ANCHO = 600   # ancho de la ventana de juego
ALTO = 400    # alto de la ventana de juego

# Creamos la ventana y el lienzo donde vamos a dibujar
ventana = tk.Tk()
ventana.title("Pong")
lienzo = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="black")
lienzo.pack()

# Dibujamos la paleta (rectángulo): esquina izquierda-arriba (10,160) y derecha-abajo (20,240)
paleta = lienzo.create_rectangle(10, 160, 20, 240, fill="white")

# Dibujamos la pelota (círculo) en el centro
pelota = lienzo.create_oval(292, 192, 308, 208, fill="white")

# Texto del puntaje, arriba en el medio
texto_puntos = lienzo.create_text(300, 20, text="Puntos: 0", fill="white", font=("Arial", 16))

# Acá guardamos los datos que van cambiando durante el juego
estado = {
    "vx": 4,            # velocidad horizontal de la pelota
    "vy": 3,            # velocidad vertical de la pelota
    "puntos": 0,        # cuántas veces rebotaste la pelota
    "perdiste": False,  # pasa a True cuando se te escapa la pelota
    "subiendo": False,  # True mientras tenés apretada la tecla para subir
    "bajando": False,   # True mientras tenés apretada la tecla para bajar
}

# ---------- 2. TECLADO ----------

# Se ejecuta cuando apretás una tecla
def apretar_tecla(evento):
    if evento.keysym in ("Up", "w"):
        estado["subiendo"] = True
    if evento.keysym in ("Down", "s"):
        estado["bajando"] = True
    if evento.keysym == "space":
        reiniciar()

# Se ejecuta cuando soltás una tecla
def soltar_tecla(evento):
    if evento.keysym in ("Up", "w"):
        estado["subiendo"] = False
    if evento.keysym in ("Down", "s"):
        estado["bajando"] = False

# Le decimos a la ventana qué funciones usar para cada evento
ventana.bind("<KeyPress>", apretar_tecla)
ventana.bind("<KeyRelease>", soltar_tecla)

# ---------- 3. REINICIAR ----------

# Vuelve todo al estado inicial
def reiniciar():
    lienzo.coords(paleta, 10, 160, 20, 240)
    lienzo.coords(pelota, 292, 192, 308, 208)
    lienzo.delete("mensaje")  # borramos el cartel de "Perdiste"
    lienzo.itemconfig(texto_puntos, text="Puntos: 0")
    estado["vx"] = 4
    estado["vy"] = 3
    estado["puntos"] = 0
    estado["perdiste"] = False

# ---------- 4. BUCLE DEL JUEGO ----------

# Esta función se repite sola unas 60 veces por segundo
def jugar():
    if not estado["perdiste"]:

        # Posición actual de la paleta: x1, y1 (arriba-izq) y x2, y2 (abajo-der)
        px1, py1, px2, py2 = lienzo.coords(paleta)

        # Mover la paleta (sin dejar que se salga de la pantalla)
        if estado["subiendo"] and py1 > 0:
            lienzo.move(paleta, 0, -8)
        if estado["bajando"] and py2 < ALTO:
            lienzo.move(paleta, 0, 8)

        # Mover la pelota sumando su velocidad
        lienzo.move(pelota, estado["vx"], estado["vy"])

        # Posición actual de la pelota (y de la paleta, que pudo moverse)
        x1, y1, x2, y2 = lienzo.coords(pelota)
        px1, py1, px2, py2 = lienzo.coords(paleta)

        # Rebote contra el techo: va hacia abajo
        if y1 <= 0:
            estado["vy"] = abs(estado["vy"])

        # Rebote contra el piso: va hacia arriba
        if y2 >= ALTO:
            estado["vy"] = -abs(estado["vy"])

        # Rebote contra la pared derecha: va hacia la izquierda
        if x2 >= ANCHO:
            estado["vx"] = -abs(estado["vx"])

        # ¿La pelota toca la paleta? (la pelota va hacia la izquierda, y se superponen)
        toca_paleta = (
            estado["vx"] < 0
            and x1 <= px2 and x2 >= px1   # coinciden en horizontal
            and y2 >= py1 and y1 <= py2   # coinciden en vertical
        )

        if toca_paleta:
            estado["vx"] = abs(estado["vx"]) * 1.05   # rebota a la derecha, un poco más rápida
            estado["puntos"] = estado["puntos"] + 1   # sumamos un punto
            lienzo.itemconfig(texto_puntos, text="Puntos: " + str(estado["puntos"]))

        # Si la pelota se fue por detrás de la paleta, perdiste
        if x2 < 0:
            estado["perdiste"] = True
            lienzo.create_text(300, 190, text="¡Perdiste!", fill="white",
                               font=("Arial", 36), tags="mensaje")
            lienzo.create_text(300, 235, text="Apretá espacio para jugar de nuevo",
                               fill="white", font=("Arial", 14), tags="mensaje")

    # Volver a llamar a esta misma función dentro de 16 milisegundos
    ventana.after(16, jugar)

# ---------- 5. ARRANCAR ----------

jugar()               # empezamos el bucle
ventana.mainloop()    # mantiene la ventana abierta y escuchando el teclado

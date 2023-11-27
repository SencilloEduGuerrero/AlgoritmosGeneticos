from GA import *
from tkinter import *


# Método para cerrar la ventana.
def close_window(_event):
    window.destroy()
    quit()


# Método para dibujar.
def re_draw(self):
    genetic_algo.visualize_genetic_algorithm(canvasOrig, canvasMid, canvasAG, 3, 1600)


# Siempre correrá el programa main.
if __name__ == "__main__":
    # Creación de ventana.
    window = Tk()
    window.geometry("1295x500")
    window.resizable(width=False, height=False)
    window.title("Algoritmos Genéticos")
    window.config(background="#FFFFFF")

    # Creación del primer canvas.
    canvasOrig = Canvas(window, width=400, height=400)
    canvasOrig.pack(side="left", expand=False)
    canvasOrig.place(x=10, y=25)

    # Creación del segundo canvas.
    canvasMid = Canvas(window, width=400, height=400)
    canvasMid.pack(side="left", expand=False)
    canvasMid.place(x=445, y=25)

    # Creación del tercer canvas.
    canvasAG = Canvas(window, width=400, height=400)
    canvasAG.pack(side="right", expand=False)
    canvasAG.place(x=880, y=25)

    # Labels ubicados debajo de cada canvas.
    label = Label(window, text="Inicio", anchor="center", bg="white")
    label.pack()
    label.config(font=("Verdana", 24))
    label.place(x=160, y=440)

    label = Label(window, text="Desarrollo", anchor="center", bg="white")
    label.config(font=("Verdana", 24))
    label.place(x=550, y=440)

    label = Label(window, text="Final", anchor="center", bg="white")
    label.config(font=("Verdana", 24))
    label.place(x=1040, y=440)

    # Algoritmo en desarrollo con sus métodos.
    genetic_algo = gene()
    genetic_algo.generar_generacion(3, 1600)
    genetic_algo.generar_generacion_population(3, 1600, genetic_algo.generate_population(10, 3))
    # genetic_algo.visualize_genetic_algorithm(canvasOrig, canvasMid, canvasAG, 3, 100)

    # Si se presiona ESCAPE cierra el programa.
    window.bind('<Escape>', close_window)
    # Si se da doble click ejecuta el programa.
    window.bind('<Double-1>', re_draw)

    window.mainloop()

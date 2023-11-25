from GA import *
from tkinter import *


def close_window(_event):
    window.destroy()
    quit()


if __name__ == "__main__":
    window = Tk()
    window.geometry("1295x500")
    window.resizable(width=False, height=False)
    window.title("Algoritmos Genéticos")
    window.config(background="#FFFFFF")

    canvasOrig = Canvas(window, width=400, height=400)
    canvasOrig.pack(side="left", expand=False)
    canvasOrig.place(x=10, y=25)

    canvasMid = Canvas(window, width=400, height=400)
    canvasMid.pack(side="left", expand=False)
    canvasMid.place(x=445, y=25)

    canvasAG = Canvas(window, width=400, height=400)
    canvasAG.pack(side="right", expand=False)
    canvasAG.place(x=880, y=25)

    label = Label(window, text="Inicio", anchor="center", bg="white")
    label.pack()
    label.config(font=("Verdana", 24))
    label.place(x=125, y=440)

    label = Label(window, text="Desarrollo", anchor="center", bg="white")
    label.pack()
    label.config(font=("Verdana", 24))
    label.place(x=600, y=440)

    label = Label(window, text="Final", anchor="center", bg="white")
    label.pack()
    label.config(font=("Verdana", 24))
    label.place(x=1040, y=440)

    genetic_algo = gene()
    genetic_algo.visualize_genetic_algorithm(canvasOrig, canvasMid, canvasAG, 3, 100)

    window.bind('<Escape>', close_window)
    window.mainloop()

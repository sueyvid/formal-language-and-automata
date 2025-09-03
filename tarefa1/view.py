import tkinter as tk
from tkinter import filedialog as fd
import os

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.filename = None

        self.title("Sem arquivo - Máquina de estados")
        self.geometry("600x600")

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.button_open = tk.Button(self.frame, text="Abrir arquivo", command=self.buscar, font=("Arial", 16))
        self.button_open.grid(row=0, column=0, columnspan=3)

        self.texto_var = tk.StringVar()
        self.label = tk.Label(self.frame, textvariable=self.texto_var, font=("Arial", 16))
        self.label.grid(row=1, column=0, columnspan=3, pady=20)

        self.button0 = tk.Button(self.frame, text="0", command=lambda: self.button_clicked(0), width=12, height=5, font=("Arial", 16))
        self.button0.grid(row=2,column=0, padx=10)
        self.button1 = tk.Button(self.frame, text="1", command=lambda: self.button_clicked(1), width=12, height=5, font=("Arial", 16))
        self.button1.grid(row=2,column=1, padx=10)
        self.button2 = tk.Button(self.frame, text="r", command=lambda: self.button_clicked(2), width=12, height=5, font=("Arial", 16))
        self.button2.grid(row=2,column=2, padx=10)

        self.controler = None

    def set_controller(self, controller):
        self.controller = controller

    def button_clicked(self, valor):
        if self.controller and self.filename:
            self.controller.processar(valor)
            self.texto_var.set(self.controller.estado_atual())

    def buscar(self):
        filetypes = (
            ('text files', '*.csv'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./dados',
            filetypes=filetypes)

        if filename:
            self.filename = filename
            self.carregar_arquivo()

    def carregar_arquivo(self):
        if self.filename:
            nome_arquivo = os.path.basename(self.filename)
            self.title(f"{nome_arquivo} - Máquina de estados")
            self.controller.carregar_arquivo(self.filename)
            self.texto_var.set("")

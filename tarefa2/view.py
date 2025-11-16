import tkinter as tk
from tkinter import filedialog as fd
import os

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.filename = None

        self.title("Sem arquivo - Máquina de estados")
        self.geometry("600x600")
        self.minsize(600, 400)

        self.button_open = tk.Button(self, text="Abrir arquivo", command=self.buscar, font=("Arial", 16))
        self.button_open.pack(side=tk.TOP, expand=False, pady=20)

        self.text_out = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text_out, font=("Arial", 16))
        self.label.pack(side=tk.TOP, expand=False, pady=50)

        self.text_in = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.text_in, font=("Arial", 16))
        self.entry.pack(side=tk.TOP, expand=False, pady=20)
        self.text_in.trace("w", self.processar)

        self.controler = None

    def set_controller(self, controller):
        self.controller = controller

    def button_clicked(self, valor):
        if self.controller and self.filename:
            self.controller.processar(valor)
            self.text_out.set(self.controller.estado_atual())

    def processar(self, *args):
        nome_arquivo = os.path.basename(self.filename)
        n = int(nome_arquivo[0])
        if self.controller and self.filename and self.text_in.get():
            try:
                entrada = self.text_in.get()
                if len(entrada) <= 3:
                    digito = f"{int(entrada):03d}"
                else:
                    digito = f"{int(entrada):0{n}d}"
                if len(self.text_in.get()) <= n:
                    s = ""
                    for i, value in enumerate(digito):
                        self.controller.processar(int(value))
                        if self.controller.saida_atual() != " ":
                            s += self.controller.saida_atual()
                        if i == 2 and len(entrada) > 3:
                            s += " mil, "
                    self.text_out.set(s)
                else:
                    raise
            except:
                self.text_out.set("entrada inválida")
        else:
            self.text_out.set("")
         

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
            self.text_out.set("")

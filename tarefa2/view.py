import tkinter as tk
from tkinter import filedialog as fd
import os
from scrollable_frame import ScrollableFrame

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.filename = None

        self.title("Sem arquivo - Máquina de estados")
        self.geometry("330x300")
        self.minsize(330, 300)
        
        self.frame_configs = tk.Frame(self)
        self.frame_configs.pack(side=tk.TOP, expand=False)
        self.button_open = tk.Button(self.frame_configs, text="Abrir arquivo", command=self.buscar, font=("Arial", 13))
        self.button_open.grid(row=0, column=0, pady=5)

        self.frame_expand = tk.Frame(self)
        self.frame_expand.pack(side=tk.TOP, expand=True)

        sf = ScrollableFrame(self.frame_expand)

        for i in range(20):
            sf.adicionar_conteudo(f"Item {i}")

        self.frame_aplicacao = tk.Frame(self)
        self.frame_aplicacao.pack(side=tk.TOP, expand=False)

        self.frame_fixo = tk.Frame(self.frame_aplicacao)
        self.frame_fixo.pack(side="bottom", padx=5)

        self.frame_visor = tk.Frame(self.frame_fixo, bg="#eeeeee")
        self.frame_visor.pack()
        self.texto_var = tk.StringVar()
        self.label = tk.Label(self.frame_visor, textvariable=self.texto_var, font=("Arial", 13), bg="#eeeeee")
        self.label.grid(row=1, column=0, columnspan=3, pady=20, padx=30)

        self.frame_buttons = tk.Frame(self.frame_fixo)
        self.frame_buttons.pack(padx=5, pady=5)
        self.button0 = tk.Button(self.frame_buttons, text="0", command=lambda: self.button_clicked(0), width=4, height=2, font=("Arial", 13))
        self.button0.grid(row=2,column=0, padx=2, pady=2, sticky="NSWE")
        self.button1 = tk.Button(self.frame_buttons, text="1", command=lambda: self.button_clicked(1), width=4, height=2, font=("Arial", 13))
        self.button1.grid(row=2,column=1, padx=2, pady=2, sticky="NSWE")
        self.button2 = tk.Button(self.frame_buttons, text="r", command=lambda: self.button_clicked(2), width=4, height=2, font=("Arial", 13))
        self.button2.grid(row=2,column=2, padx=2, pady=2, sticky="NSWE")

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

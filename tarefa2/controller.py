import pandas as pd

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def processar(self, valor):
        self.model.processar(valor)

    def saida_atual(self):
        return self.model.saida_atual()

    def carregar_arquivo(self, filename):
        df = pd.read_csv(filename, header=None)
        matriz = df.values.tolist()
        TE = matriz[:10]
        VS = matriz[10:]
        self.model.definir_maquina(TE, VS)
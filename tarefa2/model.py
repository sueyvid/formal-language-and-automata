import pandas as pd

class Model:
    def __init__(self, TE=None, VS=None):
        self.TE = TE
        self.VS = VS

        self.entrada = None
        self.estado = 0
        self.saida = None
    
    def processar(self, valor):
        self.entrada = valor
        self.saida = self.VS[self.entrada][self.estado]
        self.estado = int(self.TE[self.entrada][self.estado])

    def definir_maquina(self, TE, VS):
        self.TE = TE
        self.VS = VS

    def estado_atual(self):
        return f"entrada: {self.entrada}, estado: {self.estado}, saída: {self.saida}"
    
    def saida_atual(self):
        return self.saida
    
    def __str__(self):
        return f"entrada: {self.entrada}, estado: {self.estado}, saída: {self.saida}"
    
if __name__ == "__main__":
    df = pd.read_csv("dados/numeros_por_extenso.csv", header=None)
    matriz = df.values.tolist()
    TE = matriz[:10]
    VS = matriz[10:]
    m = Model()
    m.definir_maquina(TE, VS)

    m.processar(5)
    print(m.estado_atual())
    m.processar(3)
    print(m.estado_atual())
    m.processar(2)
    print(m.estado_atual())
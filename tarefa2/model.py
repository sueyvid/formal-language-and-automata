class Model:
    def __init__(self, TE=None, VS=None):
        self.TE = TE
        self.VS = VS

        self.entrada = None
        self.estado = 0
        self.saida = None
    
    def processar(self, valor):
        self.entrada = valor
        self.estado = self.TE[self.entrada][self.estado]
        self.saida = self.VS[self.estado]

    def definir_maquina(self, TE, VS):
        self.TE = TE
        self.VS = VS

    def estado_atual(self):
        return f"entrada: {self.entrada}, estado: {self.estado}, saída: {self.saida}"
    
    def __str__(self):
        return f"entrada: {self.entrada}, estado: {self.estado}, saída: {self.saida}"
    
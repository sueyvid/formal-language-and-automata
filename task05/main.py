# ---------------------------------------------
# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DCA-3705 – AUTÔMATOS E LINGUAGENS FORMAIS
# Lista 5 – Autômato com Pilha Determinístico (DPDA)
# Autor: Sueyvid José
# ---------------------------------------------

class DPDA:
    def __init__(self, estados, alfabeto_entrada, alfabeto_pilha, transicoes,
                 estado_inicial, simbolo_inicial_pilha, estados_finais):
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_pilha = alfabeto_pilha
        self.transicoes = transicoes  # dicionário {(estado, símbolo, topo_pilha): (novo_estado, nova_pilha)}
        self.estado_inicial = estado_inicial
        self.simbolo_inicial_pilha = simbolo_inicial_pilha
        self.estados_finais = estados_finais

    def processar(self, entrada):
        estado = self.estado_inicial
        pilha = [self.simbolo_inicial_pilha]

        for simbolo in entrada:
            topo = pilha[-1] if pilha else None
            chave = (estado, simbolo, topo)

            if chave not in self.transicoes:
                # tenta transição com epsilon (None) se existir
                chave = (estado, None, topo)
                if chave not in self.transicoes:
                    print(f"❌ Transição não encontrada para {chave}")
                    return False

            novo_estado, acao_pilha = self.transicoes[chave]
            estado = novo_estado

            # Atualiza pilha
            if acao_pilha == 'ε':  # desempilha
                pilha.pop()
            elif acao_pilha != '':  # empilha novo símbolo
                pilha.pop()
                pilha.append(acao_pilha)

            print(f"Símbolo: {simbolo}, Estado: {estado}, Pilha: {pilha}")

        # Após consumir entrada, verifica se está em estado final e pilha vazia
        aceita = estado in self.estados_finais and (not pilha or pilha == [self.simbolo_inicial_pilha])
        return aceita


# ---------------------------------------------------------
# Exemplo 1: L = { a^n b^n | n ≥ 0 }
# ---------------------------------------------------------
def exemplo_a_n_b_n():
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'a', 'b'}
    alfabeto_pilha = {'Z', 'A'}
    transicoes = {
        ('q0', 'a', 'Z'): ('q0', 'A'),     # empilha A
        ('q0', 'a', 'A'): ('q0', 'A'),     # empilha mais A
        ('q0', 'b', 'A'): ('q1', 'ε'),     # começa a desempilhar
        ('q1', 'b', 'A'): ('q1', 'ε'),
        ('q1', None, 'Z'): ('qf', 'Z'),    # epsilon move para final
    }
    estado_inicial = 'q0'
    simbolo_inicial_pilha = 'Z'
    estados_finais = {'qf'}

    dpda = DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes,
                estado_inicial, simbolo_inicial_pilha, estados_finais)

    for cadeia in ['aabb', 'aaabbb', 'ab', 'aab', 'abb']:
        print(f"\nTestando cadeia: {cadeia}")
        resultado = dpda.processar(cadeia)
        print("✅ Aceita" if resultado else "❌ Rejeitada")


# ---------------------------------------------------------
# Exemplo 2: L = { 0^n 1^m | n, m ≥ 0 }
# ---------------------------------------------------------
def exemplo_0n_1m():
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'0', '1'}
    alfabeto_pilha = {'Z'}
    transicoes = {
        ('q0', '0', 'Z'): ('q0', 'Z'),    # ignora 0s
        ('q0', '1', 'Z'): ('q1', 'Z'),    # passa para ler 1s
        ('q1', '1', 'Z'): ('q1', 'Z'),    # continua lendo 1s
        ('q1', None, 'Z'): ('qf', 'Z'),   # move para final
    }
    estado_inicial = 'q0'
    simbolo_inicial_pilha = 'Z'
    estados_finais = {'qf'}

    dpda = DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes,
                estado_inicial, simbolo_inicial_pilha, estados_finais)

    for cadeia in ['00011', '001', '111', '000', '']:
        print(f"\nTestando cadeia: {cadeia}")
        resultado = dpda.processar(cadeia)
        print("✅ Aceita" if resultado else "❌ Rejeitada")


# ---------------------------------------------------------
# Execução
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== Exemplo 1: L = { a^n b^n } ===")
    exemplo_a_n_b_n()
    print("\n=== Exemplo 2: L = { 0^n 1^m } ===")
    exemplo_0n_1m()

from typing import Dict, Tuple, Optional, List

Action = Tuple[str, Optional[str]]  # ('push', 'A') | ('pop', None) | ('nop', None)
TransitionKey = Tuple[str, Optional[str], str]  # (estado, simbolo_entrada_or_None, topo_pilha)
TransitionVal = Tuple[str, Action]  # (novo_estado, acao_sobre_pilha)


class DPDA:
    def __init__(self,
                 estados: set,
                 alfabeto_entrada: set,
                 alfabeto_pilha: set,
                 transicoes: Dict[TransitionKey, TransitionVal],
                 estado_inicial: str,
                 simbolo_inicial_pilha: str,
                 estados_finais: set):
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_pilha = alfabeto_pilha
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.simbolo_inicial_pilha = simbolo_inicial_pilha
        self.estados_finais = estados_finais

    def _aplicar_acao_pilha(self, pilha: List[str], acao: Action) -> None:
        tipo, valor = acao
        if tipo == 'pop':
            if pilha:
                pilha.pop()
            else:
                raise RuntimeError("Tentativa de pop em pilha vazia")
        elif tipo == 'push':
            pilha.append(valor)
        elif tipo == 'nop':
            pass
        else:
            raise ValueError(f"Ação desconhecida na pilha: {acao}")

    def _buscar_transicao(self, estado: str, simbolo: Optional[str], topo: str) -> Optional[TransitionVal]:
        chave = (estado, simbolo, topo)
        return self.transicoes.get(chave, None)

    def processar(self, entrada: str, verbose: bool = False) -> bool:
        """
        Processa a cadeia 'entrada'. Retorna True se aceita, False caso contrário.
        Se verbose=True, imprime trace dos passos; caso contrário, apenas retorna o booleano.
        """
        estado = self.estado_inicial
        pilha: List[str] = [self.simbolo_inicial_pilha]

        pos = 0
        n = len(entrada)

        if verbose:
            print(f"Estado inicial: {estado}, Pilha inicial: {pilha}, Entrada: '{entrada}'\n")

        while pos < n:
            simbolo = entrada[pos]
            topo = pilha[-1] if pilha else ''
            # tenta transição com símbolo lido
            trans = self._buscar_transicao(estado, simbolo, topo)

            # se não existe, tenta transição ε (None)
            if trans is None:
                trans = self._buscar_transicao(estado, None, topo)
                using_epsilon = trans is not None
            else:
                using_epsilon = False

            if trans is None:
                if verbose:
                    print(f"❌ Nenhuma transição aplicável em (estado={estado}, simbolo={simbolo}, topo={topo}). Rejeita.")
                return False

            novo_estado, acao = trans
            if verbose:
                if using_epsilon:
                    print(f"--> Aplica transição ε: ({estado}, ε, {topo}) -> ( {novo_estado}, {acao} )")
                else:
                    print(f"--> Aplica transição: ({estado}, {simbolo}, {topo}) -> ( {novo_estado}, {acao} )")

            # aplica ação de pilha
            try:
                self._aplicar_acao_pilha(pilha, acao)
            except Exception as e:
                if verbose:
                    print("Erro ao aplicar ação na pilha:", e)
                return False

            estado = novo_estado

            # só avança na fita se não foi uma transição epsilon
            if not using_epsilon:
                pos += 1

            if verbose:
                consumed = entrada[:pos]
                remaining = entrada[pos:]
                print(f"Consumi: '{consumed}' | Estado: {estado} | Pilha: {pilha} | Restam: '{remaining}'")

        # entrada consumida; aplicar transições ε remanescentes (até limite)
        if verbose:
            print("\nEntrada consumida. Tentando aplicar transições ε remanescentes (se houver).")

        max_eps_steps = 1000
        eps_steps = 0
        changed = True
        while eps_steps < max_eps_steps and changed:
            changed = False
            topo = pilha[-1] if pilha else ''
            trans = self._buscar_transicao(estado, None, topo)
            if trans is not None:
                novo_estado, acao = trans
                if verbose:
                    print(f"--> Aplica transição ε pós-entrada: ({estado}, ε, {topo}) -> ( {novo_estado}, {acao} )")
                try:
                    self._aplicar_acao_pilha(pilha, acao)
                except Exception as e:
                    if verbose:
                        print("Erro ao aplicar ação na pilha:", e)
                    return False
                estado = novo_estado
                changed = True
                eps_steps += 1

        if eps_steps >= max_eps_steps:
            if verbose:
                print("⚠️ Máximo de passos ε atingido — possível loop de ε. Rejeita para segurança.")
            return False

        aceita = (estado in self.estados_finais) and (pilha == [self.simbolo_inicial_pilha])
        # se verbose=True, mostramos detalhes; caso contrário, apenas retornamos booleano
        if verbose:
            if aceita:
                print(f"\nEstado final: {estado}, Pilha final: {pilha}")
                print("✅ Aceita")
            else:
                print(f"\nEstado final: {estado}, Pilha final: {pilha}")
                print("❌ Rejeitada")
        return aceita


# ---------------------------
# Construção dos DPDAs de exemplo
# ---------------------------

def montar_dpda_anbn() -> DPDA:
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'a', 'b'}
    alfabeto_pilha = {'Z', 'A'}
    Z = 'Z'
    transicoes: Dict[TransitionKey, TransitionVal] = {
        ('q0', 'a', 'Z'): ('q0', ('push', 'A')),
        ('q0', 'a', 'A'): ('q0', ('push', 'A')),
        ('q0', 'b', 'A'): ('q1', ('pop', None)),
        ('q1', 'b', 'A'): ('q1', ('pop', None)),
        ('q1', None, 'Z'): ('qf', ('nop', None)),
        ('q0', None, 'Z'): ('qf', ('nop', None)),
    }
    return DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes, 'q0', Z, {'qf'})


def montar_dpda_0n1m() -> DPDA:
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'0', '1'}
    alfabeto_pilha = {'Z'}
    Z = 'Z'
    transicoes: Dict[TransitionKey, TransitionVal] = {
        ('q0', '0', 'Z'): ('q0', ('nop', None)),
        ('q0', '1', 'Z'): ('q1', ('nop', None)),
        ('q1', '1', 'Z'): ('q1', ('nop', None)),
        ('q0', None, 'Z'): ('qf', ('nop', None)),
        ('q1', None, 'Z'): ('qf', ('nop', None)),
    }
    return DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes, 'q0', Z, {'qf'})


# ---------------------------
# Execução: imprime apenas ACEITA/REJEITADA por entrada
# ---------------------------

def run_tests_minimal_output():
    dpda1 = montar_dpda_anbn()
    testes1 = ['', 'ab', 'aabb', 'aaabbb', 'aab', 'abb']
    # imprime apenas indicação de reconhecimento
    for s in testes1:
        aceita = dpda1.processar(s, verbose=False)
        print(f"'{s}' -> {'ACEITA' if aceita else 'REJEITADA'}")

    dpda2 = montar_dpda_0n1m()
    testes2 = ['', '00011', '001', '111', '000']
    for s in testes2:
        aceita = dpda2.processar(s, verbose=False)
        print(f"'{s}' -> {'ACEITA' if aceita else 'REJEITADA'}")


if __name__ == "__main__":
    # Apenas saídas mínimas, como requisitado
    run_tests_minimal_output()

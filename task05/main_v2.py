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
            # empilha sem remover o topo (pilha cresce)
            pilha.append(valor)
        elif tipo == 'nop':
            pass
        else:
            raise ValueError(f"Ação desconhecida na pilha: {acao}")

    def _buscar_transicao(self, estado: str, simbolo: Optional[str], topo: str) -> Optional[TransitionVal]:
        chave = (estado, simbolo, topo)
        return self.transicoes.get(chave, None)

    def processar(self, entrada: str, verbose: bool = True) -> bool:
        """
        Processa a cadeia 'entrada'. Retorna True se aceita, False caso contrário.
        Se verbose=True, imprime trace dos passos.
        """
        estado = self.estado_inicial
        pilha: List[str] = [self.simbolo_inicial_pilha]

        pos = 0
        n = len(entrada)

        if verbose:
            print(f"Estado inicial: {estado}, Pilha inicial: {pilha}, Entrada: '{entrada}'\n")

        # função auxiliar para mostrar estado atual
        def show(step_sym=None):
            if verbose:
                consumed = entrada[:pos]
                remaining = entrada[pos:]
                print(f"Consumi: '{consumed}' | Próximo: '{step_sym}' | Estado: {estado} | Pilha: {pilha} | Restam: '{remaining}'")

        while pos < n:
            simbolo = entrada[pos]
            topo = pilha[-1] if pilha else ''  # topo sempre existirá por causa do símbolo inicial
            # primeiro tenta transição com o símbolo lido
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

            show(simbolo)

        # entrada consumida; ainda podemos aplicar transições ε repetidamente (até um limite)
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

        if verbose:
            print(f"\nEstado final: {estado}, Pilha final: {pilha}")
        aceita = (estado in self.estados_finais) and (pilha == [self.simbolo_inicial_pilha])
        if verbose:
            print("✅ Aceita" if aceita else "❌ Rejeitada")
        return aceita

# Exemplos

def montar_dpda_anbn() -> DPDA:
    """
    DPDA que reconhece L = { a^n b^n | n >= 0 }
    Estratégia:
    - Em q0: para cada 'a' push 'A'.
    - Ao ler o primeiro 'b' (com topo 'A'), vai para q1 e pop 'A'.
    - Em q1: para cada 'b' pop 'A'.
    - Quando topo volta a 'Z' (símbolo inicial), há transição ε para qf (final) com 'nop'.
    Aceitação: estado final e pilha contendo apenas 'Z'.
    """
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'a', 'b'}
    alfabeto_pilha = {'Z', 'A'}
    Z = 'Z'
    transicoes: Dict[TransitionKey, TransitionVal] = {
        # empilha A para cada 'a' (não remove o topo)
        ('q0', 'a', 'Z'): ('q0', ('push', 'A')),
        ('q0', 'a', 'A'): ('q0', ('push', 'A')),

        # ao ver b, começa a desempilhar A (vai para q1)
        ('q0', 'b', 'A'): ('q1', ('pop', None)),
        ('q1', 'b', 'A'): ('q1', ('pop', None)),

        # quando a pilha voltar ao Z, podemos ir ao estado final por epsilon
        ('q1', None, 'Z'): ('qf', ('nop', None)),

        # caso vazio de entrada (n=0): em q0 com topo Z aceitamos via epsilon p/ qf
        ('q0', None, 'Z'): ('qf', ('nop', None)),
    }
    return DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes, 'q0', Z, {'qf'})


def montar_dpda_0n1m() -> DPDA:
    """
    DPDA que reconhece L = { 0^n 1^m | n,m >= 0 } (qualquer número de 0s seguidos por 1s).
    Estratégia:
    - q0 lê 0s; ao ver '1' vai para q1 e permanece.
    - pilha praticamente não é usada (apenas Z).
    """
    estados = {'q0', 'q1', 'qf'}
    alfabeto_entrada = {'0', '1'}
    alfabeto_pilha = {'Z'}
    Z = 'Z'
    transicoes: Dict[TransitionKey, TransitionVal] = {
        ('q0', '0', 'Z'): ('q0', ('nop', None)),
        ('q0', '1', 'Z'): ('q1', ('nop', None)),
        ('q1', '1', 'Z'): ('q1', ('nop', None)),
        # aceitar vazio ou terminar em q1 via epsilon
        ('q0', None, 'Z'): ('qf', ('nop', None)),
        ('q1', None, 'Z'): ('qf', ('nop', None)),
    }
    return DPDA(estados, alfabeto_entrada, alfabeto_pilha, transicoes, 'q0', Z, {'qf'})


# Testes rápidos

def testar_exemplo_anbn():
    dpda = montar_dpda_anbn()
    testes = ['', 'ab', 'aabb', 'aaabbb', 'aaaabbbb', 'aab', 'abb', 'ba', 'aaabb']
    print("\n=== Testes L = { a^n b^n } ===")
    for s in testes:
        print(f"\n--- Testando: '{s}'")
        dpda.processar(s, verbose=True)


def testar_exemplo_0n1m():
    dpda = montar_dpda_0n1m()
    testes = ['','00011','001','111','000','010','101']
    print("\n=== Testes L = { 0^n 1^m } ===")
    for s in testes:
        print(f"\n--- Testando: '{s}'")
        dpda.processar(s, verbose=True)


if __name__ == "__main__":
    # Executa os dois exemplos
    testar_exemplo_anbn()
    testar_exemplo_0n1m()

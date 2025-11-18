import json

class Grammar:
    def __init__(self, variables, terminals, rules, start):
        self.variables = variables
        self.terminals = terminals
        self.rules = rules  # dict: A -> [right_sides]
        self.start = start

    def get_active_rules(self, sentential):
        active = []
        rule_number = 1

        for left, prods in self.rules.items():
            for right in prods:
                if left in sentential:
                    active.append((rule_number, left, right))
                rule_number += 1
        return active

    def apply_rule(self, sentential, left, right):
        return sentential.replace(left, right, 1)


def load_from_keyboard():
    print("\n=== Entrada manual da gramática ===")
    variables = input("Variáveis (ex: A B S): ").split()
    terminals = input("Terminais (ex: a b 0 1): ").split()
    start = input("Símbolo inicial: ").strip()

    rules = {}
    print("\nInforme regras no formato A->bc | A->aA | ...")
    print("Digite 'fim' para encerrar\n")

    while True:
        line = input("Regra: ").strip()
        if line == "fim":
            break
        left, rights = line.split("->")
        left = left.strip()
        prods = [p.strip() for p in rights.split("|")]
        rules.setdefault(left, []).extend(prods)

    return Grammar(variables, terminals, rules, start)


def load_from_file(path):
    print("\n=== Lendo gramática do arquivo ===")
    with open(path, "r") as f:
        data = json.load(f)
    return Grammar(data["V"], data["Sigma"], data["R"], data["S"])


def load_default_grammars():
    print("\nSelecione uma gramática de teste:")
    print("1) Palíndromos sobre {a,b}")
    print("2) G = <{A,B}, {0,1}, R, A>")
    op = input("Escolha: ")

    if op == "1":
        return Grammar(
            ["S"],
            ["a", "b"],
            {
                "S": ["aSa", "bSb", "a", "b", ""]
            },
            "S"
        )
    else:
        return Grammar(
            ["A", "B"],
            ["0", "1"],
            {"A": ["0A1", "1A0", "B"],
             "B": ["01", "10"]},
            "A"
        )


def choose_configuration():
    print("=== Configuração da Gramática ===")
    print("1) Usar gramática embutida (palíndromos ou a gramática do enunciado)")
    print("2) Ler gramática de um arquivo .json")
    print("3) Digitar a gramática manualmente")
    op = input("Escolha: ")

    if op == "1":
        return load_default_grammars()
    elif op == "2":
        path = input("Caminho do arquivo JSON: ")
        return load_from_file(path)
    else:
        return load_from_keyboard()


def main():
    grammar = choose_configuration()
    current = grammar.start

    print("\n===============================")
    print("Iniciando derivação…")
    print("Sentencial inicial:", current)
    print("===============================")

    rule_list = []
    # Criar lista numerada de regras apenas uma vez
    for left, prods in grammar.rules.items():
        for right in prods:
            rule_list.append((left, right))

    while True:
        active = grammar.get_active_rules(current)

        if not active:
            print("\nSem regras aplicáveis. Derivação encerrada.")
            print("Sentencial final:", current)
            break

        print("\nSentencial atual:", current)
        print("Regras aplicáveis:")

        for num, left, right in active:
            print(f"{num}) {left} -> {right}")

        escolha = int(input("\nEscolha o número da regra: "))

        valid_nums = [num for num, _, _ in active]
        if escolha not in valid_nums:
            print("Regra inválida. Tente novamente.")
            continue

        left, right = rule_list[escolha - 1]
        current = grammar.apply_rule(current, left, right)

        print(f"\nAplicando regra {escolha}: {left} -> {right}")
        print("Novo sentencial:", current)


if __name__ == "__main__":
    main()

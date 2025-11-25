import re

# Token types
NUMBER = "NUMBER"
PLUS = "PLUS"
STAR = "STAR"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF = "EOF"

# Lexer
class Lexer:
    token_spec = [
        (NUMBER, r"[0-9]+"),
        (PLUS, r"\+"),
        (STAR, r"\*"),
        (LPAREN, r"\("),
        (RPAREN, r"\)"),
        ("SKIP", r"[ \t]+"),
        ("MISMATCH", r"."),
    ]
    def __init__(self, text):
        self.text = text
        parts = [f"(?P<{name}>{pattern})" for name, pattern in self.token_spec]
        self.regex = re.compile("|".join(parts))
        self.tokens = self.tokenize()
        self.pos = 0

    def tokenize(self):
        tokens = []
        for m in self.regex.finditer(self.text):
            kind = m.lastgroup
            value = m.group()
            if kind == NUMBER:
                tokens.append((NUMBER, int(value)))
            elif kind == PLUS:
                tokens.append((PLUS, value))
            elif kind == STAR:
                tokens.append((STAR, value))
            elif kind == LPAREN:
                tokens.append((LPAREN, value))
            elif kind == RPAREN:
                tokens.append((RPAREN, value))
            elif kind == "SKIP":
                continue
            else:
                raise Exception(f"Erro léxico: símbolo inesperado '{value}'")
        tokens.append((EOF, None))
        return tokens

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

class ParserOptimized:
    def __init__(self, lexer):
        self.lexer = lexer

    def eat(self, token_type):
        tok = self.lexer.peek()
        if tok[0] == token_type:
            return self.lexer.advance()
        # Melhora a mensagem de erro mostrando onde parou
        raise Exception(f"Erro sintático: Esperado '{token_type}', mas encontrou '{tok[1]}' (Tipo: {tok[0]})")

    def parse(self):
        result = self.E()
        # Garante que não sobrou lixo no final da string
        if self.lexer.peek()[0] != EOF:
             raise Exception("Erro sintático: Entrada contém caracteres extras após a expressão válida.")
        return result

    # E -> T (+ T)*
    def E(self):
        val = self.T()
        while self.lexer.peek()[0] == PLUS:
            self.eat(PLUS)
            val += self.T()
        return val

    # T -> F (* F)*
    def T(self):
        val = self.F()
        while self.lexer.peek()[0] == STAR:
            self.eat(STAR)
            val *= self.F()
        return val

    # F -> ( E ) | NUMBER
    def F(self):
        tok = self.lexer.peek()
        if tok[0] == NUMBER:
            return self.eat(NUMBER)[1]
        elif tok[0] == LPAREN:
            self.eat(LPAREN)
            val = self.E()
            self.eat(RPAREN)
            return val
        else:
            raise Exception(f"Erro sintático: Início de expressão inválido '{tok[1]}'")

def main():
    print("Digite expressões aritméticas (ou 'sair' para fechar).")
    while True:
        try:
            text = input("Entrada > ")
            if text.lower() in ['sair', 'exit']:
                break
            if not text.strip():
                continue
                
            lexer = Lexer(text) # Usa a sua classe Lexer
            parser = ParserOptimized(lexer)
            result = parser.parse()
            
            print(f"Resultado: {result}")
            print("Status: Expressão Correta [cite: 14]") # Confirmação pedida na lista
            
        except Exception as e:
            print(f"ERRO: {e} [cite: 13]") # Tratamento de erro pedido na lista

if __name__ == "__main__":
    main()

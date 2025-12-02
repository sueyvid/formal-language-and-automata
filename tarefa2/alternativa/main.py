# import re

# centenas = ["cem", "duzentos", "trezentos"]

# numero = input("Digite um número de até 6 dígitos separado por ponto, (ex.: xxx.xxx): ")
# if re.search(r'\d{3}.\d{3}', numero):
#     print("Válido")
# else:
#     print("Inválido")
# if not re.search(r'0\d{2}.\d{3}', numero):
#     print(centenas[int(numero[0])-1] + " mil")

import pandas as pd
import re

VS_centena = ["", "Cem", "Duzentos", "Trezentos", "Quatrocentos", "Quinhentos", "Seiscentos", "Setecentos", "Oitocentos", "Novecentos"]

VS = {
    0: [
        "",
        "Cento e",
        "Duzentos e",
        "Trezentos e",
        "Quatrocentos e",
        "Quinhentos e",
        "Seiscentos e",
        "Setecentos e",
        "Oitocentos e",
        "Novecentos e"
    ],
    1: [
        "",
        "",
        "Vinte",
        "Trinta",
        "Quarenta",
        "Cinquenta",
        "Cessenta",
        "Setenta",
        "Oitenta",
        "Noventa"
    ],
    2: [
        "",
        "e Um",
        "e Dois",
        "e Três",
        "e Quatro",
        "e Cinco",
        "e Seis",
        "e Sete",
        "e Oito",
        "e Nove"
    ],
    3: [
        "",
        "Um",
        "Dois",
        "Três",
        "Quatro",
        "Cinco",
        "Seis",
        "Sete",
        "Oito",
        "Nove"
    ],
    4 : [
        "Dez",
        "Onze",
        "Doze",
        "Treze",
        "Quatorze",
        "Quinze",
        "Dezesseis",
        "Dezessete",
        "Dezoito",
        "Dezenove"
    ]
}

filename = "dados/6-digit_FSM.csv"
df = pd.read_csv(filename, header=None)
TE = df.values.tolist()

def processar(valor, estado):
    entrada = valor
    saida = VS[estado][entrada]
    estado = int(TE[entrada][estado])
    return saida, estado

numero = input("Digite um número de até 3 dígitos: ")
resultado = ""
estado = 0
if re.search(r'\d{1}00', numero):
    resultado += VS_centena[int(numero[0])]
else:
    for i in numero:
        saida, estado = processar(int(i), estado)
        if saida:
            resultado += saida + " "
print(resultado)
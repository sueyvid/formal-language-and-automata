import re
from collections import Counter
import tkinter as tk
from tkinter import ttk

def limpar_texto():
    # Obtém texto da caixa de entrada
    texto_original = entrada_texto.get("1.0", tk.END)

    # ====== LIMPEZA COM REGEX ======
    texto_limpo = re.sub(r'https?://\S+', '', texto_original)        # Remove URLs
    texto_limpo = re.sub(r'[@#]\w+', '', texto_limpo)                # Remove hashtags e menções
    texto_limpo = re.sub(r'[^A-Za-zÀ-ÿ0-9\s.,!?]', '', texto_limpo)  # Remove emojis e símbolos
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()           # Remove espaços extras

    # Exibe texto limpo
    saida_texto.delete("1.0", tk.END)
    saida_texto.insert(tk.END, texto_limpo)

    # Conta palavras
    palavras = re.findall(r'\b\w+\b', texto_limpo.lower())
    contagem = Counter(palavras)

    # Exibe palavras mais frequentes
    texto_freq = "Palavras mais frequentes:\n"
    for palavra, freq in contagem.most_common(5):
        texto_freq += f"{palavra}: {freq}\n"

    label_freq.config(text=texto_freq)

# ====== INTERFACE TKINTER ======

janela = tk.Tk()
janela.title("Limpador de Texto com Expressões Regulares")
janela.geometry("950x550")
janela.resizable(False, False)
janela.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(janela, text="🧹 Limpador de Texto com Regex", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

# Frame principal (lado a lado)
frame = tk.Frame(janela, bg="#f0f0f0")
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Caixa de texto original
frame_entrada = tk.Frame(frame)
frame_entrada.pack(side="left", fill="both", expand=True, padx=10)

label_entrada = tk.Label(frame_entrada, text="Texto original:", font=("Helvetica", 12))
label_entrada.pack(anchor="w")

entrada_texto = tk.Text(frame_entrada, wrap="word", width=50, height=20, font=("Helvetica", 11))
entrada_texto.pack(fill="both", expand=True)

# Caixa de texto saída
frame_saida = tk.Frame(frame)
frame_saida.pack(side="left", fill="both", expand=True, padx=10)

label_saida = tk.Label(frame_saida, text="Texto limpo:", font=("Helvetica", 12))
label_saida.pack(anchor="w")

saida_texto = tk.Text(frame_saida, wrap="word", width=50, height=20, font=("Helvetica", 11), bg="#e8f5e9")
saida_texto.pack(fill="both", expand=True)

# Botão para limpar texto
botao_limpar = ttk.Button(janela, text="Limpar texto", command=limpar_texto)
botao_limpar.pack(pady=10)

# Label para exibir frequência de palavras
label_freq = tk.Label(janela, text="", font=("Helvetica", 11), bg="#f0f0f0", justify="left")
label_freq.pack()

# Exemplo inicial
exemplo = """Amei demais esse show!!! 🔥🔥🔥 #forró #SãoJoão
Segue lá: @bandaNordestina 💃
Confira no site: https://www.bandanordestina.com.br 🎶
Foi top demais!!! 😍😍
"""
entrada_texto.insert("1.0", exemplo)

# Inicia a janela
janela.mainloop()

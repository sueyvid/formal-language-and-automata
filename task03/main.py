import re
from collections import Counter

print("=== Limpador de Texto com Expressões Regulares ===")

texto_original = """
Amei demais esse show!!! 🔥🔥🔥 #forró #SãoJoão
Segue lá: @bandaNordestina 💃
Confira no site: https://www.bandanordestina.com.br 🎶
Foi top demais!!! 😍😍
"""

print("📝 Texto original:")
print(texto_original)

# ====== LIMPEZA COM REGEX ======

# 1. Remove URLs
texto_limpo = re.sub(r'https?://\S+', '', texto_original)

# 2. Remove hashtags e menções
texto_limpo = re.sub(r'[@#]\w+', '', texto_limpo)

# 3. Remove emojis e caracteres não alfabéticos (exceto .,!?)
texto_limpo = re.sub(r'[^A-Za-zÀ-ÿ0-9\s.,!?]', '', texto_limpo)

# 4. Remove múltiplos espaços
texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()

print("\n✨ Texto limpo:")
print(texto_limpo)

# ====== ANÁLISE DE PALAVRAS ======
palavras = re.findall(r'\b\w+\b', texto_limpo.lower())
contagem = Counter(palavras)

print("\n📊 Palavras mais frequentes:")
for palavra, freq in contagem.most_common(5):
    print(f"{palavra}: {freq}")

# # ====== TESTE INTERATIVO ======
# print("\n--- Teste Interativo ---")
# entrada = input("Digite um texto com emojis, hashtags ou links: ")

# entrada_limpa = re.sub(r'https?://\S+', '', entrada)
# entrada_limpa = re.sub(r'[@#]\w+', '', entrada_limpa)
# entrada_limpa = re.sub(r'[^A-Za-zÀ-ÿ0-9\s.,!?]', '', entrada_limpa)
# entrada_limpa = re.sub(r'\s+', ' ', entrada_limpa).strip()

# print("\nTexto limpo:")
# print(entrada_limpa)

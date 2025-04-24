import pandas as pd
import random
from itertools import combinations

caminho_dataset = r"C:\Users\Richard\Downloads\teste\dataset_catalogo_streaming.csv"

df = pd.read_csv(caminho_dataset, sep=';', encoding='utf-8')

transacoes = []
for _, row in df.iterrows():
    transacao = set(filter(lambda x: isinstance(x, str) and x.strip() != '', row[1:].values))
    if transacao:
        transacoes.append(transacao)

def gerar_regras(transacoes, suporte_min=0.01, confianca_min=0.02):
    total = len(transacoes)
    suporte_item = {}
    regras = []

    for t in transacoes:
        for item in t:
            item_frozen = frozenset([item])
            suporte_item[item_frozen] = suporte_item.get(item_frozen, 0) + 1
        for par in combinations(t, 2):
            par_set = frozenset(par)
            suporte_item[par_set] = suporte_item.get(par_set, 0) + 1

    for itemset in suporte_item:
        if len(itemset) == 2:
            a, b = list(itemset)
            A, B = frozenset([a]), frozenset([b])
            suporte = suporte_item[itemset] / total

            if suporte >= suporte_min:
                conf_ab = suporte_item[itemset] / suporte_item[A]
                conf_ba = suporte_item[itemset] / suporte_item[B]
                if conf_ab >= confianca_min:
                    regras.append((A, B, suporte, conf_ab))
                if conf_ba >= confianca_min:
                    regras.append((B, A, suporte, conf_ba))

    return regras

regras_apriori = gerar_regras(transacoes)
titulos_unicos = sorted({list(r[0])[0] for r in regras_apriori})

regras_df = pd.DataFrame([
    {"Base": list(A)[0], "Recomendado": list(B)[0], "Suporte": suporte, "Confiança": confianca}
    for A, B, suporte, confianca in regras_apriori
])

regras_df.to_csv(r"C:\Users\Richard\Downloads\teste\regras_apriori_streaming.csv", index=False)

with open(r"C:\Users\Richard\Downloads\teste\titulos_streaming.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(titulos_unicos))

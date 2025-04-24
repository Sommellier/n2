import streamlit as st
import pandas as pd

# Caminhos relativos (funciona tanto local quanto no Streamlit Cloud)
regras_df = pd.read_csv("regras_apriori_streaming.csv")
with open("titulos_streaming.txt", "r", encoding="utf-8") as f:
    titulos = [linha.strip() for linha in f.readlines() if linha.strip()]

st.title("🎬 Sistema de Recomendação de Séries com Apriori")

titulo_escolhido = st.selectbox("Selecione uma série que você assistiu:", titulos)

if st.button("Recomendar"):
    resultados = regras_df[regras_df['Base'] == titulo_escolhido]

    if resultados.empty:
        st.warning("Nenhuma recomendação encontrada para esse título.")
    else:
        resultados = resultados.sort_values(by="Confiança", ascending=False)
        resultados['Suporte'] = resultados['Suporte'].map(lambda x: f"{x:.2%}")
        resultados['Confiança'] = resultados['Confiança'].map(lambda x: f"{x:.2%}")
        st.success(f"Recomendações baseadas em '{titulo_escolhido}':")
        st.table(resultados.reset_index(drop=True))

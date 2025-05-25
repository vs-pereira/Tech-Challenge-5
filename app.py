import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import zipfile
import io
import os

st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que mostra os resultados de clusterização conforme candidatos aprovados")

# 1) Baixar do Drive com gdown (substitua pelo seu ID)
DRIVE_ID = "1IqYZm_6uuanwHy9H0Azfv452K9nQlEWK"
ZIP_PATH = "df_final.zip"
if not os.path.exists(ZIP_PATH):
    url = f"https://drive.google.com/uc?id={DRIVE_ID}"
    gdown.download(url, ZIP_PATH, quiet=False)

# 2) Extrair CSV do ZIP
with zipfile.ZipFile(ZIP_PATH, "r") as z:
    # assume que dentro há 'df_final.csv'
    z.extractall()

# 3) Carregar DataFrame
df = pd.read_csv("df_final.csv

st.write("**Colunas disponíveis no DataFrame:**", df.columns.tolist())
st.stop()  # interrompe a execução aqui para você ver as colunas

# 4) Cálculo Top 10 clusters
cluster_stats = (
    df.groupby('cluster')['is_hired']
      .agg(total_hired='sum', total='count')
)
cluster_stats['pct'] = 100 * cluster_stats.total_hired / cluster_stats.total
top10 = cluster_stats.sort_values('pct', ascending=False) \
                    .head(10) \
                    .reset_index()

# 5) Plot com rótulos
fig = px.bar(
    top10, x='cluster', y='pct', text='pct',
    labels={'cluster':'Cluster','pct':'% Contratados'}
)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# 6) Conclusões
st.subheader("Conclusões Finais")
st.markdown("""
- Priorização de certificações SQL e Linux.  
- Área de Desenvolvimento/Programação em destaque.  
- Inglês básico/intermediário suficiente.  
- 100% têm “outras_certificacoes”.  
""")

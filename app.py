import streamlit as st
import pandas as pd
import plotly.express as px
import requests, zipfile, io

st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que mostra os resultados de clusterização…")

# 1) Baixar e extrair o ZIP do Google Drive
ZIP_URL = "https://drive.google.com/uc?export=download&id=1IqYZm_6uuanwHy9H0Azfv452K9nQlEWK"
r = requests.get(ZIP_URL)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()  # cria df_final.csv na raiz

# 2) Carregar o DataFrame final
df = pd.read_csv("df_final.csv")

# 3) Top 10 Clusters
cluster_stats = (
    df.groupby('cluster')['is_hired']
      .agg(total_hired='sum', total='count')
)
cluster_stats['pct'] = cluster_stats.total_hired / cluster_stats.total * 100
top10 = (
    cluster_stats
    .sort_values('pct', ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top10, x='cluster', y='pct', text='pct',
    labels={'cluster':'Cluster','pct':'% Contratados'}
)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# 4) Conclusões Finais
st.subheader("Conclusões Finais")
st.markdown("""
- Priorização de certificações SQL e Linux.  
- Área de Desenvolvimento/Programação em destaque.  
- Inglês básico/intermediário suficiente.  
- 100% têm “outras_certificacoes”.  
""")

import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import zipfile
import io
import os

st.set_page_config(page_title="Perfis Ideais - Datathon FIAP", layout="wide")
st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown(
    """
    Este app exibe os resultados da clusterização de candidatos e destaca os perfis com maior taxa de contratação.
    """  
)

# --- 1) Baixar e extrair o ZIP do Google Drive ---
DRIVE_ID = "1IqYZm_6uuanwHy9H0Azfv452K9nQlEWK"
ZIP_PATH = "df_final.zip"
if not os.path.exists(ZIP_PATH):
    url = f"https://drive.google.com/uc?id={DRIVE_ID}"
    gdown.download(url, ZIP_PATH, quiet=False)

with zipfile.ZipFile(ZIP_PATH, "r") as z:
    # Extrai o CSV na raiz (df_final.csv)
    z.extractall()

# --- 2) Carregar o DataFrame e verificar colunas ---
df = pd.read_csv("df_final.csv")
st.write("**Colunas carregadas:**", df.columns.tolist())

# Checar se temos as colunas essenciais
if 'cluster' not in df.columns or 'is_hired' not in df.columns:
    st.error(
        "O CSV não contém as colunas obrigatórias **cluster** e/ou **is_hired**.\n\n"
        "- Verifique se você salvou `df_final.csv` **após** executar a clusterização e criar `df['cluster']` e `df['is_hired']` no notebook.\n"
        "- Refaça `df.to_csv('df_final.csv', index=False)` **após** esses passos e re-gere o ZIP."
    )
    st.stop()

# --- 3) Calcular estatísticas dos clusters ---
cluster_stats = (
    df.groupby('cluster')['is_hired']
      .agg(total_hired='sum', total='count')
)
cluster_stats['pct'] = 100 * cluster_stats.total_hired / cluster_stats.total
top10 = (
    cluster_stats
      .sort_values('pct', ascending=False)
      .head(10)
      .reset_index()
)

# --- 4) Plot Top10 Clusters ---
st.subheader("Top 10 Clusters por % de Contratação")
fig = px.bar(
    top10,
    x='cluster',
    y='pct',
    text='pct',
    labels={'cluster':'Cluster','pct':'% Contratação'},
)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(yaxis_title='% de Contratação', xaxis_title='Cluster')
st.plotly_chart(fig, use_container_width=True)

# --- 5) Conclusões Finais ---
st.subheader("Conclusões Finais")
st.markdown("""
1. **Certificações Técnicas**  
   - Destaque para SQL Server, Oracle e Linux.  
2. **Área de Atuação**  
   - Desenvolvimento/Programação lidera, seguido por Projetos e Qualidade/Testes.  
3. **Inglês**  
   - Nível Básico/Intermediário é suficiente para alta taxa de contratação.  
4. **Micro-certificações**  
   - 100% dos candidatos possuem “outras_certificacoes” (workshops, cursos rápidos).  
5. **Próximos Passos**  
   - Incluir variáveis de soft skills.  
   - Refinar parâmetros de clusterização para captar segmentos intermediários.
""")

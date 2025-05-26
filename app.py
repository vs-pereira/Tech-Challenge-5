import streamlit as st
import pandas as pd
import plotly.express as px
import gdown, zipfile, os

# --- 1) Configuração da página ---
st.set_page_config(page_title="Perfis Ideais - Datathon FIAP", layout="wide")
st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que apresenta os resultados da clusterização e perfil dos candidatos com maior taxa de contratação.")

# --- 2) Download e extração do ZIP ---
DRIVE_ID = "17AnJzOfGSymSabFN0kp2l_IxF7j6CmJc"
ZIP_PATH = "df_final2.zip"
CSV_NAME = "df_final.csv"

if not os.path.exists(ZIP_PATH):
    gdown.download(f"https://drive.google.com/uc?id={DRIVE_ID}", ZIP_PATH, quiet=False)

with zipfile.ZipFile(ZIP_PATH, "r") as z:
    z.extractall()

# --- 3) Carregar e validar o DataFrame ---
df = pd.read_csv(CSV_NAME)
if not {'cluster','is_hired'}.issubset(df.columns):
    st.error("O CSV precisa conter as colunas 'cluster' e 'is_hired'.")
    st.stop()

# --- 4) Cálculo das métricas por cluster ---
df['cluster'] = df['cluster'].astype(str)
stats = (
    df.groupby('cluster', as_index=False)
      .agg(total_hired=('is_hired','sum'),
           total=('is_hired','count'))
      .assign(pct=lambda d: 100*d['total_hired']/d['total'])
)

# --- 5) Selecionar Top 10 e definir ordem ---
top10 = stats.sort_values('pct', ascending=False).head(10)
# Ordem invertida para que o maior % fique no topo na barra horizontal
order = top10['cluster'].tolist()[::-1]

# --- 6) Plot horizontal apenas com o Top 10 ---
fig = px.bar(
    top10,
    x='pct',
    y='cluster',
    orientation='h',
    text=top10['pct'].map(lambda v: f"{v:.1f}%"),
    labels={'pct':'% Contratados','cluster':'Cluster'},
    category_orders={'cluster': order}
)

# Forçar o Plotly a usar exatamente essa ordem no eixo Y
fig.update_layout(
    yaxis={'categoryorder':'array', 'categoryarray': order},
    xaxis_title='% de Contratação',
    yaxis_title='Cluster',
    margin=dict(l=80, r=20, t=40, b=40),
    height=500
)

# Estilizar as barras e textos
fig.update_traces(
    marker_color='#4CAF50',
    textposition='outside'
)

st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# 8) Conclusões finais (mantido igual)
st.subheader("Conclusões Finais")
st.markdown("""
**1. Perfil Técnico de Alta Contratação (Cluster 120)**  
  1.1. **Certificações**  
   - SQL Server (MS 70-431) e Oracle (DBA/Solaris) aparecem repetidamente.  
   - Linux LPIC I e ITIL v3 sugerem domínio de infraestrutura.  
  1.2. **Área de Atuação**  
   - Desenvolvimento/Programação é majoritário.  
   - Projetos, Qualidade/Testes e Processos complementam o perfil.  
  1.3. **Inglês**  
   - Básico e Intermediário são suficientes; poucos possuem fluência total.

**2. Importância de Micro-Certificações**  
  - 100 % dos contratados têm “outras_certificacoes” (cursos rápidos, workshops, treinamentos internos).  
  - Isso indica valor decisivo de aprendizado contínuo.

**3. Recomendações para Recrutamento**  
  3.1. **Priorizar** candidatos com certificações formais em bancos de dados e infraestrutura.  
  3.2. **Não exigir** inglês avançado: foco no domínio técnico específico.  
  3.3. **Valorizar** micro-certificações e capacidade de aprendizado acelerado.  

**4. Próximos Passos Analíticos**  
  - Incorporar variáveis de **soft skills** (colaboração, comunicação) para perfis não-técnicos.  
  - Refinar clusterização (ex.: ajustar `min_cluster_size` no HDBSCAN) para descobrir subgrupos relevantes.  
""")

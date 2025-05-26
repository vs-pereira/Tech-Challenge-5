import streamlit as st
import pandas as pd
import plotly.express as px
import gdown, zipfile, os

# Configuração de página
st.set_page_config(page_title="Perfis Ideais - Datathon FIAP", layout="wide")
st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que apresenta os resultados da clusterização e perfil dos candidatos com maior taxa de contratação.")

# 1) Baixar e extrair df_final.csv
DRIVE_ID = "17AnJzOfGSymSabFN0kp2l_IxF7j6CmJc"
ZIP_PATH = "df_final2.zip"
if not os.path.exists(ZIP_PATH):
    gdown.download(f"https://drive.google.com/uc?id={DRIVE_ID}", ZIP_PATH, quiet=False)

with zipfile.ZipFile(ZIP_PATH, "r") as z:
    z.extractall()

# 2) Carregar o DataFrame final
df = pd.read_csv("df_final.csv")

# 3) Validar colunas
if 'cluster' not in df.columns or 'is_hired' not in df.columns:
    st.error("O CSV precisa ter as colunas 'cluster' e 'is_hired'. Gere novamente o df_final.csv após essas colunas existirem.")
    st.stop()

# --- 4) Cálculo das estatísticas por cluster ---
df['cluster'] = df['cluster'].astype(str) 

stats = (
    df
    .groupby('cluster', as_index=False)['is_hired'] 
    .agg(total_hired=('is_hired', 'sum'), total=('is_hired', 'count'))
    .assign(pct=lambda d: 100 * d['total_hired'] / d['total'])
    .sort_values('pct', ascending=False)
)

# --- 5) Selecionar Top 10 (garantindo 10 clusters) ---
top10 = stats.head(10) 
top10_plot = top10.sort_values('pct', ascending=True)

# --- 6) Gráfico com ordem categórica forçada ---
fig = px.bar(
    top10_plot,
    x='pct',
    y='cluster',
    orientation='h',
    text='pct',
    labels={'pct': '% Contratados', 'cluster': 'Cluster'},
    category_orders={'cluster': top10_plot['cluster'].tolist()} 
)

# Ajustar texto e layout
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(
    xaxis_title='% de Contratação',
    yaxis_title='Cluster',
    yaxis={'categoryorder': 'array', 'categoryarray': top10_plot['cluster'].tolist()},
    height=500
)

# --- 7) Exibir no Streamlit ---
st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# 8) Conclusões finais detalhadas
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

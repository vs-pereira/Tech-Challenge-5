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

# --- 5) Selecionar Top 10 e preparar ordem para o gráfico ---
top10 = stats.sort_values('pct', ascending=False).head(10)
order = top10['cluster'].tolist()[::-1]

# --- 6) Plot horizontal do Top 10 ---
fig = px.bar(
    top10,
    x='pct',
    y='cluster',
    orientation='h',
    text=top10['pct'].map(lambda v: f"{v:.1f}%"),
    labels={'pct':'% Contratados','cluster':'Cluster'},
    category_orders={'cluster': order}
)
fig.update_layout(
    yaxis={'categoryorder':'array', 'categoryarray': order},
    xaxis_title='% de Contratação',
    yaxis_title='Cluster',
    margin=dict(l=80, r=20, t=40, b=40),
    height=500
)
fig.update_traces(marker_color='#4CAF50', textposition='outside')

st.subheader("Clusters vs. % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# --- 7) Conclusões finais ---
st.subheader("Conclusões Finais")
st.markdown("""
**1. Perfil Técnico de Alta Contratação (Cluster 120)**  
  - **Certificações**: SQL Server, Oracle, Linux/ITIL.  
  - **Áreas**: Desenvolvimento > Projetos > Testes.  
  - **Inglês**: Básico/Intermediário suficiente.

**2. Micro-certificações**  
  - 100% dos contratados possuem “outras_certificacoes” (cursos rápidos, workshops).

**3. Recomendações**  
  1. Priorização de certificações formais em bancos de dados e infraestrutura.  
  2. Não exigir inglês avançado.  
  3. Valorizar aprendizado contínuo.

**4. Próximos Passos**  
  - Incluir variáveis de soft skills.  
  - Refinar parâmetros de clusterização para subgrupos.
""")

# --- 8) Nova seção: Sobre o Método de Clusterização ---
st.subheader("🔍 Sobre o Método de Clusterização")
st.markdown("""
**O que é clusterização?**  
A clusterização é uma técnica de **aprendizado não supervisionado** que agrupa observações (neste caso, candidatos) com **características semelhantes** em “clusters” (grupos). Em vez de prever um resultado, ela identifica **padrões** e **semelhanças** nos dados por meio de métricas de distância.

**Por que usamos clusterização aqui?**  
- Para **descobrir perfis** de candidatos que se comportam de forma similar durante o processo seletivo.  
- Identificar **segmentos** com **alta taxa de contratação** (Top 10) e contrastá-los com grupos de baixo sucesso.  
- Ajudar o RH a **direcionar** esforços de triagem e entrevistas para perfis mais promissores.

**O que esperávamos atingir?**  
1. **Perfil Ideal**: Mostrar quais combinações de certificações, áreas e níveis de inglês levam a maiores chances de contratação.  
2. **Eficiência**: Reduzir tempo e custo de recrutamento ao focar em candidatos que se encaixam nos clusters de sucesso.  
3. **Insights de Aprendizado**: Enxergar padrões que não seriam óbvios em uma simples análise univariada, como a influência de “outras_certificacoes” no sucesso.

Com essa abordagem, transformamos dados históricos de contratações em **insights acionáveis** para otimizar os processos de seleção.  
""")

import streamlit as st
import pandas as pd
import plotly.express as px
import gdown, zipfile, os
 
st.set_page_config(page_title="Perfis Ideais - Datathon FIAP", layout="wide")
st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que mostra os resultados da clusterização…")

# 1) Baixa e extrai df_final.csv
DRIVE_ID = "17AnJzOfGSymSabFN0kp2l_IxF7j6CmJc"
ZIP_PATH = "df_final2.zip"
if not os.path.exists(ZIP_PATH):
    gdown.download(f"https://drive.google.com/uc?id={DRIVE_ID}", ZIP_PATH, quiet=False)

with zipfile.ZipFile(ZIP_PATH, "r") as z:
    z.extractall()

# 2) Carrega o DataFrame final
df = pd.read_csv("df_final.csv")

# 3) Garante que as colunas existem
if 'cluster' not in df.columns or 'is_hired' not in df.columns:
    st.error("O CSV deve conter as colunas 'cluster' e 'is_hired'.\n"
             "Refaça df.to_csv(...) **após** criar essas colunas no notebook.")
    st.stop()

# 4) Calcula estatísticas e Top10
stats = df.groupby('cluster')['is_hired'].agg(total_hired='sum', total='count')
stats['pct'] = stats.total_hired / stats.total * 100
top10 = stats.sort_values('pct', ascending=False).head(10).reset_index()

# 5) Plota
fig = px.bar(top10, x='cluster', y='pct', text='pct',
             labels={'cluster':'Cluster','pct':'% Contratados'})
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(yaxis_title='% Contratação', xaxis_title='Cluster')
st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

# 6) Conclusões
st.subheader("Conclusões Finais")
st.markdown("""
1. Certificações em SQL e Linux têm alta correlação com contratação.  
2. Vagas de Desenvolvimento/Programação, Projetos e Qualidade lideram as contratações.  
3. Inglês Básico/Intermediário foi suficiente para a maioria.  
4. Todos os contratados possuem “outras_certificacoes” (workshops, cursos rápidos).  
""")

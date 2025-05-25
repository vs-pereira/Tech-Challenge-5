import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Perfis Ideais de Candidatos - Datathon FIAP")
st.markdown("Aplicativo que mostra os resultados de clusterização…")

# Carrega o DataFrame final (faça upload do df_final.csv no Colab)
df = pd.read_csv("df_final.csv")

# Top 10 Clusters
cluster_stats = df.groupby('cluster')['is_hired'] \
                  .agg(total_hired='sum', total='count')
cluster_stats['pct'] = cluster_stats.total_hired/cluster_stats.total*100
top10 = cluster_stats.sort_values('pct', ascending=False).head(10).reset_index()

fig = px.bar(top10, x='cluster', y='pct', text='pct',
             labels={'cluster':'Cluster','pct':'% Contratados'})
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.subheader("Top 10 Clusters por % de Contratação")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Conclusões Finais")
st.markdown("""
- Priorização de certificações SQL e Linux.  
- Área de Desenvolvimento/Programação em destaque.  
- Inglês básico/intermediário suficiente.  
- 100% têm “outras_certificacoes”.  
""")

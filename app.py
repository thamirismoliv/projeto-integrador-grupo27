
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.extracao import baixar_bases
from src.limpeza import limpar_arquivos
from src.kpis import calcular_kpis
from src.transformacao import transformar_dados

@st.cache_data
def carregar_dados():
    baixar_bases()
    limpar_arquivos()
    kpis_dict = calcular_kpis()
    df_tranformacao = transformar_dados()

    return kpis_dict, df_tranformacao

# Carrega os dados
kpis, df_final = carregar_dados()
#configurações da pagina 
st.set_page_config(page_title="Dashboard Olist", layout="wide")

# barra lateral 
st.sidebar.title("Filtros do Projeto")
data_filtro = st.sidebar.date_input("Selecione o Período")
estado_filtro = st.sidebar.multiselect("Selecione o Estado", ["SP", "RJ", "MG", "Outros"])
status_filtro = st.sidebar.selectbox("Status do pedido", ["Entregue", "Cancelado", "Todos"])

# cartoes de metricas
st.title("📊 Análise de E-commerce (Olist)")
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}")
col2.metric("Total de pedidos", f"{kpis['total_pedidos']}")
col3.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}")
col4.metric("Satisfação Média", f"{kpis['nota_media']:.2f} ⭐")

st.markdown("---")

# Gráfico 1: Vendas por Estado
st.header("Vendas por Estado")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(x=kpis['vendas_por_estado'].index, y=kpis['vendas_por_estado'].values, ax=ax1)
ax1.set_title("Vendas por Estado")
ax1.set_xlabel("Estado")
ax1.set_ylabel("Total de pedidos")
st.pyplot(fig1)

# Gráfico 2: Top 10 categorias
st.header("Top 10 Categorias")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=kpis['vendas_por_categoria'], x='total_vendas', y='categoria', ax=ax2)
ax2.set_title("Top 10 Categorias")
ax2.set_xlabel("Total de Vendas")
ax2.set_ylabel("Categoria")
st.pyplot(fig2)

# Gráfico 3: Prazo médio por estado
st.header("Prazo Médio de Entrega por Estado")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(data=kpis['prazo_por_estado'], x='prazo_medio_dias', y='estado', ax=ax3)
ax3.set_title("Prazo Médio de Entrega por Estado")
ax3.set_xlabel("Prazo Médio (dias)")
ax3.set_ylabel("Estado")
st.pyplot(fig3)

# Gráfico 4: Distribuição de avaliações
st.header("Distribuição de Avaliações")
fig4, ax4 = plt.subplots(figsize=(6, 4))
sns.barplot(x=kpis['distribuicao_notas'].index.astype(str), y=kpis['distribuicao_notas'].values, ax=ax4)
ax4.set_title("Distribuição de Notas")
ax4.set_xlabel("Nota")
ax4.set_ylabel("Quantidade")
st.pyplot(fig4)

# Mostra amostra dos dados transformados
st.header("Amostra dos dados transformados")
st.dataframe(df_final.head())

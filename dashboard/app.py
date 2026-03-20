import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    caminho = "data/processed/df_sales_analytics.parquet"
    try:
        return pd.read_parquet(caminho)
    except Exception:
        return None
    
# Carga de dados
df_final = carregar_dados()

#Configuração  da pagina
st.set_page_config(page_title="Dashboard Olist", layout="wide")

# Barra Lateral (Sidebar) 
st.sidebar.title("Filtros do Projeto")
data_filtro = st.sidebar.date_input("Selecione o Período")
estado_filtro = st.sidebar.multiselect("Selecione o Estado", ["SP", "RJ", "MG", "Outros"])
status_filtro = st.sidebar.selectbox("Status do pedido", ["Entregue", "Cancelado", "Todos"])

#Titulo 
st.title("📊 Análise de E-commerce (Olist)")
st.markdown("---")

#Cartoes de Metricas (topo) 

col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", "R$ 0,00")
col2.metric("Total de pedidos", "0")
col3.metric("Ticket Médio", "R$ 0,00")
col4.metric("Satisfação Média", "0.0 ⭐")

st.markdown("---")

#Divisão em abas (Corpo Graficos) 
aba1, aba2, aba3 = st.tabs(["📈 Visão Geral", "🚚 Logística", "💳 Pagamentos"])

with aba1:
    st.header("Vendas ao longo do tempo")
    st.info("Grafico 1 temporal e categorias")

with aba2:
    st.header("Analise de Entrega")
    st.info("Grafico 2 calor e logisticas")

with aba3:
    st.header("Métodos de Pagamento")
    st.info("Grafico 3 distribuição de pagamentos")
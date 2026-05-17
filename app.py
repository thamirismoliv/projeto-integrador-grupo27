import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from src.extracao import baixar_bases
from src.limpeza import limpar_arquivos
from src.kpis import calcular_kpis
from src.transformacao import transformar_dados

st.set_page_config(page_title="Dashboard Olist", layout="wide")


@st.cache_data
def carregar_dados():
    baixar_bases()
    limpar_arquivos()
    kpis_dict = calcular_kpis()
    df_transformacao = transformar_dados()
    return kpis_dict, df_transformacao


kpis, df_final = carregar_dados()

# Sidebar
st.sidebar.title("Filtros do Projeto")
data_filtro = st.sidebar.date_input("Selecione o Período", value=[])
todos_estados = sorted(kpis['vendas_por_estado'].index.tolist())
estado_filtro = st.sidebar.multiselect("Selecione o Estado", todos_estados)
status_filtro = st.sidebar.selectbox("Status do pedido", ["Todos", "Entregue", "Em andamento"])

# Aplicar filtros ao df_final
df_filtrado = df_final.copy()
df_filtrado['order_purchase_timestamp'] = pd.to_datetime(df_filtrado['order_purchase_timestamp'])
df_filtrado['order_delivered_customer_date'] = pd.to_datetime(df_filtrado['order_delivered_customer_date'])

if estado_filtro:
    df_filtrado = df_filtrado[df_filtrado['customer_state'].isin(estado_filtro)]

if isinstance(data_filtro, (list, tuple)) and len(data_filtro) == 2:
    inicio = pd.Timestamp(data_filtro[0])
    fim = pd.Timestamp(data_filtro[1])
    df_filtrado = df_filtrado[df_filtrado['order_purchase_timestamp'].between(inicio, fim)]

if status_filtro == "Entregue":
    df_filtrado = df_filtrado[df_filtrado['order_delivered_customer_date'].notna()]
elif status_filtro == "Em andamento":
    df_filtrado = df_filtrado[df_filtrado['order_delivered_customer_date'].isna()]

# Cards de métricas
st.title("📊 Análise de E-commerce (Olist)")
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}")
col2.metric("Total de Pedidos", f"{kpis['total_pedidos']}")
col3.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}")
col4.metric("Satisfação Média", f"{kpis['nota_media']:.2f} ⭐")

st.markdown("---")

# Gráfico 1: Vendas por mês (linha)
st.header("Vendas por Mês")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(kpis['vendas_por_mes'].index, kpis['vendas_por_mes'].values, marker='o', linewidth=2)
ax1.set_title("Evolução de Vendas Mensais")
ax1.set_xlabel("Mês")
ax1.set_ylabel("Número de Pedidos")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

st.markdown("---")

# Gráfico 2: Vendas por Estado (filtrado)
st.header("Vendas por Estado")
vendas_estado_filtrado = df_filtrado['customer_state'].value_counts()
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(x=vendas_estado_filtrado.index, y=vendas_estado_filtrado.values, ax=ax2)
ax2.set_title("Pedidos por Estado")
ax2.set_xlabel("Estado")
ax2.set_ylabel("Total de Pedidos")
st.pyplot(fig2)

st.markdown("---")

# Gráfico 3: Top 10 categorias (filtrado)
st.header("Top 10 Categorias")
top10_filtrado = (
    df_filtrado['product_category_name']
    .value_counts()
    .head(10)
    .reset_index()
)
top10_filtrado.columns = ['categoria', 'total_vendas']
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top10_filtrado, x='total_vendas', y='categoria', ax=ax3)
ax3.set_title("Top 10 Categorias Mais Vendidas")
ax3.set_xlabel("Total de Vendas")
ax3.set_ylabel("Categoria")
st.pyplot(fig3)

st.markdown("---")

# Gráfico 4: Distribuição de métodos de pagamento (pizza/donut)
st.header("Métodos de Pagamento")
fig4, ax4 = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax4.pie(
    kpis['distribuicao_pagamentos'].values,
    labels=kpis['distribuicao_pagamentos'].index,
    autopct='%1.1f%%',
    wedgeprops=dict(width=0.5),
)
ax4.set_title("Distribuição dos Métodos de Pagamento")
st.pyplot(fig4)

st.markdown("---")

# Gráfico 5: Prazo médio por estado
st.header("Prazo Médio de Entrega por Estado")
fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.barplot(data=kpis['prazo_por_estado'], x='prazo_medio_dias', y='estado', ax=ax5)
ax5.set_title("Prazo Médio de Entrega por Estado")
ax5.set_xlabel("Prazo Médio (dias)")
ax5.set_ylabel("Estado")
st.pyplot(fig5)

st.markdown("---")

# Gráfico 6: Distribuição do tempo de entrega (histograma)
st.header("Distribuição do Tempo de Entrega")
fig6, ax6 = plt.subplots(figsize=(8, 4))
sns.histplot(kpis['tempo_entrega_series'], bins=40, kde=True, ax=ax6)
ax6.set_title("Distribuição do Tempo de Entrega")
ax6.set_xlabel("Dias")
ax6.set_ylabel("Frequência")
st.pyplot(fig6)

st.markdown("---")

# Gráfico 7: Distribuição de avaliações
st.header("Distribuição de Avaliações")
fig7, ax7 = plt.subplots(figsize=(6, 4))
sns.barplot(x=kpis['distribuicao_notas'].index.astype(str), y=kpis['distribuicao_notas'].values, ax=ax7)
ax7.set_title("Distribuição das Notas")
ax7.set_xlabel("Nota")
ax7.set_ylabel("Quantidade")
st.pyplot(fig7)

st.markdown("---")

# Gráfico 8: Scatter — atraso na entrega vs avaliação
st.header("Atraso na Entrega vs Avaliação")
fig8, ax8 = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=kpis['scatter_atraso_avaliacao'],
    x='dias_atraso',
    y='review_score',
    alpha=0.3,
    ax=ax8,
)
ax8.set_title("Atraso na Entrega vs Nota de Avaliação")
ax8.set_xlabel("Dias de Atraso")
ax8.set_ylabel("Nota")
st.pyplot(fig8)

st.markdown("---")

# Gráfico 9: Mapa de calor geográfico
st.header("Concentração de Pedidos por Localização")
fig9 = px.density_mapbox(
    kpis['localizacao_pedidos'],
    lat='lat',
    lon='lng',
    radius=4,
    center={"lat": -14.2, "lon": -51.9},
    zoom=3,
    mapbox_style="open-street-map",
    title="Mapa de Calor — Concentração de Pedidos",
)
st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")

# Amostra dos dados transformados
st.header("Amostra dos Dados Transformados")
st.dataframe(df_filtrado.head())

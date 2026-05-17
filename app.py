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

st.title("📊 Análise de E-commerce (Olist)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Visão Geral", "Vendas", "Logística", "Satisfação", "Geografia"])

# ── Tab 1: Visão Geral ────────────────────────────────────────────────────────
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}")
    col2.metric("Total de Pedidos", f"{kpis['total_pedidos']}")
    col3.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}")
    col4.metric("Satisfação Média", f"{kpis['nota_media']:.2f} ⭐")

    st.subheader("Evolução de Vendas Mensais")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(kpis['vendas_por_mes'].index, kpis['vendas_por_mes'].values, marker='o', linewidth=2)
    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Número de Pedidos")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig1)

# ── Tab 2: Vendas ─────────────────────────────────────────────────────────────
with tab2:
    todos_estados = sorted(kpis['vendas_por_estado'].index.tolist())
    estado_filtro = st.multiselect("Filtrar por Estado", todos_estados)

    df_vendas = df_final.copy()
    if estado_filtro:
        df_vendas = df_vendas[df_vendas['customer_state'].isin(estado_filtro)]

    st.subheader("Pedidos por Estado")
    vendas_estado = df_vendas['customer_state'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=vendas_estado.index, y=vendas_estado.values, ax=ax2)
    ax2.set_xlabel("Estado")
    ax2.set_ylabel("Total de Pedidos")
    st.pyplot(fig2)

    st.subheader("Top 10 Categorias Mais Vendidas")
    top10 = df_vendas['product_category_name'].value_counts().head(10).reset_index()
    top10.columns = ['categoria', 'total_vendas']
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top10, x='total_vendas', y='categoria', ax=ax3)
    ax3.set_xlabel("Total de Vendas")
    ax3.set_ylabel("Categoria")
    st.pyplot(fig3)

    st.subheader("Distribuição dos Métodos de Pagamento")
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(
        kpis['distribuicao_pagamentos'].values,
        labels=kpis['distribuicao_pagamentos'].index,
        autopct='%1.1f%%',
        wedgeprops=dict(width=0.5),
    )
    st.pyplot(fig4)

# ── Tab 3: Logística ──────────────────────────────────────────────────────────
with tab3:
    st.subheader("Prazo Médio de Entrega por Estado")
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=kpis['prazo_por_estado'], x='prazo_medio_dias', y='estado', ax=ax5)
    ax5.set_xlabel("Prazo Médio (dias)")
    ax5.set_ylabel("Estado")
    st.pyplot(fig5)

    st.subheader("Distribuição do Tempo de Entrega")
    fig6, ax6 = plt.subplots(figsize=(8, 4))
    sns.histplot(kpis['tempo_entrega_series'], bins=40, kde=True, ax=ax6)
    ax6.set_xlabel("Dias")
    ax6.set_ylabel("Frequência")
    st.pyplot(fig6)

# ── Tab 4: Satisfação ─────────────────────────────────────────────────────────
with tab4:
    st.subheader("Distribuição das Avaliações")
    fig7, ax7 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=kpis['distribuicao_notas'].index.astype(str), y=kpis['distribuicao_notas'].values, ax=ax7)
    ax7.set_xlabel("Nota")
    ax7.set_ylabel("Quantidade")
    st.pyplot(fig7)

    st.subheader("Atraso na Entrega vs Nota de Avaliação")
    fig8, ax8 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=kpis['scatter_atraso_avaliacao'],
        x='dias_atraso',
        y='review_score',
        alpha=0.3,
        ax=ax8,
    )
    ax8.set_xlabel("Dias de Atraso")
    ax8.set_ylabel("Nota")
    st.pyplot(fig8)

# ── Tab 5: Geografia ──────────────────────────────────────────────────────────
with tab5:
    st.subheader("Concentração de Pedidos por Localização")
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

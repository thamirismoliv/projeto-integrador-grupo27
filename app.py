import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
from pathlib import Path

from src.extracao import baixar_bases
from src.kpis import calcular_kpis
from src.limpeza import limpar_arquivos
from src.transformacao import transformar_dados

st.set_page_config(page_title="Dashboard Olist", layout="wide")


@st.cache_data
def carregar_dados():
    baixar_bases()
    limpar_arquivos()
    df_transformacao = transformar_dados()
    kpis_dict = calcular_kpis()
    return kpis_dict, df_transformacao


kpis, df_final = carregar_dados()

with st.popover("⚙️ Administração"):
    st.warning("Apaga todos os dados e baixa novamente do zero.")
    if st.button("Resetar dados", type="primary"):
        for f in Path("data/raw").glob("*.csv"):
            f.unlink(missing_ok=True)
        for f in Path("data/processed").glob("*.csv"):
            f.unlink(missing_ok=True)
        st.cache_data.clear()
        st.rerun()

st.title("📊 Análise de E-commerce (Olist)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Visão Geral", "Vendas", "Logística", "Satisfação", "Geografia"])

# ── Tab 1: Visão Geral ────────────────────────────────────────────────────────
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faturamento Total", f"R$ {kpis['faturamento_total']:,.2f}", help="Soma de todos os pagamentos recebidos. Ver detalhes na aba Vendas.")
    col2.metric("Total de Pedidos", f"{kpis['total_pedidos']}", help="Número de pedidos únicos. Ver detalhes na aba Vendas.")
    col3.metric("Ticket Médio", f"R$ {kpis['ticket_medio']:,.2f}", help="Valor médio gasto por pedido (faturamento ÷ pedidos). Ver detalhes na aba Vendas.")
    col4.metric("Satisfação Média", f"{kpis['nota_media']:.2f} ⭐", help="Média das avaliações dos clientes (1–5 estrelas). Ver detalhes na aba Satisfação.")

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

    log_escala = st.checkbox("Escala logarítmica")

    with st.expander("Pedidos por Estado", expanded=False):
        vendas_estado = df_vendas.drop_duplicates(subset='order_id')['customer_state'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.barplot(x=vendas_estado.index, y=vendas_estado.values, ax=ax2)
        ax2.set_xlabel("Estado")
        ax2.set_ylabel("Total de Pedidos")
        if log_escala:
            ax2.set_yscale('log')
        st.pyplot(fig2)

    with st.expander("Faturamento por Estado", expanded=False):
        faturamento_estado = df_vendas.groupby('customer_state')['valor_total'].sum().sort_values(ascending=False)
        fig2b, ax2b = plt.subplots(figsize=(10, 4))
        sns.barplot(x=faturamento_estado.index, y=faturamento_estado.values, ax=ax2b)
        ax2b.yaxis.set_major_formatter('{x:,.0f}')
        ax2b.set_xlabel("Estado")
        ax2b.set_ylabel("Faturamento (R$)")
        if log_escala:
            ax2b.set_yscale('log')
        st.pyplot(fig2b)

    with st.expander("Top 10 Categorias Mais Vendidas", expanded=False):
        top10 = df_vendas['product_category_name'].value_counts().head(10).reset_index()
        top10.columns = ['categoria', 'total_vendas']
        top10['categoria'] = top10['categoria'].str.replace('_', ' ').str.title()
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top10, x='total_vendas', y='categoria', ax=ax3)
        ax3.set_xlabel("Total de Vendas")
        ax3.set_ylabel("Categoria")
        st.pyplot(fig3)

    with st.expander("Distribuição dos Métodos de Pagamento", expanded=False):
        pag = kpis['pagamentos_detalhado']
        if estado_filtro:
            pag = pag[pag['customer_state'].isin(estado_filtro)]
        dist_pag = pag['payment_type'].value_counts()
        dist_pag.index = dist_pag.index.str.replace('_', ' ').str.title()
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        ax4.pie(
            dist_pag.values,
            labels=dist_pag.index,
            autopct='%1.1f%%',
            wedgeprops=dict(width=0.5),
        )
        st.pyplot(fig4)

# ── Tab 3: Logística ──────────────────────────────────────────────────────────
with tab3:
    col1, col2, col3 = st.columns(3)
    col1.metric("Prazo Médio de Entrega", f"{kpis['prazo_medio']:.1f} dias", help="Média de dias entre a compra e a entrega ao cliente.")
    col2.metric("Pedidos Atrasados", f"{kpis['perc_atraso']:.1f}%", help="Percentual de pedidos entregues após o prazo estimado.")
    col3.metric("Tempo Médio de Atraso", f"{kpis['tempo_medio_atraso']:.1f} dias", help="Média de dias de atraso considerando apenas os pedidos que atrasaram.")

    with st.expander("Prazo Médio de Entrega por Estado", expanded=False):
        fig5, ax5 = plt.subplots(figsize=(8, 6))
        sns.barplot(data=kpis['prazo_por_estado'], x='prazo_medio_dias', y='estado', ax=ax5)
        ax5.set_xlabel("Prazo Médio (dias)")
        ax5.set_ylabel("Estado")
        st.pyplot(fig5)

    with st.expander("Distribuição do Tempo de Entrega", expanded=False):
        p99 = kpis['tempo_entrega_series'].quantile(0.99)
        fig6, ax6 = plt.subplots(figsize=(8, 4))
        sns.histplot(kpis['tempo_entrega_series'], bins=40, kde=True, ax=ax6)
        ax6.set_xlim(0, p99)
        ax6.set_xlabel("Dias")
        ax6.set_ylabel("Frequência")
        st.pyplot(fig6)

# ── Tab 4: Satisfação ─────────────────────────────────────────────────────────
with tab4:
    col1, col2 = st.columns(2)
    col1.metric("Nota Média (No Prazo)", f"{kpis['media_nota_no_prazo']:.2f} ⭐", help="Média das avaliações de pedidos entregues dentro do prazo estimado.")
    col2.metric("Nota Média (Atrasados)", f"{kpis['media_nota_atrasado']:.2f} ⭐", help="Média das avaliações de pedidos entregues com atraso.")

    with st.expander("Distribuição das Avaliações", expanded=False):
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        sns.barplot(x=kpis['distribuicao_notas'].index.astype(str), y=kpis['distribuicao_notas'].values, ax=ax7)
        ax7.set_xlabel("Nota")
        ax7.set_ylabel("Quantidade")
        st.pyplot(fig7)

    with st.expander("Atraso de Entrega por Nota de Avaliação", expanded=False):
        fig8, ax8 = plt.subplots(figsize=(8, 5))
        sns.boxplot(
            data=kpis['scatter_atraso_avaliacao'],
            x='review_score',
            y='dias_atraso',
            ax=ax8,
        )
        ax8.axhline(0, color='red', linestyle='--', linewidth=1)
        ax8.set_ylim(-60, 60)
        ax8.set_xlabel("Nota de Avaliação (estrelas)")
        ax8.set_ylabel("Dias em Relação ao Prazo Estimado")
        st.pyplot(fig8)

    with st.expander("Distribuição Geral do Atraso de Entrega", expanded=False):
        fig8b, ax8b = plt.subplots(figsize=(8, 3))
        sns.boxplot(x=kpis['scatter_atraso_avaliacao']['dias_atraso'], ax=ax8b)
        ax8b.axvline(0, color='red', linestyle='--', linewidth=1)
        ax8b.set_xlabel("Dias em Relação ao Prazo Estimado  (negativo = antecipado  |  positivo = atrasado)")
        st.pyplot(fig8b)

# ── Tab 5: Geografia ──────────────────────────────────────────────────────────
with tab5:
    st.subheader("Concentração de Pedidos por Localização")
    fig9 = px.density_map(
        kpis['localizacao_pedidos'],
        lat='lat',
        lon='lng',
        radius=4,
        center={"lat": -14.2, "lon": -51.9},
        zoom=3,
        map_style="open-street-map",
        title="Mapa de Calor — Concentração de Pedidos",
    )
    fig9.update_layout(height=800)
    st.plotly_chart(fig9, width='stretch')

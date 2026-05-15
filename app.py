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


# Carga de dados
kpis, df_final = carregar_dados()

# Configuração  da pagina
st.set_page_config(page_title="Dashboard Olist", layout="wide")

# Barra Lateral  
st.sidebar.title("Filtros do Projeto")
data_filtro = st.sidebar.date_input("Selecione o Período")
estado_filtro = st.sidebar.multiselect("Selecione o Estado", ["SP", "RJ", "MG", "Outros"])
status_filtro = st.sidebar.selectbox("Status do pedido", ["Entregue", "Cancelado", "Todos"])

# Titulo
st.title("📊 Análise de E-commerce (Olist)")
st.markdown("---")

# Cartoes de Metricas (topo)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", f"{kpis['faturamento_total']:.2f}")
col2.metric("Total de pedidos", "0")
col3.metric("Ticket Médio", "R$ 0,00")
col4.metric("Satisfação Média", "0.0 ⭐")

st.markdown("---")

# Divisão em abas (Corpo Graficos)
aba1, aba2, aba3 = st.tabs(["📈 Visão Geral", "🚚 Logística", "💳 Pagamentos"])

with aba1:
    st.title('Título do Gráfico de Linha')
    st.header("Vendas ao longo do tempo")
    
    eixo_x = [1, 2, 3, 4, 5]
    eixo_y = [10, 20, 15, 25, 30]
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(eixo_x, eixo_y, marker='o', linestyle='-', color='b', label='Tendência')
    ax1.set_xlabel('Eixo X (Tempo/Categorias)')
    ax1.set_ylabel('Eixo Y (Valores)')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)
    
    st.markdown("<p style='text-align: center;'>Grafico 1 temporal e categorias</p>", unsafe_allow_html=True)

with aba2:
    st.title('Distribuição Percentual')
    st.header("Analise de Entrega")
    
    valores = [25, 35, 20, 20]
    categorias = ['Acessórios', 'Roupas', 'Eletrônicos', 'Beleza']
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140, wedgeprops={'width': 0.4})
    st.pyplot(fig2)
    
    st.markdown("<p style='text-align: center;'>Grafico 2 calor e logisticas</p>", unsafe_allow_html=True)

with aba3:
    st.title('Comparativo de Categorias')
    st.header("Métodos de Pagamento")
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.bar(categorias, valores, color='skyblue')
    ax3.set_xlabel('Categorias')
    ax3.set_ylabel('Valores')
    st.pyplot(fig3)
    
    st.markdown("<p style='text-align: center;'>Grafico 3 distribuição de pagamentos</p>", unsafe_allow_html=True)

#Grafico 4
# Definindo os dados usados no histograma e boxplot
# Substitua por seus dados reais, por exemplo uma coluna do DataFrame
dados = [12, 15, 14, 20, 18, 22, 17, 16, 19, 21, 25, 30, 28, 14, 13, 18, 20, 23, 19, 17]

# Histograma
plt.figure(figsize=(10, 5))
sns.histplot(dados, kde=True, color='green')
plt.title('Distribuição de Frequência (Histograma)')
plt.show()

# Boxplot
plt.figure(figsize=(10, 5))
sns.boxplot(x=dados, color='lightcoral')
plt.title('Análise de Outliers (Boxplot)')
plt.show()

#Grafico 5
# Definindo dados_matriz para o heatmap (correlação entre variáveis numéricas)
# Usando tabela_final se disponível, senão dados de exemplo
if 'tabela_final' in globals():
    # Adicionando coluna dias_entrega_num se não existir
    if 'dias_entrega_num' not in tabela_final.columns:
        tabela_final['dias_entrega_num'] = (tabela_final['order_delivered_customer_date'] - 
                                            tabela_final['order_purchase_timestamp']).dt.days
    dados_matriz = tabela_final[['price', 'freight_value', 'valor_total', 'dias_entrega_num']].corr()
else:
    # Dados de exemplo se tabela_final não estiver definida
    dados_matriz = pd.DataFrame({
        'price': [1, 0.8, 0.9, 0.2],
        'freight_value': [0.8, 1, 0.7, 0.3],
        'valor_total': [0.9, 0.7, 1, 0.1],
        'dias_entrega_num': [0.2, 0.3, 0.1, 1]
    })

plt.figure(figsize=(12, 8))
sns.heatmap(dados_matriz, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Mapa de Calor de Correlação')
plt.show()

#Grafico 6
plt.figure(figsize=(10, 6))
plt.scatter(eixo_x, eixo_y, alpha=0.5, c='purple')
plt.title('Dispersão: Variável X vs Variável Y')
plt.xlabel('Variável X')
plt.ylabel('Variável Y')
plt.show()

#Grafico 7
dados_matriz = [
    [1, 0.5, 0.3],
    [0.5, 1, 0.2],
    [0.3, 0.2, 1]
]
sns.heatmap(dados_matriz, annot=True, cmap='coolwarm', fmt='.2f')

plt.figure(figsize=(12, 8))
# 'df.corr()' calcula a correlação automaticamente se usar Pandas
sns.heatmap(dados_matriz, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Mapa de Calor de Correlação')
plt.show()

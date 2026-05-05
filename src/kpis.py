import pandas as pd

# CARREGANDO TODOS OS DADOS LIMPOS

df_pedidos = pd.read_csv('data/processed/olist_orders_dataset.csv')
df_pagamentos = pd.read_csv('data/processed/olist_order_payments_dataset.csv')
df_avaliacoes = pd.read_csv('data/processed/olist_order_reviews_dataset.csv')
df_clientes = pd.read_csv('data/processed/olist_customers_dataset.csv')
df_itens = pd.read_csv('data/processed/olist_order_items_dataset.csv')
df_produtos = pd.read_csv('data/processed/olist_products_dataset.csv')

# Tratando as colunas de datas para que o Python entenda que são dias e horas
df_pedidos['order_purchase_timestamp'] = pd.to_datetime(df_pedidos['order_purchase_timestamp'])
df_pedidos['order_delivered_customer_date'] = pd.to_datetime(df_pedidos['order_delivered_customer_date'])
df_pedidos['order_estimated_delivery_date'] = pd.to_datetime(df_pedidos['order_estimated_delivery_date'])


print("--- MÉTRICAS DE VENDAS ---")

faturamento_total = df_pagamentos['payment_value'].sum()
total_pedidos = df_pedidos['order_id'].nunique()
ticket_medio = faturamento_total / total_pedidos

print(f"1. Faturamento Total: R$ {faturamento_total:,.2f}")
print(f"2. Número Total de Pedidos: {total_pedidos}")
print(f"3. Ticket Médio: R$ {ticket_medio:,.2f}")

# Vendas por região (estado)
df_pedidos_clientes = pd.merge(df_pedidos, df_clientes, on='customer_id')
vendas_por_estado = df_pedidos_clientes['customer_state'].value_counts()
print(f"\n4. Vendas por Estado (Top 5):\n{vendas_por_estado.head(5)}")


print("\n--- ANÁLISE DE PRODUTOS ---")

# Juntar as tabelas de itens e produtos para ver as categorias
df_vendas_produtos = pd.merge(df_itens, df_produtos, on='product_id')
top_10_categorias = df_vendas_produtos['product_category_name'].value_counts().head(10)

print(f"Top 10 Categorias Mais Vendidas:\n{top_10_categorias}")


print("\n--- MÉTRICAS LOGÍSTICAS ---")

# Prazo médio de entrega (data de entrega menos a data de compra)
df_pedidos['tempo_entrega_dias'] = (df_pedidos['order_delivered_customer_date'] - df_pedidos['order_purchase_timestamp']).dt.days
prazo_medio = df_pedidos['tempo_entrega_dias'].mean()

# Percentual de entregas atrasadas
df_pedidos['atrasado'] = df_pedidos['order_delivered_customer_date'] > df_pedidos['order_estimated_delivery_date']
perc_atraso = (df_pedidos['atrasado'].sum() / len(df_pedidos.dropna(subset=['order_delivered_customer_date']))) * 100

print(f"1. Prazo Médio de Entrega: {prazo_medio:.1f} dias")
print(f"2. Percentual de Entregas Atrasadas: {perc_atraso:.2f}%")


print("\n--- MÉTRICAS DE SATISFAÇÃO DO CLIENTE ---")

# Nota média de avaliação
nota_media = df_avaliacoes['review_score'].mean()
print(f"1. Nota Média de Avaliação: {nota_media:.2f} estrelas")

# Distribuição das avaliações (1–5 estrelas)
distribuicao_notas = df_avaliacoes['review_score'].value_counts().sort_index(ascending=False)
print(f"\n2. Distribuição das Avaliações:\n{distribuicao_notas}")

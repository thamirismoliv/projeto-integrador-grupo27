import pandas as pd


def calcular_kpis():
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

    df_entregues = df_pedidos.dropna(subset=["order_delivered_customer_date"]).copy()

    # Métricas de vendas

    faturamento_total = df_pagamentos['payment_value'].sum()
    total_pedidos = df_pedidos['order_id'].nunique()
    ticket_medio = faturamento_total / total_pedidos

    # Vendas por região (estado)
    df_pedidos_clientes = pd.merge(df_pedidos, df_clientes, on='customer_id')
    vendas_por_estado = df_pedidos_clientes['customer_state'].value_counts()

    # Juntar as tabelas de itens e produtos para ver as categorias
    df_vendas_produtos = pd.merge(df_itens, df_produtos, on='product_id')
    top_10_categorias = df_vendas_produtos['product_category_name'].value_counts().head(10).reset_index()
    top_10_categorias.columns = ["categoria", "total_vendas"]

    # Metricas Logisticas
    # Prazo médio de entrega (data de entrega menos a data de compra)
    df_entregues["tempo_entrega_dias"] = (
            df_entregues["order_delivered_customer_date"] - df_entregues["order_purchase_timestamp"]
    ).dt.days
    prazo_medio = df_entregues["tempo_entrega_dias"].mean()

    # Percentual de entregas atrasadas
    df_entregues["atrasado"] = (
            df_entregues["order_delivered_customer_date"] > df_entregues["order_estimated_delivery_date"]
    )
    perc_atraso = (df_entregues["atrasado"].sum() / len(df_entregues)) * 100

    # Tempo médio de atraso (apenas os pedidos que atrasaram)
    df_atrasados = df_entregues[df_entregues["atrasado"]].copy()
    df_atrasados["dias_atraso"] = (
            df_atrasados["order_delivered_customer_date"] - df_atrasados["order_estimated_delivery_date"]
    ).dt.days
    tempo_medio_atraso = df_atrasados["dias_atraso"].mean()

    # Prazo médio de entrega por estado
    df_entregues_clientes = pd.merge(df_entregues, df_clientes, on="customer_id")
    prazo_por_estado = (
        df_entregues_clientes.groupby("customer_state")["tempo_entrega_dias"]
        .mean()
        .round(1)
        .reset_index()
    )
    prazo_por_estado.columns = ["estado", "prazo_medio_dias"]
    prazo_por_estado = prazo_por_estado.sort_values("prazo_medio_dias", ascending=False)

    # Metricas de satisfação do cliente
    # Nota média de avaliação
    nota_media = df_avaliacoes['review_score'].mean()

    # Distribuição das avaliações (1–5 estrelas)
    distribuicao_notas = df_avaliacoes['review_score'].value_counts().sort_index(ascending=False)

    # Relação entre atraso na entrega e avaliação
    df_atraso_avaliacao = pd.merge(
        df_entregues[["order_id", "atrasado"]],
        df_avaliacoes[["order_id", "review_score"]],
        on="order_id"
    )

    df_atraso_avaliacao = pd.merge(
        df_atraso_avaliacao,
        df_atrasados[["order_id", "dias_atraso"]],
        on="order_id",
        how="left"
    )

    media_nota_no_prazo = df_atraso_avaliacao[~df_atraso_avaliacao["atrasado"]]["review_score"].mean()
    media_nota_atrasado = df_atraso_avaliacao[df_atraso_avaliacao["atrasado"]]["review_score"].mean()

    return {
        # Vendas
        "faturamento_total": faturamento_total,
        "total_pedidos": total_pedidos,
        "ticket_medio": ticket_medio,
        "vendas_por_estado": vendas_por_estado,
        "vendas_por_categoria": top_10_categorias,

        # Logística
        "prazo_medio": prazo_medio,
        "perc_atraso": perc_atraso,
        "tempo_medio_atraso": tempo_medio_atraso,
        "prazo_por_estado": prazo_por_estado,

        # Satisfação
        "nota_media": nota_media,
        "distribuicao_notas": distribuicao_notas,
        "media_nota_no_prazo": media_nota_no_prazo,
        "media_nota_atrasado": media_nota_atrasado,
    }


if __name__ == "__main__":
    kpis = calcular_kpis()

    print("--- MÉTRICAS DE VENDAS ---")
    print(f"Faturamento Total:     R$ {kpis['faturamento_total']:,.2f}")
    print(f"Total de Pedidos:      {kpis['total_pedidos']}")
    print(f"Ticket Médio:          R$ {kpis['ticket_medio']:,.2f}")
    print(f"\nTop 5 estados:\n{kpis['vendas_por_estado'].head(5).to_string(index=False)}")
    print(f"\nTop 10 categorias:\n{kpis['vendas_por_categoria'].to_string(index=False)}")

    print("\n--- MÉTRICAS LOGÍSTICAS ---")
    print(f"Prazo Médio de Entrega:      {kpis['prazo_medio']:.1f} dias")
    print(f"Entregas Atrasadas:          {kpis['perc_atraso']:.2f}%")
    print(f"Tempo Médio de Atraso:       {kpis['tempo_medio_atraso']:.1f} dias")
    print(f"\nPrazo médio por estado:\n{kpis['prazo_por_estado'].to_string(index=False)}")

    print("\n--- MÉTRICAS DE SATISFAÇÃO ---")
    print(f"Nota Média:                  {kpis['nota_media']:.2f} estrelas")
    print(f"Nota média (no prazo):       {kpis['media_nota_no_prazo']:.2f} estrelas")
    print(f"Nota média (atrasados):      {kpis['media_nota_atrasado']:.2f} estrelas")
    print(f"\nDistribuição:\n{kpis['distribuicao_notas'].to_string()}")

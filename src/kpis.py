import pandas as pd


def calcular_kpis():
    df_pedidos = pd.read_csv('data/processed/olist_orders_dataset.csv')
    df_pagamentos = pd.read_csv('data/processed/olist_order_payments_dataset.csv')
    df_avaliacoes = pd.read_csv('data/processed/olist_order_reviews_dataset.csv')
    df_clientes = pd.read_csv('data/processed/olist_customers_dataset.csv')
    df_itens = pd.read_csv('data/processed/olist_order_items_dataset.csv')
    df_produtos = pd.read_csv('data/processed/olist_products_dataset.csv')
    df_geolocalizacao = pd.read_csv('data/processed/olist_geolocation_dataset.csv')

    df_pedidos['order_purchase_timestamp'] = pd.to_datetime(df_pedidos['order_purchase_timestamp'])
    df_pedidos['order_delivered_customer_date'] = pd.to_datetime(df_pedidos['order_delivered_customer_date'])
    df_pedidos['order_estimated_delivery_date'] = pd.to_datetime(df_pedidos['order_estimated_delivery_date'])

    df_entregues = df_pedidos.dropna(subset=["order_delivered_customer_date"]).copy()

    # Métricas de vendas
    faturamento_total = df_pagamentos['payment_value'].sum()
    total_pedidos = df_pedidos['order_id'].nunique()
    ticket_medio = faturamento_total / total_pedidos

    df_pedidos_clientes = pd.merge(df_pedidos, df_clientes, on='customer_id')
    vendas_por_estado = df_pedidos_clientes['customer_state'].value_counts()

    df_vendas_produtos = pd.merge(df_itens, df_produtos, on='product_id')
    top_10_categorias = df_vendas_produtos['product_category_name'].value_counts().head(10).reset_index()
    top_10_categorias.columns = ["categoria", "total_vendas"]

    # Vendas por mês
    df_pedidos['mes'] = df_pedidos['order_purchase_timestamp'].dt.to_period('M').astype(str)
    vendas_por_mes = df_pedidos.groupby('mes')['order_id'].count().sort_index()

    # Distribuição de métodos de pagamento
    distribuicao_pagamentos = df_pagamentos['payment_type'].value_counts()

    # Métricas logísticas
    df_entregues["tempo_entrega_dias"] = (
        df_entregues["order_delivered_customer_date"] - df_entregues["order_purchase_timestamp"]
    ).dt.days
    prazo_medio = df_entregues["tempo_entrega_dias"].mean()

    df_entregues["atrasado"] = (
        df_entregues["order_delivered_customer_date"] > df_entregues["order_estimated_delivery_date"]
    )
    perc_atraso = (df_entregues["atrasado"].sum() / len(df_entregues)) * 100

    df_atrasados = df_entregues[df_entregues["atrasado"]].copy()
    df_atrasados["dias_atraso"] = (
        df_atrasados["order_delivered_customer_date"] - df_atrasados["order_estimated_delivery_date"]
    ).dt.days
    tempo_medio_atraso = df_atrasados["dias_atraso"].mean()

    df_entregues_clientes = pd.merge(df_entregues, df_clientes, on="customer_id")
    prazo_por_estado = (
        df_entregues_clientes.groupby("customer_state")["tempo_entrega_dias"]
        .mean()
        .round(1)
        .reset_index()
    )
    prazo_por_estado.columns = ["estado", "prazo_medio_dias"]
    prazo_por_estado = prazo_por_estado.sort_values("prazo_medio_dias", ascending=False)

    # Série de tempo de entrega para histograma
    tempo_entrega_series = df_entregues["tempo_entrega_dias"]

    # Métricas de satisfação
    nota_media = df_avaliacoes['review_score'].mean()
    distribuicao_notas = df_avaliacoes['review_score'].value_counts().sort_index(ascending=False)

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

    # Scatter: dias de atraso × avaliação (apenas pedidos atrasados)
    scatter_atraso_avaliacao = pd.merge(
        df_atrasados[["order_id", "dias_atraso"]],
        df_avaliacoes[["order_id", "review_score"]],
        on="order_id"
    )[["dias_atraso", "review_score"]]

    # Localização dos pedidos para mapa de calor
    geo_por_cep = (
        df_geolocalizacao
        .groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']]
        .first()
        .reset_index()
    )
    df_pedidos_geo = pd.merge(
        df_pedidos_clientes,
        geo_por_cep,
        left_on='customer_zip_code_prefix',
        right_on='geolocation_zip_code_prefix',
        how='inner'
    )
    localizacao_pedidos = df_pedidos_geo[['geolocation_lat', 'geolocation_lng']].rename(
        columns={'geolocation_lat': 'lat', 'geolocation_lng': 'lng'}
    )

    return {
        # Vendas
        "faturamento_total": faturamento_total,
        "total_pedidos": total_pedidos,
        "ticket_medio": ticket_medio,
        "vendas_por_estado": vendas_por_estado,
        "vendas_por_categoria": top_10_categorias,
        "vendas_por_mes": vendas_por_mes,
        "distribuicao_pagamentos": distribuicao_pagamentos,

        # Logística
        "prazo_medio": prazo_medio,
        "perc_atraso": perc_atraso,
        "tempo_medio_atraso": tempo_medio_atraso,
        "prazo_por_estado": prazo_por_estado,
        "tempo_entrega_series": tempo_entrega_series,

        # Satisfação
        "nota_media": nota_media,
        "distribuicao_notas": distribuicao_notas,
        "media_nota_no_prazo": media_nota_no_prazo,
        "media_nota_atrasado": media_nota_atrasado,
        "scatter_atraso_avaliacao": scatter_atraso_avaliacao,

        # Geografia
        "localizacao_pedidos": localizacao_pedidos,
    }


if __name__ == "__main__":
    kpis = calcular_kpis()

    print("--- MÉTRICAS DE VENDAS ---")
    print(f"Faturamento Total:     R$ {kpis['faturamento_total']:,.2f}")
    print(f"Total de Pedidos:      {kpis['total_pedidos']}")
    print(f"Ticket Médio:          R$ {kpis['ticket_medio']:,.2f}")
    print(f"\nTop 5 estados:\n{kpis['vendas_por_estado'].head(5).to_string()}")
    print(f"\nTop 10 categorias:\n{kpis['vendas_por_categoria'].to_string(index=False)}")
    print(f"\nVendas por mês (últimos 5):\n{kpis['vendas_por_mes'].tail(5).to_string()}")
    print(f"\nMétodos de pagamento:\n{kpis['distribuicao_pagamentos'].to_string()}")

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
    print(f"\nScatter (primeiras linhas):\n{kpis['scatter_atraso_avaliacao'].head().to_string(index=False)}")

    print(f"\n--- GEOGRAFIA ---")
    print(f"Pedidos com localização: {len(kpis['localizacao_pedidos'])}")

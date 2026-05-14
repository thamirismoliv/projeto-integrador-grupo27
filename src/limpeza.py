import os
import pandas as pd


def limpar_arquivos():
    arquivos = [
        "data/raw/olist_orders_dataset.csv",
        "data/raw/olist_order_items_dataset.csv",
        "data/raw/olist_order_payments_dataset.csv",
        "data/raw/olist_order_reviews_dataset.csv",
        "data/raw/olist_products_dataset.csv",
        "data/raw/olist_customers_dataset.csv",
        "data/raw/olist_geolocation_dataset.csv"
    ]

    colunas_data = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "shipping_limit_date"
    ]

    os.makedirs("data/processed", exist_ok=True)

    for arquivo in arquivos:
        print(f"Lendo: {arquivo}")
        df = pd.read_csv(arquivo)

        # Converter datas
        for coluna in colunas_data:
            if coluna in df.columns:
                df[coluna] = pd.to_datetime(df[coluna], errors="coerce")

        # Tratar pedidos cancelados e indisponíveis
        if "order_status" in df.columns:
            df = df[
                (df["order_status"] != "canceled") &
                (df["order_status"] != "unavailable")
                ]

        # Tratar valores nulos específicos:
        # pedidos sem avaliação são atribuídos o valor medio
        if "review_score" in df.columns:
            media = df["review_score"].mean()
            df["review_score"] = df["review_score"].fillna(media)

        # pedidos sem categoria são atribuídos valor "sem_categoria"
        if "product_category_name" in df.columns:
            df["product_category_name"] = df["product_category_name"].fillna("sem_categoria")

        # Remover linhas com muitos valores nulos
        df = df.dropna()

        # Remover duplicados
        df = df.drop_duplicates()

        nome_arquivo = arquivo.split("/")[-1]
        print(f"Salvando: data/processed/{nome_arquivo}")
        df.to_csv(f"data/processed/{nome_arquivo}", index=False)
        print("----------------------------------")

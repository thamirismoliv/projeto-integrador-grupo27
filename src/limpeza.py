from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")

PROCESSED_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
]

COLUNAS_DATA = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date",
]

DROPNA_SUBSET = {
    "olist_orders_dataset.csv":          ["order_id", "customer_id"],
    "olist_order_items_dataset.csv":     ["order_id", "product_id"],
    "olist_order_payments_dataset.csv":  ["order_id", "payment_value"],
    "olist_order_reviews_dataset.csv":   ["order_id"],
    "olist_products_dataset.csv":        ["product_id"],
    "olist_customers_dataset.csv":       ["customer_id"],
    "olist_geolocation_dataset.csv":     [],
}

DEMAIS_ARQUIVOS = [
    "data/raw/olist_order_items_dataset.csv",
    "data/raw/olist_order_payments_dataset.csv",
    "data/raw/olist_order_reviews_dataset.csv",
    "data/raw/olist_products_dataset.csv",
    "data/raw/olist_customers_dataset.csv",
    "data/raw/olist_geolocation_dataset.csv",
]


def _converter_datas(df):
    for col in COLUNAS_DATA:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def _limpar_arquivo(df, nome_arquivo, valid_order_ids=None):
    df = _converter_datas(df)

    if "review_score" in df.columns:
        df["review_score"] = df["review_score"].fillna(df["review_score"].mean())

    if "product_category_name" in df.columns:
        df["product_category_name"] = df["product_category_name"].fillna("sem_categoria")

    if valid_order_ids is not None and "order_id" in df.columns:
        df = df[df["order_id"].isin(valid_order_ids)]

    subset = DROPNA_SUBSET.get(nome_arquivo, [])
    if subset:
        df = df.dropna(subset=subset)

    return df.drop_duplicates()


def limpar_arquivos():
    if all((PROCESSED_DIR / f).exists() for f in PROCESSED_FILES):
        print("Arquivos processados já existem. Pulando limpeza.")
        return

    tabela_mestra = PROCESSED_DIR / "tabela_mestra.csv"
    if tabela_mestra.exists():
        tabela_mestra.unlink()

    import os
    os.makedirs("data/processed", exist_ok=True)

    # Etapa A: processar orders primeiro para extrair valid_order_ids
    print("Lendo: data/raw/olist_orders_dataset.csv")
    df_orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
    df_orders = _converter_datas(df_orders)
    df_orders = df_orders[
        ~df_orders["order_status"].isin(["canceled", "unavailable"])
    ]
    df_orders = df_orders.dropna(subset=["order_id", "customer_id"]).drop_duplicates()
    valid_order_ids = set(df_orders["order_id"])
    df_orders.to_csv("data/processed/olist_orders_dataset.csv", index=False)
    print(f"Salvando: data/processed/olist_orders_dataset.csv ({len(df_orders)} linhas)")
    print("----------------------------------")

    # Etapa B: processar demais arquivos filtrando por valid_order_ids
    for arquivo in DEMAIS_ARQUIVOS:
        print(f"Lendo: {arquivo}")
        df = pd.read_csv(arquivo)
        nome_arquivo = arquivo.split("/")[-1]

        df = _limpar_arquivo(df, nome_arquivo, valid_order_ids=valid_order_ids)

        destino = f"data/processed/{nome_arquivo}"
        df.to_csv(destino, index=False)
        print(f"Salvando: {destino} ({len(df)} linhas)")
        print("----------------------------------")

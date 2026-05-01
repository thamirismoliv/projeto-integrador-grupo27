import os
import pandas as pd

arquivos = ["data/raw/olist_orders_dataset.csv",
            "data/raw/olist_order_items_dataset.csv",
            "data/raw/olist_order_payments_dataset.csv",
            "data/raw/olist_order_reviews_dataset.csv",
            "data/raw/olist_products_dataset.csv",
            "data/raw/olist_customers_dataset.csv",
            "data/raw/olist_geolocation_dataset.csv"]

os.makedirs(f"data/processed", exist_ok=True)

for arquivo in arquivos:
    print(f"Lendo: {arquivo}")
    df = pd.read_csv(arquivo)
    print(f"Limpando: {arquivo}")
    df = df.dropna()
    print(f"Salvando: data/processed/{arquivo.split('/')[-1]}")
    df.to_csv(f"data/processed/{arquivo.split('/')[-1]}", index=False)
    print("----------------------------------")
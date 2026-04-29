from pathlib import Path
import requests
import pandas as pd

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "olist_orders_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_orders_dataset.csv",
    "olist_order_items_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_products_dataset.csv",
    "olist_customers_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv": "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/olist_geolocation_dataset.csv",
}

def baixar_arquivo(url, destino):
    resposta = requests.get(url, timeout=120)
    resposta.raise_for_status()
    destino.write_bytes(resposta.content)

def baixar_bases():
    print("Iniciando download das bases...\n")

    for nome_arquivo, url in FILES.items():
        destino = RAW_DIR / nome_arquivo

        if destino.exists():
            print(f"{nome_arquivo} já existe. Pulando download.")
            continue

        print(f"Baixando {nome_arquivo}...")
        baixar_arquivo(url, destino)
        print(f"{nome_arquivo} baixado com sucesso.\n")

def carregar_bases():
    bases = {
        "orders": pd.read_csv(RAW_DIR / "olist_orders_dataset.csv"),
        "order_items": pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv"),
        "order_payments": pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv"),
        "order_reviews": pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv"),
        "products": pd.read_csv(RAW_DIR / "olist_products_dataset.csv"),
        "customers": pd.read_csv(RAW_DIR / "olist_customers_dataset.csv"),
        "geolocation": pd.read_csv(RAW_DIR / "olist_geolocation_dataset.csv"),
    }
    return bases

def exibir_resumo(bases):
    print("\nArquivos carregados com sucesso!\n")

    print("Dimensão das tabelas:")
    for nome, df in bases.items():
        print(f"{nome}: {df.shape}")

    print("\nColunas de cada tabela:\n")
    for nome, df in bases.items():
        print(f"{nome}: {list(df.columns)}")

    print("\nValores nulos por tabela:\n")
    for nome, df in bases.items():
        print(f"{nome}:")
        print(df.isnull().sum())
        print()

    print("Etapa de extração concluída com sucesso!")

def main():
    baixar_bases()
    bases = carregar_bases()
    exibir_resumo(bases)

if __name__ == "__main__":
    main()
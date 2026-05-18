from pathlib import Path
import io
import zipfile
import requests
import pandas as pd

RAW_DIR = Path("data/raw")

URL = "https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce"

ARQUIVOS = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
]


def baixar_bases():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if all((RAW_DIR / f).exists() for f in ARQUIVOS):
        print("Todos os arquivos já existem. Pulando download.")
        return

    print("Baixando dataset...\n")
    resposta = requests.get(URL, timeout=300)
    resposta.raise_for_status()

    # Extrai apenas os arquivos desejados do zip
    with zipfile.ZipFile(io.BytesIO(resposta.content)) as zf:
        for arquivo in ARQUIVOS:
            destino = RAW_DIR / arquivo

            if destino.exists():
                print(f"{arquivo} já existe. Pulando.")
                continue

            print(f"Extraindo {arquivo}...")
            destino.write_bytes(zf.read(arquivo))

    print("\nDownload concluído.\n")


def _carregar_bases():
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


def _exibir_resumo(bases):
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
    bases = _carregar_bases()
    _exibir_resumo(bases)


if __name__ == "__main__":
    main()

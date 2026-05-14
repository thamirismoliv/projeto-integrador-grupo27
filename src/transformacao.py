# transformacao.py

import pandas as pd


def transformar_dados():
    # Passo 1: Carregando os arquivos CSV da pasta data/processed/
    print("Carregando os dados...")
    orders = pd.read_csv('data/processed/olist_orders_dataset.csv')
    items = pd.read_csv('data/processed/olist_order_items_dataset.csv')
    products = pd.read_csv('data/processed/olist_products_dataset.csv')
    print("Dados carregados!")

    # Passo 2: Convertendo colunas de data para datetime
    print("Convertendo datas...")
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    print("Datas convertidas!")

    # Passo 3: Fazendo merge de pedidos com itens (tabela1)
    print("Mesclando pedidos com itens...")
    tabela1 = pd.merge(orders, items, on='order_id')
    print("Tabela1 criada!")

    # Merge da tabela1 com produtos (tabela_final)
    print("Mesclando com produtos...")
    tabela_final = pd.merge(tabela1, products, on='product_id')
    print("Tabela final criada!")

    # Passo 4: Criando coluna valor_total (price + freight_value)
    print("Calculando valor total...")
    tabela_final['valor_total'] = tabela_final['price'] + tabela_final['freight_value']
    print("Valor total adicionado!")

    # Passo 5: Criando coluna tempo_entrega (data entrega - data compra)
    print("Calculando tempo de entrega...")
    tabela_final['tempo_entrega'] = tabela_final['order_delivered_customer_date'] - tabela_final[
        'order_purchase_timestamp']
    print("Tempo de entrega adicionado!")

    # Passo 6: Salvando o resultado em tabela_mestra.csv sem o índice
    print("Salvando tabela mestra...")
    tabela_final.to_csv('data/processed/tabela_mestra.csv', index=False)
    print("Arquivo salvo com sucesso!")

    print("Script finalizado!")

    return tabela_final

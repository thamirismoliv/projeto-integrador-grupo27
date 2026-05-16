import pandas as pd


def transformar_dados():
    print("Iniciando transformação dos dados...")

    orders = pd.read_csv('data/processed/olist_orders_dataset.csv')
    items = pd.read_csv('data/processed/olist_order_items_dataset.csv')
    products = pd.read_csv('data/processed/olist_products_dataset.csv')
    customers = pd.read_csv('data/processed/olist_customers_dataset.csv')

    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

    tabela1 = pd.merge(orders, items, on='order_id')
    tabela_final = pd.merge(tabela1, products, on='product_id')
    tabela_final = pd.merge(tabela_final, customers[['customer_id', 'customer_state']], on='customer_id', how='left')

    tabela_final['valor_total'] = tabela_final['price'] + tabela_final['freight_value']
    tabela_final['tempo_entrega'] = (
        tabela_final['order_delivered_customer_date'] - tabela_final['order_purchase_timestamp']
    ).dt.days

    tabela_final.to_csv('data/processed/tabela_mestra.csv', index=False)
    print("Transformação concluída.")

    return tabela_final

import pandas as pd

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
order_payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
geolocation = pd.read_csv("data/raw/olist_geolocation_dataset.csv")

print("Arquivos carregados com sucesso!\n")

print("Dimensão das tabelas:")
print("orders:", orders.shape)
print("order_items:", order_items.shape)
print("order_payments:", order_payments.shape)
print("order_reviews:", order_reviews.shape)
print("products:", products.shape)
print("customers:", customers.shape)
print("geolocation:", geolocation.shape)

print("\nColunas de cada tabela:\n")
print("orders:", list(orders.columns))
print("order_items:", list(order_items.columns))
print("order_payments:", list(order_payments.columns))
print("order_reviews:", list(order_reviews.columns))
print("products:", list(products.columns))
print("customers:", list(customers.columns))
print("geolocation:", list(geolocation.columns))

print("\nValores nulos por tabela:\n")

print("orders:")
print(orders.isnull().sum())
print()

print("order_items:")
print(order_items.isnull().sum())
print()

print("order_payments:")
print(order_payments.isnull().sum())
print()

print("order_reviews:")
print(order_reviews.isnull().sum())
print()

print("products:")
print(products.isnull().sum())
print()

print("customers:")
print(customers.isnull().sum())
print()

print("geolocation:")
print(geolocation.isnull().sum())
print()
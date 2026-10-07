from data_loader import load_orders, load_products

orders = load_orders()
products = load_products()

print("Orders:", orders.shape)
print("Products:", products.shape)
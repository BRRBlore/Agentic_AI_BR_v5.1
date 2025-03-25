import pandas as pd

DATA_PATH = "/content/drive/My Drive/AI_Agent_4/Ecommerce_Order_Dataset/train/df_Orders.csv"
df_orders = pd.read_csv(DATA_PATH)

def lookup_order(order_id):
    order_id = order_id.strip().upper()
    match = df_orders[df_orders['order_id'].str.upper() == order_id]

    if match.empty:
        return "❌ Order not found. Please check the order ID."

    row = match.iloc[0]
    return (
        f"📦 Order Status: {row['order_status'].capitalize()}\n"
        f"🗓️ Order Date: {row['order_purchase_timestamp']}\n"
        f"✅ Approved On: {row.get('order_approved_at', 'N/A')}\n"
        f"🚚 Delivered On: {row.get('order_delivered_timestamp', 'Not yet delivered')}\n"
        f"📅 Estimated Delivery: {row['order_estimated_delivery_date']}"
    )

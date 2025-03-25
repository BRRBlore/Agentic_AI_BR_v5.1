# tools/order_db.py
import pandas as pd
import os

ORDER_DATA_PATH = os.path.join("Ecommerce_Order_Dataset", "Order_Dataset.csv")

def lookup_order(order_id):
    try:
        df = pd.read_csv(ORDER_DATA_PATH)
        result = df[df['order_id'].astype(str).str.contains(order_id, case=False)]

        if result.empty:
            return "⚠️ Order not found. Please check the Order ID."

        row = result.iloc[0]
        response = f"""📦 **Order Status**: {row['order_status']}
🗓️ **Order Date**: {row['order_purchase_timestamp']}
✅ **Approved On**: {row['order_approved_at']}
🚚 **Delivered On**: {row['order_delivered_timestamp']}
📅 **Estimated Delivery**: {row['order_estimated_delivery_date']}"""
        return response

    except FileNotFoundError:
        return "⚠️ Order tracking file not found. Please contact support."
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {str(e)}"

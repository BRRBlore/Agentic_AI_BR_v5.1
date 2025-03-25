# tools/order_db.py
import pandas as pd
import os

ORDER_DATA_PATH = os.path.join("Ecommerce_Order_Dataset", "Order_Dataset.csv")

def lookup_order(order_id):
    try:
        df = pd.read_csv(ORDER_DATA_PATH)
        result = df[df['Order ID'].astype(str).str.contains(order_id, case=False)]

        if result.empty:
            return "⚠️ Order not found. Please check the Order ID."

        row = result.iloc[0]
        response = f"""📦 **Order Status**: {row['Status']}
🗓️ **Order Date**: {row['Order Date']}
✅ **Approved On**: {row['Approval Date']}
🚚 **Delivered On**: {row['Delivery Date']}
📅 **Estimated Delivery**: {row['Estimated Delivery']}"""
        return response

    except FileNotFoundError:
        return "⚠️ Order tracking file not found. Please contact support."
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {str(e)}"

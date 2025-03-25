# tools/shipping_api.py

import pandas as pd
import os

SHIPPING_DATA_PATH = os.path.join("Ecommerce_Shipping_Data", "Shipping_Dataset.csv")

def lookup_shipping(order_id):
    try:
        df = pd.read_csv(SHIPPING_DATA_PATH)
        result = df[df['Order ID'].astype(str).str.contains(order_id, case=False)]

        if result.empty:
            return "⚠️ Shipping info not found. Please check the Order ID."

        row = result.iloc[0]
        response = f"""🚚 **Shipping Carrier**: {row['Carrier']}
📦 **Tracking Number**: {row['Tracking Number']}
📅 **Shipped On**: {row['Shipping Date']}
🌐 **Shipping Status**: {row['Shipping Status']}"""
        return response

    except FileNotFoundError:
        return "⚠️ Shipping tracking file not found. Please contact support."
    except Exception as e:
        return f"❌ Error fetching shipping details: {str(e)}"

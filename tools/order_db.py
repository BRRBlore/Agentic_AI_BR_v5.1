# tools/order_db.py

import pandas as pd
import os

# Path to the CSV file (relative to root of your repo)
CSV_PATH = os.path.join(os.path.dirname(__file__), "../tech_support_sample_QA.csv")

def lookup_order(order_id: str) -> str:
    try:
        df = pd.read_csv(CSV_PATH)

        # Normalize comparison
        order_row = df[df['Order ID'].astype(str).str.lower() == order_id.lower()]
        if order_row.empty:
            return f"❌ Order ID '{order_id}' not found."

        row = order_row.iloc[0]
        return (
            f"📦 Order Status: {row['Status']}\n"
            f"🗓️ Order Date: {row['Order Date']}\n"
            f"✅ Approved On: {row['Approval Date']}\n"
            f"🚚 Delivered On: {row['Delivery Date']}\n"
            f"📅 Estimated Delivery: {row['Estimated Delivery']}"
        )

    except FileNotFoundError:
        return "⚠️ Order data file not found. Please contact support."

    except Exception as e:
        return f"⚠️ An unexpected error occurred: {e}"

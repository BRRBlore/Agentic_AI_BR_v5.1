# tools/dispatch_api.py

import pandas as pd
import os

CSV_PATH = os.path.join("Ecommerce_Transport_LogisticsTracking", "Transportation_and_Logistics_Tracking_Dataset.xlsx")

def track_delivery(tracking_id):
    try:
        # Load the correct sheet
        df = pd.read_excel(CSV_PATH, sheet_name="Refined")

        # Clean up column names (remove spaces, lower case)
        df.columns = df.columns.str.strip()

        # Check column name and fix key mismatch
        if "Delivery Id" not in df.columns:
            return "❌ Error: 'Delivery Id' column not found in Excel sheet."

        # Match against tracking ID (case-insensitive)
        match = df[df["Delivery Id"].astype(str).str.contains(str(tracking_id), case=False, na=False)]

        if match.empty:
            return "⚠️ Delivery tracking file not found. Please check the Delivery ID."

        row = match.iloc[0]
        response = (
            f"📦 **Delivery ID**: {row['Delivery Id']}\n"
            f"🚚 **Status**: ✅ Delivered\n"
            f"🕒 **Dispatched On**: {row.get('created_at', 'N/A')}\n"
            f"⏱️ **Delivered At**: {row.get('actual_delivery_time', 'N/A')}\n"
            f"📍 **From**: {row.get('Origin_Location', 'N/A')}\n"
            f"📍 **To**: {row.get('Destination_Location', 'N/A')}\n"
            f"📊 **On-Time**: {row.get('On time Delivery', 'N/A')}\n"
            f"🌤️ **Weather**: {row.get('condition_text', 'N/A')}\n"
            f"⭐ **Customer Rating**: {row.get('Customer_rating', 'N/A')}"
        )
        return response

    except FileNotFoundError:
        return f"❌ File not found: {CSV_PATH}"
    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

# tools/dispatch_api.py

import pandas as pd
import os

# ✅ Use absolute path to Excel file on Google Drive
EXCEL_PATH = "/content/drive/My Drive/AI_Agent_4/Ecommerce_Transport_LogisticsTracking/Transportation_and_Logistics_Tracking_Dataset.xlsx"

def track_delivery(delivery_id: str) -> str:
    try:
        print(f"🔎 DEBUG: Looking for delivery ID -> {delivery_id}")  # ✅ Debug line

        # ✅ Read 'Refined' sheet
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # ✅ Normalize column names for safer access
        df.columns = df.columns.str.strip().str.lower()

        # ✅ Check for correct delivery ID column
        delivery_col = None
        if "delivery id" in df.columns:
            delivery_col = "delivery id"
        elif "deliveryid" in df.columns:
            delivery_col = "deliveryid"
        else:
            return "❌ Delivery ID column not found in dataset."

        # ✅ Perform case-insensitive matching
        match = df[df[delivery_col].astype(str).str.contains(delivery_id, case=False, na=False)]

        if match.empty:
            return "❌ Delivery ID not found. Please check and try again."

        row = match.iloc[0]

        # ✅ Format response from cleaned columns
        response = (
            f"📦 **Delivery ID**: {row[delivery_col]}\n"
            f"🚚 **Status**: ✅ Delivered\n"
            f"🕒 **Dispatched On**: {row['created_at']}\n"
            f"⏱️ **Delivered At**: {row['actual_delivery_time']}\n"
            f"📍 **From**: {row['origin_location']}\n"
            f"📍 **To**: {row['destination_location']}\n"
            f"📊 **On-Time**: {'Yes' if row['on time delivery'] == 1 else 'No'}\n"
            f"🌤️ **Weather**: {row['condition_text']}\n"
            f"⭐ **Customer Rating**: {row['customer_rating']}"
        )

        return response

    except FileNotFoundError:
        return "❌ Logistics dataset not found. Please check the file path."
    except Exception as e:
        return f"❌ Error: {str(e)}"

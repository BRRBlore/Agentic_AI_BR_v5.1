# tools/dispatch_api.py

import pandas as pd

# Path to your Excel file in Google Drive
EXCEL_PATH = "/content/drive/My Drive/AI_Agent_4/Ecommerce_Transport_LogisticsTracking/Transportation_and_Logistics_Tracking_Dataset.xlsx"

# Load the "Refined" sheet
df_dispatch = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

def track_delivery(delivery_id):
    delivery_id = delivery_id.strip().upper()
    match = df_dispatch[df_dispatch['Delivery Id'].str.upper() == delivery_id]

    if match.empty:
        return "❌ Delivery ID not found. Please check and try again."

    row = match.iloc[0]

    status = "✅ Delivered" if pd.notnull(row['actual_delivery_time']) else "⌛ In Transit"
    on_time = "Yes" if row['On time Delivery'] == 1.0 else "No"

    return (
        f"📦 **Delivery ID**: {row['Delivery Id']}\n"
        f"🚚 **Status**: {status}\n"
        f"🕒 **Dispatched On**: {row['created_at']}\n"
        f"⏱️ **Delivered At**: {row.get('actual_delivery_time', 'Not yet')}\n"
        f"📍 **From**: {row['Origin_Location']}\n"
        f"📍 **To**: {row['Destination_Location']}\n"
        f"📊 **On-Time**: {on_time}\n"
        f"🌤️ **Weather**: {row['condition_text']}\n"
        f"⭐ **Customer Rating**: {row['Customer_rating']}"
    )

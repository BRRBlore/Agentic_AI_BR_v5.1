# tools/dispatch_api.py

import pandas as pd
import os

# Correct path and file name
EXCEL_PATH = os.path.join("Ecommerce_Transport_LogisticsTracking", "Transportation_and_Logistics_Tracking_Dataset.xlsx")

def track_delivery(tracking_id):
    try:
        # Load the Refined sheet
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # Match tracking ID using correct column name "Delivery Id"
        match = df[df["Delivery Id"].astype(str).str.contains(str(tracking_id), case=False, na=False)]

        if match.empty:
            return "⚠️ Delivery tracking file not found. Please check the Delivery ID."

        row = match.iloc[0]
        response = (
            f"📦 **Delivery ID**: {row['Delivery Id']}\n"
            f"🚚 **Status**: ✅ Delivered\n"
            f"🕒 **Dispatched On**: {row['Dispatched Date']}\n"
            f"⏱️ **Delivered At**: {row['Delivery Date']}\n"
            f"📍 **From**: {row['Source Location']}\n"
            f"📍 **To**: {row['Destination Location']}\n"
            f"📊 **On-Time**: {row['On-Time']}\n"
            f"🌤️ **Weather**: {row['Weather']}\n"
            f"⭐ **Customer Rating**: {row['Customer Rating']}"
        )
        return response

    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

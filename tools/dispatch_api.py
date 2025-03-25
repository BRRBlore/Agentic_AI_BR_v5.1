# tools/dispatch_api.py

import pandas as pd
import os

# Correct Excel file and sheet path
EXCEL_PATH = os.path.join(
    "Ecommerce_Transport_LogisticsTracking",
    "Transportation_and_Logistics_Tracking_Dataset.xlsx"
)

def track_delivery(tracking_id):
    try:
        # Load the refined sheet
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # Clean column headers in case of hidden whitespaces
        df.columns = df.columns.str.strip()

        # Standardize Delivery ID column and tracking input
        df["Delivery Id"] = df["Delivery Id"].astype(str).str.strip().str.upper()
        tracking_id = tracking_id.strip().upper()

        # Match the tracking ID
        match = df[df["Delivery Id"].str.contains(tracking_id, na=False)]

        if match.empty:
            return "⚠️ Delivery tracking file not found. Please check the Delivery ID."

        row = match.iloc[0]

        # Construct response
        response = (
            f"📦 **Delivery ID**: {row['Delivery Id']}\n"
            f"🚚 **Status**: ✅ Delivered\n"
            f"🕒 **Dispatched On**: {row['created_at']}\n"
            f"⏱️ **Delivered At**: {row['actual_delivery_time']}\n"
            f"📍 **From**: {row['Origin_Location']}\n"
            f"📍 **To**: {row['Destination_Location']}\n"
            f"📊 **On-Time Delivery**: {'Yes' if row['On time Delivery'] == 1 else 'No'}\n"
            f"🌤️ **Weather**: {row['condition_text']}\n"
            f"⭐ **Customer Rating**: {row['Customer_rating']}"
        )
        return response

    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

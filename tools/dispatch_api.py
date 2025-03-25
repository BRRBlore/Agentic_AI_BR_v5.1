# tools/dispatch_api.py

import pandas as pd
import os

# Path to your Excel file inside the repo
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "../Transportation_and_Logistics_Tracking_Dataset.xlsx")

def track_delivery(delivery_id: str) -> str:
    try:
        # Read the 'Refined' sheet (update this if your data is in another sheet)
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # Find matching row by Delivery ID
        row = df[df["Delivery Id"].astype(str).str.lower() == delivery_id.lower()]
        if row.empty:
            return f"❌ Delivery ID '{delivery_id}' not found."

        row = row.iloc[0]  # Get the first match

        # Format the response
        return (
            f"📦 **Delivery ID**: {row['Delivery Id']}\n"
            f"🚚 **Status**: ✅ Delivered\n"
            f"🕒 **Dispatched On**: {row['created_at']}\n"
            f"⏱️ **Delivered At**: {row['actual_delivery_time']}\n"
            f"📍 **From**: {row['Origin_Location']}\n"
            f"📍 **To**: {row['Destination_Location']}\n"
            f"📊 **On-Time**: {'Yes' if row['On time Delivery'] == 1 else 'No'}\n"
            f"🌤️ **Weather**: {row['condition_text']}\n"
            f"⭐ **Customer Rating**: {row['Customer_rating']}"
        )

    except FileNotFoundError:
        return "⚠️ Delivery tracking file not found. Please contact support."

    except Exception as e:
        return f"⚠️ An error occurred while tracking delivery: {str(e)}"

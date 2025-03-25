# tools/dispatch_api.py
import pandas as pd
import os

DISPATCH_FILE = os.path.join("Ecommerce_Transport_LogisticsTracking", "Transportation_and_Logistics_Tracking_Dataset.xlsx")

def track_dispatch(dispatch_id):
    try:
        df = pd.read_excel(DISPATCH_FILE, sheet_name="Refined")
        result = df[df['Delivery ID'].astype(str).str.contains(dispatch_id, case=False)]

        if result.empty:
            return "⚠️ Delivery tracking ID not found. Please contact support."

        row = result.iloc[0]
        response = f"""📦 **Delivery ID**: {row['Delivery ID']}
🚚 **Status**: ✅ {row['Status']}
🕒 **Dispatched On**: {row['Dispatched On']}
⏱️ **Delivered At**: {row['Delivered At']}
📍 **From**: {row['From']}
📍 **To**: {row['To']}
📊 **On-Time**: {row['On Time']}
🌤️ **Weather**: {row['Weather']}
⭐ **Customer Rating**: {row['Customer Rating']}"""
        return response

    except FileNotFoundError:
        return "⚠️ Delivery tracking file not found. Please contact support."
    except Exception as e:
        return f"⚠️ An unexpected error occurred: {str(e)}"

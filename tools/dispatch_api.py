# tools/dispatch_api.py

import pandas as pd
import os

# Correct Excel file path
EXCEL_PATH = os.path.join("Ecommerce_Transport_LogisticsTracking", "Transportation_and_Logistics_Tracking_Dataset.xlsx")
SHEET_NAME = "Refined"  # Sheet to load

def track_delivery(tracking_id):
    try:
        # Load the specified sheet
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

        # Match tracking ID from the "Delivery ID" column
        match = df[df["Delivery ID"].astype(str).str.contains(str(tracking_id), case=False, na=False)]

        if match.empty:
            return "⚠️ Delivery tracking ID not found. Please check and try again."

        row = match.iloc[0]

        # Build response safely using `.get()` fallback
        response = f"""📦 **Delivery ID**: {row.get('Delivery ID', 'N/A')}
🚚 **Status**: ✅ Delivered
🕒 **Dispatched On**: {row.get('Dispatched Date', 'N/A')}
⏱️ **Delivered At**: {row.get('Delivery Date', 'N/A')}
📍 **From**: {row.get('Source Location', 'N/A')}
📍 **To**: {row.get('Destination Location', 'N/A')}
📊 **On-Time**: {row.get('On-Time', 'N/A')}
🌤️ **Weather**: {row.get('Weather', 'N/A')}
⭐ **Customer Rating**: {row.get('Customer Rating', 'N/A')}"""
        return response

    except FileNotFoundError:
        return "❌ Delivery tracking file not found. Please contact support."

    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

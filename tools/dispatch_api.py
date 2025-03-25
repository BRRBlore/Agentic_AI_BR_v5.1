# tools/dispatch_api.py

import pandas as pd
import os

# Path to the Excel file
EXCEL_PATH = os.path.join("Ecommerce_Transport_LogisticsTracking", "Transportation_and_Logistics_Tracking_Dataset.xlsx")

def track_delivery(tracking_id):
    try:
        # Load Excel sheet named "Refined"
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # Ensure column is named correctly
        if "Delivery Id" not in df.columns:
            return "❌ 'Delivery Id' column not found in the Excel sheet."

        # Match against Delivery Id
        match = df[df["Delivery Id"].astype(str).str.contains(str(tracking_id), case=False, na=False)]

        if match.empty:
            return "⚠️ Delivery tracking file not found. Please check the Delivery ID."

        row = match.iloc[0]
        response = (
            f"📦 **Delivery ID**: {row['Delivery Id']}\n"
            f"🚚 **From**: {row['Origin_Location']}\n"
            f"📍 **To**: {row['Destination_Location']}\n"
            f"🌍 **Region**: {row['region']}\n"
            f"📅 **Created At**: {row['created_at']}\n"
            f"⏱️ **Delivered At**: {row['actual_delivery_time']}\n"
            f"🕒 **On-Time**: {'✅ Yes' if row['On time Delivery'] == 1 else '❌ No'}\n"
            f"⭐ **Customer Rating**: {row['Customer_rating']}\n"
            f"🌤️ **Condition**: {row['condition_text']}\n"
            f"💰 **Cost**: ₹{row['Fixed Costs']} | 🛠️ Maintenance: ₹{row['Maintenance']}"
        )
        return response

    except FileNotFoundError:
        return "❌ Excel file not found."
    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

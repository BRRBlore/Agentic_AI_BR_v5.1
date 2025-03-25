import pandas as pd
import os

# Set correct path for the Excel file
EXCEL_PATH = os.path.join(
    "Ecommerce_Transport_LogisticsTracking",
    "Transportation_and_Logistics_Tracking_Dataset.xlsx"
)

def track_delivery(tracking_id):
    try:
        # Load the correct sheet
        df = pd.read_excel(EXCEL_PATH, sheet_name="Refined")

        # OPTIONAL: Print columns for debug
        # print("Available columns:", df.columns.tolist())

        # Match using the correct column name: 'Delivery Id'
        match = df[df["Delivery Id"].astype(str).str.contains(str(tracking_id), case=False, na=False)]

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
            f"📊 **On-Time**: {row['On time Delivery']}\n"
            f"🌤️ **Weather**: {row['condition_text']}\n"
            f"⭐ **Customer Rating**: {row['Customer_rating']}"
        )
        return response

    except FileNotFoundError:
        return "❌ Error: Logistics tracking file not found on the server."
    except KeyError as e:
        return f"❌ Error fetching delivery details: Column not found: {str(e)}"
    except Exception as e:
        return f"❌ Error fetching delivery details: {str(e)}"

import pandas as pd
import re

def clean_monday_data(raw_items):

    cleaned_data = []

    for item in raw_items:
        row = {"name": item["name"]}

        for col in item["column_values"]:
            col_id = col.get("id", "unknown")
            val = col.get("text", "")

            # Handle numeric fields
            if "value" in col_id or "revenue" in col_id:
                if val:
                    numeric_val = re.sub(r"[^\d.]", "", val)
                    row[col_id] = float(numeric_val) if numeric_val else 0.0
                else:
                    row[col_id] = 0.0

            # Handle date fields
            elif "date" in col_id:
                if val:
                    date_val = pd.to_datetime(val, errors="coerce")
                    row[col_id] = date_val
                else:
                    row[col_id] = None

            # Handle text fields
            else:
                row[col_id] = val.strip().lower() if val else "unknown"

        cleaned_data.append(row)

    return pd.DataFrame(cleaned_data)
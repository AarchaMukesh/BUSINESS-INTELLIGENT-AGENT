# Goal: Convert Messy Monday Data to Usable Dataframe

import pandas as pd

def monday_to_dataframe(api_response):

    items = api_response["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Item Name": item["name"]}

        for col in item["column_values"]:
            col_name = col["column"]["title"]
            row[col_name] = col["text"]

        rows.append(row)

    df = pd.DataFrame(rows)

    return df
# Building the question answering agent

import pandas as pd
from monday_api import get_board_items
from data_processing import monday_to_dataframe


def run_bi_agent(user_query, deals_board_id, work_orders_board_id, context=None):

    if context is None:
        context = {}

    steps = []
    query = user_query.lower()

    # --------------------------------
    # 1. LIVE DATA FETCH
    # --------------------------------
    steps.append("📡 Fetching live data from Monday boards")

    deals_response = get_board_items(deals_board_id)
    work_orders_response = get_board_items(work_orders_board_id)

    # --------------------------------
    # 2. DATAFRAME CONVERSION
    # --------------------------------
    steps.append("📊 Converting API data to dataframe")

    deals_df = monday_to_dataframe(deals_response)
    work_orders_df = monday_to_dataframe(work_orders_response)

    # --------------------------------
    # 3. DATA CLEANING
    # --------------------------------
    steps.append("🧹 Cleaning inconsistent values")

    deals_df = deals_df.fillna("")
    work_orders_df = work_orders_df.fillna("")

    # --------------------------------
    # 4. AUTO DETECT IMPORTANT COLUMNS
    # --------------------------------
    revenue_col = None
    sector_col = None
    status_col = None

    for col in deals_df.columns:

        name = col.lower()

        if "revenue" in name or "value" in name:
            revenue_col = col

        if "sector" in name or "service" in name:
            sector_col = col

        if "status" in name:
            status_col = col

    # --------------------------------
    # FOLLOW-UP QUERY SUPPORT
    # --------------------------------
    if "those" in query or "them" in query:

        if "last_result" not in context:
            return "No previous result available to filter.", steps

        df = context["last_result"]

        if "energy" in query and sector_col:

            filtered = df[df[sector_col].str.contains("energy", case=False, na=False)]

            context["last_result"] = filtered

            return f"Filtered results contain {len(filtered)} energy sector deals.", steps

    # --------------------------------
    # PIPELINE / REVENUE ANALYSIS
    # --------------------------------
    if "pipeline" in query or "revenue" in query:

        if revenue_col is None:
            return "Revenue column not found.", steps

        deals_df[revenue_col] = (
            deals_df[revenue_col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("$", "")
        )

        deals_df[revenue_col] = pd.to_numeric(deals_df[revenue_col], errors="coerce")

        total = deals_df[revenue_col].sum()
        avg = deals_df[revenue_col].mean()

        context["last_result"] = deals_df

        insight = f"""
Pipeline Overview

Total Pipeline Value: ${total:,.2f}
Total Deals: {len(deals_df)}
Average Deal Size: ${avg:,.2f}
"""

        return insight, steps

    # --------------------------------
    # SECTOR PERFORMANCE
    # --------------------------------
    if "sector" in query:

        if sector_col is None:
            return "Sector column not found.", steps

        sector_counts = deals_df[sector_col].value_counts()

        top_sector = sector_counts.index[0]
        top_count = sector_counts.iloc[0]

        total_deals = len(deals_df)

        breakdown = ""

        for sector, count in sector_counts.items():

            percent = (count / total_deals) * 100

            breakdown += f"{sector}: {count} deals ({percent:.1f}%)\n"

        context["last_result"] = deals_df

        insight = f"""
Top Performing Sector: {top_sector}

Deals in Top Sector: {top_count}

Sector Distribution:
{breakdown}
"""

        return insight, steps

    # --------------------------------
    # TOP DEALS
    # --------------------------------
    if "top" in query and "deal" in query:

        if revenue_col is None:
            return "Revenue column not found.", steps

        deals_df[revenue_col] = pd.to_numeric(
            deals_df[revenue_col].astype(str).str.replace(",", "").str.replace("$", ""),
            errors="coerce"
        )

        top_deals = deals_df.sort_values(revenue_col, ascending=False).head(5)

        context["last_result"] = top_deals

        insight = f"""
Top 5 Deals by Value

{top_deals[['Item Name', revenue_col]]}
"""

        return insight, steps

    # --------------------------------
    # WORK ORDER METRICS
    # --------------------------------
    if "work order" in query or "delivery" in query:

        total_orders = len(work_orders_df)

        delayed = 0

        for col in work_orders_df.columns:
            if "status" in col.lower():

                delayed = len(
                    work_orders_df[
                        work_orders_df[col].str.contains("delay", case=False, na=False)
                    ]
                )

        insight = f"""
Operational Overview

Total Work Orders: {total_orders}
Delayed Orders: {delayed}
"""

        return insight, steps

    return "I couldn't interpret the query yet. Try asking about pipeline, sectors, deals, or work orders.", steps
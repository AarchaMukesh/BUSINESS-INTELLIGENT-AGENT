# Building the chat interface

import streamlit as st
from agent import run_bi_agent


# -------------------------------
# BOARD IDS
# -------------------------------
DEALS_BOARD_ID = 5026984879
WORK_ORDERS_BOARD_ID = 5026985516


st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com Business Intelligence Agent")


st.write("""
This prototype answers **founder-level business intelligence questions**
using **live data from Monday.com boards**.

The agent performs:

1️⃣ Live Monday API queries  
2️⃣ Data cleaning and normalization  
3️⃣ Rule-based query interpretation  
4️⃣ Business analytics on deals and work orders
""")


# -------------------------------
# LIMITATIONS
# -------------------------------
st.info("""
⚠️ **Current Limitations**

This agent uses **rule-based query interpretation**, which means:

• It can only answer questions it has explicit logic rules for  
• It does not fully understand complex natural language queries  
• Time-based filters like **"this quarter"** are not yet supported  
• Follow-up queries work only for simple filters (e.g., "filter those by energy")  
• Column detection depends on column names containing words like **sector, value, status**

With more time, this could be improved by:

• Adding a query parser  
• Supporting time-series analysis  
• Using a hybrid AI + analytics approach
""")


# -------------------------------
# EXAMPLE QUESTIONS
# -------------------------------
st.write("### Example Questions")

st.write("""
• How is our pipeline looking?  
• Which sector has the most deals?  
• Show the top deals  
• How many deals do we have?  
• Are any work orders delayed?  
• Show sector distribution  
""")


st.divider()


# -------------------------------
# CONVERSATION MEMORY
# -------------------------------
if "context" not in st.session_state:
    st.session_state.context = {}


# -------------------------------
# USER INPUT
# -------------------------------
query = st.text_input("Ask a business question")


# -------------------------------
# RUN AGENT
# -------------------------------
if query:

    answer, steps = run_bi_agent(
        query,
        DEALS_BOARD_ID,
        WORK_ORDERS_BOARD_ID,
        st.session_state.context
    )

    # Show agent reasoning steps
    st.subheader("🤖 Agent Actions")

    for step in steps:
        st.write(step)

    # Show insight
    st.subheader("📈 Business Insight")

    st.success(answer)
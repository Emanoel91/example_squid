import streamlit as st
import requests
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Squid Tokens",
    layout="wide"
)

st.title("🪙 Squid Supported Tokens")

# -----------------------------
# API Configuration
# -----------------------------
URL = "https://v2.api.squidrouter.com/v2/tokens"

HEADERS = {
    "x-integrator-id": "squid-analytics-8e21d778-a2a6-4a50-802c-77d3987802"
}

# -----------------------------
# Call API
# -----------------------------
with st.spinner("Loading Tokens..."):

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=60
    )

# -----------------------------
# Error Handling
# -----------------------------
if response.status_code != 200:

    st.error(f"HTTP Error {response.status_code}")

    st.code(response.text)

    st.stop()

# -----------------------------
# Parse JSON
# -----------------------------
data = response.json()

# -----------------------------
# Show Raw JSON
# -----------------------------
with st.expander("📄 Raw JSON"):

    st.json(data)

# -----------------------------
# Convert JSON to DataFrame
# -----------------------------
if isinstance(data, dict):

    if "tokens" in data:

        df = pd.json_normalize(data["tokens"])

    elif "data" in data:

        df = pd.json_normalize(data["data"])

    else:

        df = pd.json_normalize(data)

elif isinstance(data, list):

    df = pd.json_normalize(data)

else:

    st.error("Unknown JSON structure.")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Tokens", f"{len(df):,}")

with col2:
    st.metric("Total Columns", len(df.columns))

# -----------------------------
# Data Table
# -----------------------------
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Column Information
# -----------------------------
st.subheader("Columns")

columns = pd.DataFrame({
    "Column": df.columns,
    "Type": df.dtypes.astype(str)
})

st.dataframe(
    columns,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download CSV",
    csv,
    file_name="squid_tokens.csv",
    mime="text/csv"
)

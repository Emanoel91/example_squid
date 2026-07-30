import streamlit as st
import requests
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Squid Chains Explorer",
    layout="wide"
)

st.title("🦑 Squid Supported Chains")

# -----------------------------
# Integrator ID
# -----------------------------
INTEGRATOR_ID = "squid-analytics-8e21d778-a2a6-4a50-802c-77d3987802"

URL = "https://v2.api.squidrouter.com/v2/chains"

headers = {
    "x-integrator-id": INTEGRATOR_ID
}

# -----------------------------
# Load Data
# -----------------------------
with st.spinner("Loading chains from Squid API..."):

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

# -----------------------------
# Check Response
# -----------------------------
if response.status_code != 200:

    st.error(f"HTTP {response.status_code}")

    st.code(response.text)

    st.stop()

data = response.json()

# -----------------------------
# Display JSON Structure
# -----------------------------
st.subheader("Raw JSON")

st.json(data)

# -----------------------------
# Convert JSON to DataFrame
# -----------------------------
if isinstance(data, dict):

    # اگر کلید chains وجود داشته باشد
    if "chains" in data:

        df = pd.json_normalize(data["chains"])

    # اگر کلید data وجود داشته باشد
    elif "data" in data:

        df = pd.json_normalize(data["data"])

    else:

        df = pd.json_normalize(data)

elif isinstance(data, list):

    df = pd.json_normalize(data)

else:

    st.warning("Unknown JSON structure.")
    st.stop()

# -----------------------------
# Display DataFrame
# -----------------------------
st.subheader("Chains Table")

st.write(f"Number of Chains: **{len(df):,}**")

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
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(
    columns,
    use_container_width=True,
    hide_index=True
)

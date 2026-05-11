import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Convert TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')

# Sidebar
st.sidebar.title("Dashboard Filters")

contract_filter = st.sidebar.multiselect(
    "Select Contract Type",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

# Apply Filters
filtered_df = df[
    (df["Contract"].isin(contract_filter)) &
    (df["gender"].isin(gender_filter))
]

# Dashboard Title
st.title("Customer Churn Prediction & Risk Segmentation Dashboard")

st.markdown("---")

# KPI Metrics
total_customers = len(filtered_df)
churn_customers = (filtered_df["Churn"] == "Yes").sum()
retained_customers = (filtered_df["Churn"] == "No").sum()
churn_rate = round((churn_customers / total_customers) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churn Customers", churn_customers)
col3.metric("Retained Customers", retained_customers)
col4.metric("Churn Rate (%)", churn_rate)

st.markdown("---")

# Row 1 Charts
col5, col6 = st.columns(2)

with col5:
    st.subheader("Churn Distribution")

    fig1 = px.pie(
        filtered_df,
        names="Churn",
        hole=0.5
    )

    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("Churn by Contract Type")

    fig2 = px.histogram(
        filtered_df,
        x="Contract",
        color="Churn",
        barmode="group"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Row 2 Charts
col7, col8 = st.columns(2)

with col7:
    st.subheader("Monthly Charges vs Tenure")

    fig3 = px.scatter(
        filtered_df,
        x="MonthlyCharges",
        y="tenure",
        color="Churn",
        hover_data=["customerID"]
    )

    st.plotly_chart(fig3, use_container_width=True)

with col8:
    st.subheader("Internet Service Distribution")

    fig4 = px.histogram(
        filtered_df,
        x="InternetService",
        color="Churn",
        barmode="group"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Dataset Preview
st.markdown("---")

st.subheader("Filtered Dataset Preview")

st.dataframe(filtered_df.head(20))
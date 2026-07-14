import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# Configure Page
# =====================================
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================
# Dashboard Title
# =====================================
st.title("📊 Global Superstore Business Dashboard")

st.write(
    "This interactive dashboard provides insights into sales, profit, customer performance, "
    "and product performance using the Global Superstore dataset."
)

# =====================================
# Load Dataset
# =====================================
df = pd.read_csv("cleaned_superstore.csv")

# =====================================
# Sidebar Filters
# =====================================
st.sidebar.title("📌 Dashboard Filters")
st.sidebar.markdown("Use the filters below to explore the data.")

region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

subcategory = st.sidebar.multiselect(
    "Select Sub-Category",
    options=sorted(df["Sub-Category"].unique()),
    default=sorted(df["Sub-Category"].unique())
)

# =====================================
# Apply Filters
# =====================================
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(subcategory))
]

# =====================================
# KPI Calculations
# =====================================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

st.divider()

# =====================================
# KPI Section
# =====================================
st.markdown("## 📈 Key Performance Indicators")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.2f}"
    )

st.divider()

# =====================================
# Top 5 Customers
# =====================================
st.subheader("🏆 Top 5 Customers by Sales")

top_customers = (
    filtered_df
    .groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

top_customers["Sales"] = top_customers["Sales"].map(lambda x: f"${x:,.2f}")

st.table(top_customers)

st.divider()

# =====================================
# Sales by Category
# =====================================
sales_by_category = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_sales = px.bar(
    sales_by_category,
    x="Category",
    y="Sales",
    title="📊 Sales by Category",
    text_auto=".2s",
    color="Category",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_sales.update_layout(
    xaxis_title="Category",
    yaxis_title="Sales ($)"
)

# =====================================
# Profit by Region
# =====================================
profit_by_region = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
    .reset_index()
)


fig_profit = px.bar(
    profit_by_region,
    x="Region",
    y="Profit",
    title="🌍 Profit by Region",
    text_auto=".2s",
    color="Region",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_profit.update_layout(
    xaxis_title="Region",
    yaxis_title="Profit ($)"
)

# =====================================
# Display Charts
# =====================================
chart1, chart2 = st.columns(2)

with chart1:
    st.plotly_chart(fig_sales, use_container_width=True)

with chart2:
    st.plotly_chart(fig_profit, use_container_width=True)

st.divider()

# =====================================
# Sales by Sub-Category
# =====================================
sales_by_subcategory = (
    filtered_df
    .groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_subcategory = px.bar(
    sales_by_subcategory,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="📦 Sales by Sub-Category",
    text_auto=".2s",
    color="Sales",
    color_continuous_scale="Blues"
)
fig_subcategory.update_layout(
    xaxis_title="Sales ($)",
    yaxis_title="Sub-Category"
)

st.plotly_chart(fig_subcategory, use_container_width=True)

st.divider()

# =====================================
# Footer
# =====================================
st.caption(
    "Global Superstore Dashboard | Built by Abdul Baqi | Internship Project | Streamlit & Plotly"
)
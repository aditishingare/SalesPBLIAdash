# Salesapp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Customer Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("PBLIA_Dashboard data set.xlsx")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
gender = st.sidebar.multiselect("Select Gender:", options=df["Gender"].unique(), default=df["Gender"].unique())
city = st.sidebar.multiselect("Select City:", options=df["City"].unique(), default=df["City"].unique())
age = st.sidebar.slider("Select Age Range:", int(df["Age"].min()), int(df["Age"].max()), (25, 45))

# Apply filters
filtered_df = df[(df["Gender"].isin(gender)) & (df["City"].isin(city)) & (df["Age"].between(age[0], age[1]))]

# Dashboard title
st.title("📊 Customer Sales Insight Dashboard")
st.markdown("This dashboard gives complete macro and micro-level insights into customer behavior, sales patterns, discounts, acquisition channels, and engagement metrics.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Sales & Discounts", "Engagement & Ratings", "Marketing Insights"])

# ==================== Tab 1: Overview ====================
with tab1:
    st.header("🔍 Customer Overview")
    st.markdown("### Summary statistics by gender and city")
    st.dataframe(filtered_df.groupby(['Gender', 'City'])[['Net Sales', 'Items Purchased']].mean().round(2))

    st.markdown("### Age Distribution")
    fig1 = px.histogram(filtered_df, x="Age", nbins=20, color="Gender", title="Age Distribution by Gender")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Net Sales Distribution")
    fig2 = px.histogram(filtered_df, x="Net Sales", nbins=30, color="City", title="Net Sales by City")
    st.plotly_chart(fig2, use_container_width=True)

# ==================== Tab 2: Sales & Discounts ====================
with tab2:
    st.header("💰 Sales & Discount Analysis")
    st.markdown("### Sales vs Discount Scatter")
    fig3 = px.scatter(filtered_df, x="Discount Amount", y="Net Sales", color="Gender", trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Average Sales by City")
    fig4 = px.bar(filtered_df.groupby("City")["Net Sales"].mean().reset_index(), x="City", y="Net Sales", title="Average Net Sales per City")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Discount Usage by Satisfaction")
    fig5 = px.box(filtered_df, x="Satisfaction Level", y="Discount Amount", color="Satisfaction Level")
    st.plotly_chart(fig5, use_container_width=True)

# ==================== Tab 3: Engagement & Ratings ====================
with tab3:
    st.header("⭐ Engagement & Ratings")
    st.markdown("### Engagement Score by Gender and Intent")
    fig6 = px.box(filtered_df, x="Gender", y="Engagement Score", color="Repeat Purchase Intent")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### Average Rating Distribution")
    fig7 = px.histogram(filtered_df, x="Average Rating", nbins=10, color="Satisfaction Level")
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("### Correlation Heatmap")
    corr = filtered_df[['Age', 'Items Purchased', 'Average Rating', 'Discount Amount', 'Net Sales', 'Engagement Score']].corr()
    fig8, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
    st.pyplot(fig8)

# ==================== Tab 4: Marketing Insights ====================
with tab4:
    st.header("📢 Marketing Channels & Acquisition")
    st.markdown("### Acquisition Channel Distribution")
    fig9 = px.pie(filtered_df, names="Customer Acquisition Channel", title="Customer Acquisition Channel Distribution")
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("### Lead Source vs Net Sales")
    fig10 = px.box(filtered_df, x="Lead Source", y="Net Sales", color="Lead Source")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("### Satisfaction Level by Channel")
    st.dataframe(filtered_df.groupby("Customer Acquisition Channel")["Satisfaction Level"].value_counts(normalize=True).unstack().round(2))

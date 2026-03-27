# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------
# 1. Load Data
# ----------------------
data = pd.read_excel(r"European_Bank.xlsx")  # Update path if needed

# ----------------------
# 2. Add Engagement Profile
# ----------------------
def engagement_profile(row):
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
        return "Active Engaged"
    elif row['IsActiveMember'] == 1 and row['NumOfProducts'] <= 1:
        return "Active Low-Product"
    elif row['IsActiveMember'] == 0 and row['Balance'] > 50000:
        return "Inactive High-Balance"
    else:
        return "Inactive Disengaged"

data['EngagementProfile'] = data.apply(engagement_profile, axis=1)

# ----------------------
# 3. Sidebar Filters
# ----------------------
st.sidebar.title("Filters")
geography = st.sidebar.multiselect("Geography", data['Geography'].unique(), default=data['Geography'].unique())
gender = st.sidebar.multiselect("Gender", data['Gender'].unique(), default=data['Gender'].unique())
balance_range = st.sidebar.slider("Balance Range", float(data['Balance'].min()), float(data['Balance'].max()), (float(data['Balance'].min()), float(data['Balance'].max())))
products_range = st.sidebar.slider("Number of Products", int(data['NumOfProducts'].min()), int(data['NumOfProducts'].max()), (int(data['NumOfProducts'].min()), int(data['NumOfProducts'].max())))

filtered_data = data[
    (data['Geography'].isin(geography)) &
    (data['Gender'].isin(gender)) &
    (data['Balance'] >= balance_range[0]) & (data['Balance'] <= balance_range[1]) &
    (data['NumOfProducts'] >= products_range[0]) & (data['NumOfProducts'] <= products_range[1])
]

# ----------------------
# 4. KPIs
# ----------------------
engagement_retention_ratio = filtered_data[filtered_data['IsActiveMember']==1]['Exited'].mean() / filtered_data[filtered_data['IsActiveMember']==0]['Exited'].mean()
product_depth_index = filtered_data[['NumOfProducts', 'Exited']].corr().iloc[0,1]
high_balance_disengagement_rate = filtered_data[(filtered_data['Balance']>50000) & (filtered_data['Exited']==1)].shape[0] / filtered_data[filtered_data['Balance']>50000].shape[0]
credit_card_stickiness = filtered_data.groupby('HasCrCard')['Exited'].mean().iloc[0]

st.title("🏦 European Bank Customer Retention Dashboard")
st.subheader("Executive Summary")
st.markdown("""
- This dashboard analyzes churn based on **engagement profiles, product depth, and high-value customer behavior**.
- Focus is on identifying **disengaged but high-balance customers**, product utilization patterns, and engagement-driven retention.
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Engagement Retention Ratio", f"{round(engagement_retention_ratio,2)}")
col2.metric("Product Depth Index", f"{round(product_depth_index,2)}")
col3.metric("High-Balance Disengagement Rate", f"{round(high_balance_disengagement_rate,2)}")
col4.metric("Credit Card Stickiness", f"{round(credit_card_stickiness,2)}")

# ----------------------
# 5. Churn Rate by Engagement Profile (Interactive Bar)
# ----------------------
st.subheader("Churn Rate by Engagement Profile")
engagement_churn = filtered_data.groupby('EngagementProfile')['Exited'].mean().reset_index()
fig1 = px.bar(engagement_churn, x='EngagementProfile', y='Exited', text='Exited', color='Exited', color_continuous_scale='Viridis')
fig1.update_layout(xaxis_title="Engagement Profile", yaxis_title="Churn Rate")
st.plotly_chart(fig1, use_container_width=True)

# ----------------------
# 6. Churn Rate by Number of Products
# ----------------------
st.subheader("Churn Rate by Number of Products")
products_churn = filtered_data.groupby('NumOfProducts')['Exited'].mean().reset_index()
fig2 = px.bar(products_churn, x='NumOfProducts', y='Exited', text='Exited', color='Exited', color_continuous_scale='Plasma')
fig2.update_layout(xaxis_title="Number of Products", yaxis_title="Churn Rate")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------
# 7. High-Value Disengaged Customers
# ----------------------
st.subheader("High-Value Disengaged Customers")
high_value_disengaged = filtered_data[(filtered_data['IsActiveMember']==0) & (filtered_data['Balance']>50000)]
st.dataframe(high_value_disengaged)
csv = high_value_disengaged.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "high_value_disengaged.csv", "text/csv")

# ----------------------
# 8. Heatmap: Retention by Engagement vs Products
# ----------------------
st.subheader("Retention Heatmap: Engagement vs Products")
heatmap_data = filtered_data.pivot_table(index='EngagementProfile', columns='NumOfProducts', values='Exited', aggfunc='mean')
fig3 = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='YlGnBu',
                 labels=dict(x="Number of Products", y="Engagement Profile", color="Churn Rate"))
st.plotly_chart(fig3, use_container_width=True)
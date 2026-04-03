import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# 1. Load Data
# ----------------------
data = pd.read_excel(r"European_Bank.xlsx")

# ----------------------
# 2. Engagement Profile
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

geography = st.sidebar.multiselect(
    "Geography", data['Geography'].unique(), default=data['Geography'].unique()
)

gender = st.sidebar.multiselect(
    "Gender", data['Gender'].unique(), default=data['Gender'].unique()
)

balance_range = st.sidebar.slider(
    "Balance Range",
    float(data['Balance'].min()),
    float(data['Balance'].max()),
    (float(data['Balance'].min()), float(data['Balance'].max()))
)

products_range = st.sidebar.slider(
    "Number of Products",
    int(data['NumOfProducts'].min()),
    int(data['NumOfProducts'].max()),
    (int(data['NumOfProducts'].min()), int(data['NumOfProducts'].max()))
)

# Apply Filters
filtered_data = data[
    (data['Geography'].isin(geography)) &
    (data['Gender'].isin(gender)) &
    (data['Balance'] >= balance_range[0]) &
    (data['Balance'] <= balance_range[1]) &
    (data['NumOfProducts'] >= products_range[0]) &
    (data['NumOfProducts'] <= products_range[1])
]

# ----------------------
# 4. KPIs
# ----------------------
active_churn = filtered_data[filtered_data['IsActiveMember']==1]['Exited'].mean()
inactive_churn = filtered_data[filtered_data['IsActiveMember']==0]['Exited'].mean()

engagement_retention_ratio = active_churn / inactive_churn if inactive_churn != 0 else 0

product_depth_index = filtered_data['NumOfProducts'].mean()

high_balance = filtered_data[filtered_data['Balance'] > 50000]

high_balance_disengagement_rate = (
    high_balance[high_balance['Exited']==1].shape[0] /
    max(high_balance.shape[0], 1)
)

cc_yes = filtered_data[filtered_data['HasCrCard']==1]['Exited'].mean()
cc_no = filtered_data[filtered_data['HasCrCard']==0]['Exited'].mean()

credit_card_stickiness = cc_no - cc_yes

# ----------------------
# 5. Relationship Strength (NEW)
# ----------------------
filtered_data['RelationshipStrength'] = (
    filtered_data['IsActiveMember'] * 0.5 +
    (filtered_data['NumOfProducts'] / 4) * 0.5
)

relationship_strength_index = filtered_data['RelationshipStrength'].mean()

# ----------------------
# 6. Dashboard Title
# ----------------------
st.title("🏦 Customer Engagement & Retention Dashboard")

st.markdown("### 📌 Executive Summary")
st.markdown("""
- Engagement and product usage drive customer retention more than financial strength  
- Identifies high-risk, high-value customers  
- Supports data-driven retention strategies  
""")

st.markdown("---")

# ----------------------
# 7. KPI Display
# ----------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Engagement Retention Ratio", round(engagement_retention_ratio,2))
col2.metric("Product Depth Index", round(product_depth_index,2))
col3.metric("High-Balance Disengagement Rate", round(high_balance_disengagement_rate,2))
col4.metric("Credit Card Stickiness", round(credit_card_stickiness,2))
col5.metric("Relationship Strength Index", round(relationship_strength_index,2))

st.markdown("---")

# ----------------------
# 8. Insights
# ----------------------
st.markdown("### 🔍 Insights")

st.markdown(f"""
- Active churn: **{round(active_churn,2)}**  
- Inactive churn: **{round(inactive_churn,2)}**  

👉 Inactive customers are **{round(engagement_retention_ratio,2)}x more likely to churn**
""")

st.markdown("---")

# ----------------------
# 9. Engagement vs Churn
# ----------------------
st.subheader("📊 Churn by Engagement Profile")

engagement_churn = filtered_data.groupby('EngagementProfile')['Exited'].mean().reset_index()

fig1 = px.bar(
    engagement_churn,
    x='EngagementProfile',
    y='Exited',
    text='Exited'
)

fig1.update_traces(texttemplate='%{text:.2%}')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ----------------------
# 10. Product vs Churn
# ----------------------
st.subheader("📊 Churn by Number of Products")

products_churn = filtered_data.groupby('NumOfProducts')['Exited'].mean().reset_index()

fig2 = px.bar(
    products_churn,
    x='NumOfProducts',
    y='Exited',
    text='Exited'
)

fig2.update_traces(texttemplate='%{text:.2%}')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ----------------------
# 11. Financial vs Engagement
# ----------------------
st.subheader("💰 Financial vs Engagement Analysis")

filtered_data['EngagementScore'] = (
    filtered_data['IsActiveMember'] + filtered_data['NumOfProducts']
)

fig_fin = px.scatter(
    filtered_data,
    x="Balance",
    y="EngagementScore",
    color="Exited"
)

st.plotly_chart(fig_fin, use_container_width=True)

st.markdown("---")

# ----------------------
# 12. High-Value Disengaged Customers
# ----------------------
st.subheader("🚨 High-Value Disengaged Customers")

high_value_disengaged = filtered_data[
    (filtered_data['IsActiveMember'] == 0) &
    (filtered_data['Balance'] > filtered_data['Balance'].quantile(0.75))
]

st.dataframe(high_value_disengaged)

csv = high_value_disengaged.to_csv(index=False).encode('utf-8')

st.download_button(
    "Download CSV",
    csv,
    "high_value_disengaged.csv",
    "text/csv"
)

st.markdown("---")

# ----------------------
# 13. Heatmap
# ----------------------
st.subheader("📊 Retention Heatmap")

heatmap_data = filtered_data.pivot_table(
    index='EngagementProfile',
    columns='NumOfProducts',
    values='Exited',
    aggfunc='mean'
)

fig3 = px.imshow(
    heatmap_data,
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ----------------------
# 14. Customer Segmentation
# ----------------------
st.subheader("📊 Customer Segmentation")

segment_counts = filtered_data['EngagementProfile'].value_counts().reset_index()
segment_counts.columns = ['EngagementProfile', 'Count']

fig4 = px.pie(segment_counts, names='EngagementProfile', values='Count')

st.plotly_chart(fig4, use_container_width=True)

# ----------------------
# 15. Recommendations
# ----------------------
st.subheader("📌 Key Insights & Recommendations")

st.markdown("""
### Key Insights
- Low product usage → highest churn risk  
- Inactive high-balance customers → silent churn  
- Product bundling improves retention  

### Recommended Actions
- 🎯 Target high-value inactive customers  
- 📦 Promote cross-selling strategies  
- 🎁 Build engagement-based loyalty programs  
""")
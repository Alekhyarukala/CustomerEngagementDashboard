import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")

# ----------------------
# 1. Load Data
# ----------------------
@st.cache_data
def load_data():
    return pd.read_excel("European_Bank.xlsx")

data = load_data()

# ----------------------
# 2. Feature Engineering
# ----------------------

def engagement_profile(row):
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
        return "Active Engaged"
    elif row['IsActiveMember'] == 1:
        return "Active Low-Product"
    elif row['Balance'] > 50000:
        return "Inactive High-Balance"
    else:
        return "Inactive Disengaged"

data['EngagementProfile'] = data.apply(engagement_profile, axis=1)

# Age Group
data['AgeGroup'] = pd.cut(
    data['Age'],
    bins=[18, 30, 45, 60, 100],
    labels=['18-30', '30-45', '45-60', '60+']
)

# Risk Score
data['RiskScore'] = (
    (1 - data['IsActiveMember']) * 0.4 +
    (1 / (data['NumOfProducts'] + 1)) * 0.3 +
    (data['Balance'] > 50000).astype(int) * 0.3
)

# Relationship Strength
data['RelationshipStrength'] = (
    data['IsActiveMember'] * 0.5 +
    (data['NumOfProducts'] / 4) * 0.5
)

# ----------------------
# 3. Sidebar Filters
# ----------------------
st.sidebar.title("🔎 Filters")

geography = st.sidebar.multiselect(
    "Geography", data['Geography'].unique(), default=data['Geography'].unique()
)

gender = st.sidebar.multiselect(
    "Gender", data['Gender'].unique(), default=data['Gender'].unique()
)

age_group = st.sidebar.multiselect(
    "Age Group", data['AgeGroup'].unique(), default=data['AgeGroup'].unique()
)

balance_range = st.sidebar.slider(
    "Balance",
    float(data['Balance'].min()),
    float(data['Balance'].max()),
    (float(data['Balance'].min()), float(data['Balance'].max()))
)

products_range = st.sidebar.slider(
    "Products",
    int(data['NumOfProducts'].min()),
    int(data['NumOfProducts'].max()),
    (int(data['NumOfProducts'].min()), int(data['NumOfProducts'].max()))
)

# Apply Filters
filtered_data = data[
    (data['Geography'].isin(geography)) &
    (data['Gender'].isin(gender)) &
    (data['AgeGroup'].isin(age_group)) &
    (data['Balance'].between(balance_range[0], balance_range[1])) &
    (data['NumOfProducts'].between(products_range[0], products_range[1]))
]

# ----------------------
# 4. Title
# ----------------------
st.title("🏦 Customer Engagement & Retention Dashboard")

st.markdown("""
### 📌 Executive Summary
- Engagement > Financial strength for retention  
- Multi-product users are more loyal  
- Identifies high-risk high-value customers  
""")

# ----------------------
# 5. Tabs
# ----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "👥 Engagement",
    "📦 Products",
    "🚨 Risk Analysis"
])

# ----------------------
# TAB 1: OVERVIEW
# ----------------------
with tab1:
    st.subheader("📊 KPI Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Churn Rate", round(filtered_data['Exited'].mean(), 2))
    col2.metric("Avg Products", round(filtered_data['NumOfProducts'].mean(), 2))
    col3.metric("Avg Risk Score", round(filtered_data['RiskScore'].mean(), 2))
    col4.metric("Relationship Strength", round(filtered_data['RelationshipStrength'].mean(), 2))

    st.subheader("📈 Balance Distribution")
    fig = px.histogram(filtered_data, x="Balance")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# TAB 2: ENGAGEMENT
# ----------------------
with tab2:
    st.subheader("📊 Engagement vs Churn")

    fig1 = px.box(
        filtered_data,
        x="EngagementProfile",
        y="Balance",
        color="Exited"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Age Group vs Churn")

    age_churn = filtered_data.groupby('AgeGroup')['Exited'].mean().reset_index()

    fig2 = px.bar(age_churn, x='AgeGroup', y='Exited', text='Exited')
    fig2.update_traces(texttemplate='%{text:.2%}')
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------
# TAB 3: PRODUCTS
# ----------------------
with tab3:
    st.subheader("📊 Products vs Churn")

    prod_churn = filtered_data.groupby('NumOfProducts')['Exited'].mean().reset_index()

    fig3 = px.bar(prod_churn, x='NumOfProducts', y='Exited', text='Exited')
    fig3.update_traces(texttemplate='%{text:.2%}')
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📊 Products vs Balance")

    fig4 = px.scatter(
        filtered_data,
        x="NumOfProducts",
        y="Balance",
        color="Exited",
        size="RiskScore"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ----------------------
# TAB 4: RISK ANALYSIS
# ----------------------
with tab4:
    st.subheader("🚨 High Risk Customers")

    high_risk = filtered_data.sort_values(by="RiskScore", ascending=False).head(10)
    st.dataframe(high_risk)

    csv = high_risk.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download High Risk Customers",
        csv,
        "high_risk_customers.csv",
        "text/csv"
    )

    st.subheader("📊 Risk Score Distribution")

    fig5 = px.histogram(filtered_data, x="RiskScore")
    st.plotly_chart(fig5, use_container_width=True)

# ----------------------
# 6. Final Recommendations
# ----------------------
st.markdown("---")

st.subheader("📌 Key Insights & Recommendations")

st.markdown("""
### 🔍 Key Insights
- Low engagement → highest churn  
- High-balance inactive customers → silent churn  
- More products → higher retention  

### 🚀 Recommendations
- 🎯 Target high-risk customers  
- 📦 Increase product cross-selling  
- 🎁 Introduce loyalty programs  
- 📊 Use behavioral analytics for decision making  
""")
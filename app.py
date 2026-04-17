import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Retention Intelligence", layout="wide")

# ----------------------
# 🎨 COLORS
# ----------------------
PRIMARY = "#4F46E5"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#F59E0B"
NEUTRAL = "#6B7280"
BG = "#F9FAFB"

COLOR_MAP = {
    0: SUCCESS,
    1: DANGER
}

# ----------------------
# 🎨 PREMIUM UI
# ----------------------
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background: linear-gradient(180deg, #F9FAFB 0%, #EEF2FF 100%);
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 1rem;
}}

h1 {{
    text-align: center !important;
    color: #111827 !important;
    font-weight: 700;
    margin-bottom: 2rem;
}}

.metric-card {{
    background: white;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    transition: 0.25s ease;
}}

.metric-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.08);
}}

.metric-card h4 {{
    color: {NEUTRAL};
    font-size: 13px;
}}

.metric-card h3 {{
    font-size: 26px;
    font-weight: 700;
    margin: 0;
}}

.kpi-red {{ border-top: 4px solid {DANGER}; }}
.kpi-green {{ border-top: 4px solid {SUCCESS}; }}
.kpi-yellow {{ border-top: 4px solid {WARNING}; }}
.kpi-blue {{ border-top: 4px solid {PRIMARY}; }}

.stTabs [role="tab"] {{
    font-size: 14px;
    padding: 10px 20px;
    border-radius: 10px;
    transition: 0.2s;
}}

.stTabs [role="tab"]:hover {{
    background-color: #EEF2FF;
}}

.stTabs [aria-selected="true"] {{
    background-color: #E0E7FF;
    color: {PRIMARY};
    font-weight: 600;
}}

.box {{
    background: white;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 4px solid {PRIMARY};
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}}

</style>
""", unsafe_allow_html=True)

# ----------------------
# LOAD DATA
# ----------------------
@st.cache_data
def load_data():
    return pd.read_excel("European_Bank.xlsx")

data = load_data()

# ----------------------
# FEATURE ENGINEERING (UNCHANGED)
# ----------------------
def engagement_profile(row):
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] >= 2:
        return "Active Engaged"
    elif row['IsActiveMember'] == 0 and row['Balance'] > 100000:
        return "Inactive High Value"
    elif row['IsActiveMember'] == 1:
        return "Active Low Product"
    else:
        return "Disengaged"

data['EngagementProfile'] = data.apply(engagement_profile, axis=1)

data['ProductDepthIndex'] = data['NumOfProducts'] / data['NumOfProducts'].max()

data['RiskScore'] = (
    (1 - data['IsActiveMember']) * 0.5 +
    (1 / (data['NumOfProducts'] + 1)) * 0.2 +
    (data['Balance'] > 50000).astype(int) * 0.2 +
    (data['Age'] > 50).astype(int) * 0.1
)

data['RelationshipIndex'] = (
    data['IsActiveMember'] * 0.5 +
    data['ProductDepthIndex'] * 0.3 +
    (data['Tenure'] / data['Tenure'].max()) * 0.2
)

active_churn = data[data['IsActiveMember']==1]['Exited'].mean()
inactive_churn = data[data['IsActiveMember']==0]['Exited'].mean()

# ----------------------
# HEADER
# ----------------------
st.markdown("<h1>🏦 Customer Retention Intelligence Dashboard</h1>", unsafe_allow_html=True)

# ----------------------
# KPI
# ----------------------
c1,c2,c3,c4 = st.columns(4)

c1.markdown(f"<div class='metric-card kpi-red'><h4>Churn Rate</h4><h3>{data['Exited'].mean():.2%}</h3></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card kpi-green'><h4>Engagement Ratio</h4><h3>{(active_churn/inactive_churn):.2f}</h3></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card kpi-yellow'><h4>Product Depth</h4><h3>{data['ProductDepthIndex'].mean():.2f}</h3></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card kpi-blue'><h4>Relationship Index</h4><h3>{data['RelationshipIndex'].mean():.2f}</h3></div>", unsafe_allow_html=True)

# ----------------------
# CHART STYLE
# ----------------------
def style_chart(fig):
    fig.update_layout(
        height=360,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor=BG,
        font=dict(color="#374151"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor="#E5E7EB"),
        yaxis=dict(gridcolor="#E5E7EB")
    )
    return fig

# ----------------------
# TABS
# ----------------------
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(
["Overview","Engagement","Products","Risk","Prediction","Financial"]
)

# ----------------------
# OVERVIEW
# ----------------------
with tab1:
    fig = px.histogram(data, x="Balance", color_discrete_sequence=[PRIMARY])
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>Customer balances are widely distributed, but high balance alone does not prevent churn.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Some high-value customers still leave → indicating weak engagement.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Segment customers beyond financial metrics and include engagement indicators.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Design personalized retention strategies instead of generic campaigns.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Financial strength alone is not a reliable indicator of customer loyalty.")

# ----------------------
# ENGAGEMENT
# ----------------------
with tab2:
    fig = px.box(data, x="EngagementProfile", y="Balance",
                 color="Exited", color_discrete_map=COLOR_MAP)
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>Inactive customers exhibit significantly higher churn rates.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Even high-balance inactive users are at risk.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Improve customer engagement via mobile banking and notifications.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Introduce loyalty programs to encourage active usage.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Track inactivity signals and trigger re-engagement campaigns.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Customer engagement is the most critical factor driving retention.")

# ----------------------
# PRODUCTS
# ----------------------
with tab3:
    prod = data.groupby('NumOfProducts')['Exited'].mean().reset_index()
    fig = px.line(prod, x='NumOfProducts', y='Exited', markers=True)
    fig.update_traces(line=dict(color=WARNING, width=3))
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>Customers with only one product have the highest churn rate.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Multi-product customers show stronger retention.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Promote cross-selling strategies across customer segments.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Offer bundled financial products to increase dependency.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Target single-product users with personalized offers.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Product depth plays a crucial role in improving customer loyalty.")

# ----------------------
# RISK
# ----------------------
with tab4:
    fig = px.histogram(data, x="RiskScore", color_discrete_sequence=[DANGER])
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>Customers with high risk scores are more likely to churn.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Risk is driven by inactivity and low product usage.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Develop targeted retention campaigns for high-risk customers.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Use CRM tools to monitor risk signals continuously.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Offer incentives to reduce churn probability.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Risk scoring enables proactive identification of churn-prone customers.")

# ----------------------
# PREDICTION
# ----------------------
with tab5:
    threshold = st.slider("Risk Threshold", 0.0,1.0,0.5)
    data['PredictedChurn'] = data['RiskScore'] > threshold

    st.metric("Predicted Churn", f"{data['PredictedChurn'].mean():.2%}")

    fig = px.histogram(
        data,
        x="RiskScore",
        color="PredictedChurn",
        color_discrete_map={True:DANGER, False:SUCCESS}
    )
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>Predicted churn helps identify customers before actual exit.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Higher threshold reduces false positives but may miss risky users.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Use predictive analytics to intervene early.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Balance threshold carefully for optimal retention strategy.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Predictive models enable early intervention and reduce churn risk.")

# ----------------------
# FINANCIAL
# ----------------------
with tab6:
    fig = px.scatter(
        data,
        x="EstimatedSalary",
        y="Balance",
        color="Exited",
        color_discrete_map=COLOR_MAP
    )
    st.plotly_chart(style_chart(fig), width='stretch')

    st.markdown("### 💡 Insights")
    st.markdown("<div class='box'>High salary or balance does not guarantee retention.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Inactive premium customers represent hidden churn risk.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Recommendations")
    st.markdown("<div class='box'>Assign relationship managers to premium inactive customers.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Provide exclusive benefits to retain high-value clients.</div>", unsafe_allow_html=True)
    st.markdown("<div class='box'>Monitor financial inactivity signals closely.</div>", unsafe_allow_html=True)

    st.markdown("### 📌 Executive Summary")
    st.write("Financial strength without engagement leads to churn risk.")
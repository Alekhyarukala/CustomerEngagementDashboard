# Customer Engagement & Product Utilization Analytics Dashboard

Author: Alekhya Rukala  
Project Type: Data Analytics & Retention Strategy  
Tools: Python, Streamlit, Pandas, Matplotlib, Seaborn, Plotly  

---

## 📌 Project Overview

Banks often focus on demographics or account balances, but customer engagement and product utilization are key drivers of retention.

This project analyzes banking customer behavior to identify:

- Engagement patterns  
- Product usage impact on churn  
- High-value customers at risk  
- Actionable insights for retention strategies  

---

## 🚀 Live Demo

https://customerengagementdashboardgit-etkb6lqiqxgqtzacmerd2o.streamlit.app/

---

## 📊 Key Features / Dashboard Modules

### Churn Rate by Engagement Profile
Shows how active/inactive customers and product usage impact churn.

### Churn Rate by Number of Products
Shows retention differences between single-product and multi-product customers.

### High-Value Disengaged Customers
Identifies premium customers who may churn despite high balances.

### Key Performance Indicators (KPIs)

- Engagement Retention Ratio  
- Product Depth Index  
- High-Balance Disengagement Rate  
- Credit Card Stickiness Score  
- Relationship Strength Index  

### Advanced Features (New Version)

- Customer Risk Scoring Model  
- Interactive Tabs (Overview, Engagement, Products, Risk Analysis)  
- Age Group Segmentation  
- Dynamic Visualizations (Scatter, Histogram, Box Plots)  
- Top High-Risk Customer Identification  

### Interactive Filters

- Geography  
- Gender  
- Age Group  
- Balance Range  
- Number of Products  

---

## 📂 Dataset

File: European_Bank.xlsx  

Columns:
CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited  

---

## ⚡ How to Run Locally

git clone https://github.com/Alekhyarukala/CustomerEngagementDashboard.git
cd CustomerEngagementDashboard
pip install -r requirements.txt
streamlit run dashboard.py

---

## 🎯 Key Insights

- Low engagement leads to highest churn risk  
- Multi-product customers are more loyal  
- High-balance inactive customers show silent churn  
- Behavioral data is more powerful than financial data  

---

## 🚀 Business Recommendations

- Target high-risk customers with personalized offers  
- Promote cross-selling strategies  
- Introduce loyalty programs based on engagement  
- Shift to behavior-driven retention strategies  

---

## 💡 Project Impact

This project helps banks move from:

Traditional demographic analysis ➜ Behavior-driven retention analytics

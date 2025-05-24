import streamlit as st
import pandas as pd
import plotly.express as px

# Title and Description
st.set_page_config(layout="wide")
st.title("📚 EduGap: Visualizing the Digital Education Divide Post-Pandemic")
st.markdown("""
This dashboard highlights disparities in digital education access post-COVID across regions, genders, and income levels.  
Use the filters to explore insights by year, state, and demographics.
""")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("education.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
years = sorted(df['Year'].unique())
year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

# Filtered Data
filtered_df = df[
    (df['Year'] == year) &
    (df['Region'].isin(region)) &
    (df['Gender'].isin(gender))
]

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("📶 Avg. Internet Access", f"{filtered_df['InternetAccessPercent'].mean():.2f}%")
col2.metric("💻 Avg. Device Access", f"{filtered_df['DeviceAccessPercent'].mean():.2f}%")
col3.metric("📉 Avg. Dropout Rate", f"{filtered_df['DropoutRate'].mean():.2f}%")

# Plot 1: Internet Access by State
st.subheader("🌐 Internet Access by State")
fig1 = px.bar(filtered_df, x="State", y="InternetAccessPercent", color="Region", barmode="group",
              title="Internet Access (%) by State and Region")
st.plotly_chart(fig1, use_container_width=True)

with st.expander("📝 Analysis: Internet Access Patterns"):
    st.markdown("""
    ### Key Observations:
    - **Urban-Rural Divide**: Urban areas consistently show higher internet access percentages
    - **Gender Gap**: In rural areas, males tend to have higher internet access than females
    - **Regional Variations**: Southern states generally show more equitable access across genders
    - **Policy Implication**: States with high urban-rural divide would benefit from targeted infrastructure investments
    """)

# Plot 2: Dropout Rate by State
st.subheader("📉 Dropout Rates by State")
fig2 = px.bar(filtered_df, x="State", y="DropoutRate", color="Gender", barmode="group",
              title="Dropout Rate (%) by State and Gender")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("📝 Analysis: Dropout Rate Patterns"):
    st.markdown("""
    ### Key Observations:
    - **Gender Correlation**: Female students in areas with low internet access show higher dropout rates
    - **Geographic Trends**: Northern states show higher variability in dropout rates between genders
    - **Digital Access Impact**: States with highest device access generally show lowest dropout rates
    - **Policy Implication**: Digital inclusion programs could significantly impact retention rates
    """)

# Plot 3: Time Series (Optional)
if 'Time' in df.columns:
    st.subheader("📈 Time Series: Device Access Over Time")
    time_fig = px.line(df[df['Region'].isin(region)], x="Time", y="DeviceAccessPercent", color="Region",
                       title="Device Access Trend Over Time")
    st.plotly_chart(time_fig, use_container_width=True)

# Correlation Analysis
st.subheader("📊 Correlation Analysis")
col1, col2 = st.columns(2)

with col1:
    st.write("#### Internet Access vs. Dropout Rate")
    fig_corr = px.scatter(filtered_df, x="InternetAccessPercent", y="DropoutRate", 
                     color="Gender", hover_data=["State", "Region"],
                     trendline="ols", 
                     title="Higher Internet Access Correlates with Lower Dropout Rates")
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    # Calculate correlation coefficient
    corr = filtered_df['InternetAccessPercent'].corr(filtered_df['DropoutRate'])
    st.metric("Correlation Coefficient", f"{corr:.2f}")
    
    st.markdown("""
    ### Key Insights:
    - **Negative Correlation**: As internet access increases, dropout rates typically decrease
    - **Digital Divide Impact**: States with lower internet penetration show consistently higher dropout rates
    - **Gender Gap**: The relationship varies significantly between genders, suggesting different barriers
    """)

# State Highlights
st.subheader("🔍 State-Level Insights")
col1, col2, col3 = st.columns(3)

# Highest internet access
highest_internet = filtered_df.loc[filtered_df['InternetAccessPercent'].idxmax()]
col1.markdown(f"""
### Highest Internet Access
**{highest_internet['State']} ({highest_internet['Region']}, {highest_internet['Gender']})**
- Internet Access: {highest_internet['InternetAccessPercent']:.1f}%
- Dropout Rate: {highest_internet['DropoutRate']:.1f}%
""")
    
# Lowest internet access
lowest_internet = filtered_df.loc[filtered_df['InternetAccessPercent'].idxmin()]
col2.markdown(f"""
### Lowest Internet Access
**{lowest_internet['State']} ({lowest_internet['Region']}, {lowest_internet['Gender']})**
- Internet Access: {lowest_internet['InternetAccessPercent']:.1f}%
- Dropout Rate: {lowest_internet['DropoutRate']:.1f}%
""")

# Highest dropout rate
highest_dropout = filtered_df.loc[filtered_df['DropoutRate'].idxmax()]
col3.markdown(f"""
### Highest Dropout Rate
**{highest_dropout['State']} ({highest_dropout['Region']}, {highest_dropout['Gender']})**
- Internet Access: {highest_dropout['InternetAccessPercent']:.1f}%
- Dropout Rate: {highest_dropout['DropoutRate']:.1f}%
""")

# Footer
st.markdown("---")
st.markdown("Built by [Paulu wilson]" )


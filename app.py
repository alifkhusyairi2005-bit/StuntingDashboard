import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Child Stunting Dashboard", layout="wide")

st.title("Child Malnutrition (Stunting) in Southeast Asia")
st.write("Data source: UNICEF-WHO-World Bank Joint Child Malnutrition Estimates (JME)")

df = pd.read_csv("stunting_child_sea.csv")

# Sidebar filters
st.sidebar.header("Filter Data")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

filtered_df = df[
    (df["Year"] == selected_year) &
    (df["Country"].isin(selected_countries))
]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Children Affected (K)",
    f"{filtered_df['Children Affected(K)'].sum():,.1f}"
)

col2.metric(
    "Average Prevalence (%)",
    f"{filtered_df['Prevalence %'].mean():.1f}%"
)

highest = filtered_df.loc[filtered_df["Prevalence %"].idxmax()]
col3.metric(
    "Highest Prevalence",
    f"{highest['Country']} ({highest['Prevalence %']}%)"
)

st.subheader(f"Dataset for {selected_year}")
st.dataframe(filtered_df, use_container_width=True)

# Bar chart: Prevalence
st.subheader("Stunting Prevalence by Country")

fig1 = px.bar(
    filtered_df,
    x="Country",
    y="Prevalence %",
    text="Prevalence %",
    title=f"Stunting Prevalence (%) in {selected_year}"
)

fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

# Bar chart: Children affected
st.subheader("Number of Children Affected")

fig2 = px.bar(
    filtered_df,
    x="Country",
    y="Children Affected(K)",
    text="Children Affected(K)",
    title=f"Children Affected by Stunting (Thousands) in {selected_year}"
)

fig2.update_traces(textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

# Trend line
st.subheader("Stunting Trend Over Time")

trend_df = df[df["Country"].isin(selected_countries)]

fig3 = px.line(
    trend_df,
    x="Year",
    y="Prevalence %",
    color="Country",
    markers=True,
    title="Stunting Prevalence Trend (2022–2024)"
)

st.plotly_chart(fig3, use_container_width=True)

# Insights
st.subheader("Key Insights")

if selected_year == 2024:
    st.write("""
    - Timor-Leste has the highest stunting prevalence.
    - Singapore has the lowest stunting prevalence.
    - Indonesia has the largest number of children affected due to its large population.
    - Several Southeast Asian countries still have stunting prevalence above 20%.
    """)

st.subheader("Recommendations")
st.write("""
- Focus nutrition programs on high-risk countries.
- Improve maternal and child nutrition support.
- Use data science to detect high-risk populations early.
- Monitor stunting trends using dashboards and yearly data.
""")

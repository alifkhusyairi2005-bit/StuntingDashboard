import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Child Stunting Dashboard", layout="wide")

st.title("Child Malnutrition (Stunting) in Southeast Asia")
st.write("Data source: UNICEF-WHO-World Bank Joint Child Malnutrition Estimates (JME)")

# Load data
df = pd.read_csv("stunting_child_sea.csv")

# Clean data types
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Children Affected(K)"] = pd.to_numeric(df["Children Affected(K)"], errors="coerce")
df["Prevalence %"] = pd.to_numeric(df["Prevalence %"], errors="coerce")

df = df.dropna(subset=["Year", "Country", "Children Affected(K)", "Prevalence %"])
df["Year"] = df["Year"].astype(int)

# Sidebar filters
st.sidebar.header("Filter Data")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years) - 1
)

countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

# Filter data
filtered_df = df[
    (df["Year"] == selected_year) &
    (df["Country"].isin(selected_countries))
]
def risk_level(prevalence):
    if prevalence >= 30:
        return "🔴 High Risk"
    elif prevalence >= 20:
        return "🟠 Moderate Risk"
    else:
        return "🟢 Low Risk"

filtered_df = filtered_df.copy()
filtered_df["Risk Level"] = filtered_df["Prevalence %"].apply(risk_level)
# KPIs
col1, col2, col3 = st.columns(3)

if not filtered_df.empty:
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
        f"{highest['Country']} ({highest['Prevalence %']:.1f}%)"
    )
else:
    col1.metric("Total Children Affected (K)", "No data")
    col2.metric("Average Prevalence (%)", "No data")
    col3.metric("Highest Prevalence", "No data")

# Dataset table
st.subheader(f"Dataset for {selected_year}")
display_df = filtered_df.reset_index(drop=True)
display_df.index = display_df.index + 1

st.dataframe(display_df, use_container_width=True)
# Bar chart: Prevalence
st.subheader("Stunting Prevalence by Country")

fig1 = px.bar(
    filtered_df,
    x="Country",
    y="Prevalence %",
    text="Prevalence %",
    title=f"Stunting Prevalence (%) in {selected_year}"
)

fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
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



# Trend line
st.subheader("Stunting Prevalence Trend Over Time")

trend_df = df[df["Country"].isin(selected_countries)]

fig3 = px.line(
    trend_df,
    x="Year",
    y="Prevalence %",
    color="Country",
    markers=True,
    title="Stunting Prevalence Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# Insights
st.subheader("Key Insights")

st.write(f"""
- The dashboard shows child stunting data for **{selected_year}**.
- Countries with higher prevalence percentages require stronger nutrition intervention.
- Countries with larger affected-child numbers may need wider national-scale support.
- Comparing prevalence and affected numbers helps identify both severity and population impact.
""")

# Recommendations
st.subheader("Recommendations")

st.write("""
- Prioritize nutrition programs in countries with high stunting prevalence.
- Improve maternal and child nutrition support.
- Use yearly data monitoring to track progress.
- Apply data analysis to identify high-risk countries and guide policy decisions.
""")

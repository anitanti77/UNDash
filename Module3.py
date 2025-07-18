# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


Primary_colors = ["#6F42C1", "#007BFF", "#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#E6E6FA", "#FFF0F5", "#F0FFF0", "#F0FFFF", "#FFFACD", "#E0FFFF", "#F5FFFA", "#FAFAD2", "#FFE4E1", "#F5F5DC", "#FFF5EE", "#FFEFD5"
]
Supporting_colors = ["#00CCCC", "#0DCAF0", "#17A2B8"]
Extended_colors = Primary_colors + Supporting_colors


st.set_page_config(
    page_title="UN Enrollment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("UNESCO Female Primary_colors‑Level Enrollment Dashboard")
st.markdown("""
**Data Source:**  
- **Bulk Download Service**: Stat Bulk Data Download Service, UNESCO UIS  
- **URI:** https://uis.unesco.org/bdds  
- **Dataset:** WDI (ID: SE.PRM.ENRL.FE.ZS)  

**License:** CC BY‑4.0  
**Aggregation Method:** Weighted average  
**Periodicity:** Annual  

**Long Definition:** Female pupils as a percentage of total pupils at Primary_colors level include enrollments in public and private schools.  
**Development Relevance:** A share > 50% indicates more girls enrolled.  
**Limitations:** Influenced by population gender ratio; use female‑to‑male enrollment rates for parity.
""")

# Loading in & cleaning data
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    engine = "xlrd" if str(path).lower().endswith(".xls") else "openpyxl"
    df = pd.read_excel(
        path,
        sheet_name="Data",
        skiprows=3,    
        engine=engine
    )
    # drop indicator columns
    df = df.drop(columns=["IndicatorName", "IndicatorCode"], errors="ignore")
  
    df = df.rename(columns={
        "Country Name": "country",
        "Country Code": "iso3"
    })
    # melt year‑columns
    year_cols = [c for c in df.columns if isinstance(c, str) and c.isdigit()]
    df_long = df.melt(
        id_vars=["country", "iso3"],
        value_vars=year_cols,
        var_name="Year",
        value_name="EnrollPct"
    )
    df_long["Year"] = df_long["Year"].astype(int)
    df_long["EnrollPct"] = pd.to_numeric(df_long["EnrollPct"], errors="coerce")
    return df_long.dropna(subset=["EnrollPct"])


DATA_PATH = Path(__file__).parent / "API_SE.PRM.ENRL.FE.ZS_DS2_en_excel_v2_20757.xls"
df = load_data(DATA_PATH)

# Sidebar Filter
st.sidebar.header("Filters")
years = sorted(df["Year"].unique())
year = st.sidebar.slider(
    "Select Year",
    min_value=years[0],
    max_value=years[-1],
    value=years[-1]
)
countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df["country"].unique()),
    default=["United States", "China", "India"]
)


mask = (df["Year"] == year) & (df["country"].isin(countries))
df_sel = df[mask]

#  Global Map 
st.subheader(f"Global Enrollment % in {year}")
map_df = df[df["Year"] == year]

fig = px.choropleth(
    map_df,
    locations="iso3",
    color="EnrollPct",
    hover_name="country",
    color_continuous_scale=Supporting_colors,
    labels={"EnrollPct": "Enrollment %"}
)

# Formatting color bar
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Enrollment %",     
        thickness=30,             
        len=0.8,                  
        tickmode="auto",
        nticks=10,               
        ticks="outside",
        ticklen=5
    )
)

st.plotly_chart(fig, use_container_width=True)

# Two‑column layout for bar + line graph
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top {len(countries)} Countries by Enrollment")
    bar = px.bar(
        df_sel.sort_values("EnrollPct", ascending=False),
        x="EnrollPct",
        y="country",
        orientation="h",
        color="country",
        color_discrete_sequence=Primary_colors,
        labels={"EnrollPct": "Primary_colors Enrollment %", "country": ""}
    )
    st.plotly_chart(bar, use_container_width=True)

with col2:
    st.subheader("Trend Over Time")
    df_trend = df[df["country"].isin(countries)]
    line = px.line(
        df_trend,
        x="Year",
        y="EnrollPct",
        color="country",
        color_discrete_sequence=Extended_colors,
        labels={"EnrollPct": "Enrollment %", "country": "Country", "Year": "Year"},
        markers=True
    )
    st.plotly_chart(line, use_container_width=True)


# Slope Chart
with st.expander("Enrollment Change (Slope Chart)"):
    
    start_year = min(years)
    end_year   = year


    df_slope = df[
        (df["Year"].isin([start_year, end_year])) &
        (df["country"].isin(countries))
    ]

    fig = px.line(
        df_slope,
        x="Year", y="EnrollPct", color="country",
        color_discrete_sequence=Extended_colors,
        markers=True,
        labels={"EnrollPct": "Enrollment %", "country": "Country"},
        title=f"Change from {start_year} to {end_year}"
    )


    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[start_year, end_year],
            ticktext=[str(start_year), str(end_year)]
        ),
        legend_title_text=""  
    )

    st.plotly_chart(fig, use_container_width=True)

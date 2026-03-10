import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from reportlab.pdfgen import canvas
df = pd.read_csv("data.csv")
st.title("National Highway Financial & Environmental Impact Model")
highway = st.selectbox(
"Select Highway",
df["Highway"]
)

row = df[df["Highway"] == highway].iloc[0]
st.header("Highway Information")

st.write("State:",row["State"])
st.write("Developer:",row["Developer"])
st.write("CIN:",row["CIN"])
st.write("Mode:",row["Mode"])
st.write("Length (km):",row["Length_km"])
st.write("Lanes:",row["Lanes"])
st.header("Highway Information")

st.write("State:",row["State"])
st.write("Developer:",row["Developer"])
st.write("CIN:",row["CIN"])
st.write("Mode:",row["Mode"])
st.write("Length (km):",row["Length_km"])
st.write("Lanes:",row["Lanes"])
st.header("NH Route Map")

map = folium.Map(location=[25,80], zoom_start=6)

# Example route coordinates

route = [
[27.0,79.5],
[26.5,80.5],
[25.8,81.3],
[25.3,82.9]
]

folium.PolyLine(
route,
color="blue",
weight=5
).add_to(map)

st_folium(map,width=700)
traffic = st.slider(
"Daily Traffic",
10000,
100000,
int(row["Traffic"])
)

toll = st.slider(
"Toll per Vehicle",
50,
200,
int(row["Toll"])
)
construction_cost = row["Length_km"] * row["Cost_per_km"]

maintenance = row["Length_km"] * 0.25

revenue = traffic * toll * 365 / 1e7

benefit = revenue - maintenance

npv = benefit * 20 - construction_cost

bcr = (benefit * 20) / construction_cost
st.header("Financial Model Results")

st.write("Annual Revenue (Crore):",round(revenue,2))
st.write("Construction Cost:",construction_cost)
st.write("Maintenance Cost:",maintenance)
st.write("NPV:",round(npv,2))
st.write("BCR:",round(bcr,2))
emission_factor = 0.192

co2 = traffic * row["Length_km"] * emission_factor * 365 / 1000

st.header("Environmental Impact")

st.write("Annual CO2 Emission (tons):",round(co2,2))
growth = st.slider(
"Traffic Growth Rate",
0.01,
0.10,
0.05
)

years = list(range(1,21))

forecast=[]

for y in years:

    traffic_year = traffic*(1+growth)**y
    
    forecast.append(traffic_year)

fig,ax = plt.subplots()

ax.plot(years,forecast)

ax.set_title("Traffic Forecast")

ax.set_xlabel("Year")
ax.set_ylabel("Vehicles")

st.pyplot(fig)
def create_pdf():

    c = canvas.Canvas("reports/highway_report.pdf")
    
    c.drawString(100,750,"Highway Financial Impact Report")
    
    c.drawString(100,720,f"Highway: {highway}")
    
    c.drawString(100,700,f"Revenue: {revenue}")
    
    c.drawString(100,680,f"NPV: {npv}")
    
    c.drawString(100,660,f"BCR: {bcr}")
    
    c.save()

if st.button("Generate PDF Report"):

    create_pdf()

    st.success("Report Generated")
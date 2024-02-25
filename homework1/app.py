import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import plotly.express as px

project_id = 'cmpe255-homework1-415323'
service_account_file = './credentials.json'
credentials = service_account.Credentials.from_service_account_file(service_account_file)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

query = """
SELECT *
FROM `cmpe255-homework1-415323.medicare.outpatient_charges_2014_cleaned`
"""
query_job = client.query(query)
df = query_job.to_dataframe()

st.title('CMPE 255 Homework 1')
st.markdown("""
- **Name:** Rohit Vardam
- **SJSU ID:** 017437433
- **Original Dataset:** bigquery-public-data.medicare.outpatient_charges_2014
""")

st.header('Data Visualization')
st.subheader('Box Plot')
box_fig = px.box(df, x='provider_state', y='average_total_payments', title="Statewise Average Total Payments")
st.plotly_chart(box_fig, use_container_width=True)

st.subheader('Bar Graph')
grouped_data = df.groupby('apc')['outpatient_services'].sum().reset_index()
bar_fig = px.bar(grouped_data, x='apc', y='outpatient_services', text_auto=True, title="APC by Number of Outpatient Services")
st.plotly_chart(bar_fig, use_container_width=True)

st.subheader('Provider Map')
df_filtered = df.dropna(subset=['latitude', 'longitude'])
map_fig = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", size="average_estimated_submitted_charges",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3,
                            mapbox_style="carto-positron", title="Provider Locations and Average Estimated Submitted Charges")
st.plotly_chart(map_fig, use_container_width=True)

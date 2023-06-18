import streamlit as st
import geopandas as gpd
import pyproj
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

# gage data
gages = gpd.read_file(r'/Users/christianl/repos/ras-data/data/WF_OneRain_Gauges.shp')
map_df = gages 
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
# Create lat and lon columns
lat = map_df.geometry.y
lon = map_df.geometry.x
map_df['lat'] = lat
map_df['lon'] = lon
map_df = map_df[['lat','lon', 'SITE_ID', 'SITENAME']]

# results data
files = os.listdir(r'/Users/christianl/repos/ras-data/data')
dfs = {}
for file in files:
    if file.endswith('.csv'):
        dfs[file[:-4]] = pd.read_csv(os.path.join(r'/Users/christianl/repos/ras-data/data', file), index_col=0)

dfs = {file[:-4]: pd.read_csv(os.path.join(r'/Users/christianl/repos/ras-data/data', file), index_col=0) for file in files if file.endswith('.csv')}

ctrl = dfs['CTRL']
pr01 = dfs['PR01']
pr05 = dfs['PR05']
pr08 = dfs['PR08']
pr12 = dfs['PR12']
id01 = dfs['ID01']
id05 = dfs['ID05']
id12 = dfs['ID12']
md08 = dfs['MD08']
md09 = dfs['MD09']
imp08 = dfs['IMP08']
imp09 = dfs['IMP09']

# Observed data

st.title('Gage Results Visualization')
st.subheader(f'Map of Gage Locations')

fig = px.scatter_mapbox(map_df, lat="lat", lon="lon", zoom=10, height=500, hover_name="SITE_ID", hover_data=["SITENAME"], color_discrete_sequence=["fuchsia"], title='Gage Locations', labels={'SITE_ID':'Gage ID'})
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

st.header('Visualize gage results at different locations')

# allow user to select which location to display
location = st.selectbox('Select location:', gages['SITE_ID'].unique())

# filter the data to only show the selected location
location_data = gages.loc[gages['SITE_ID'] == location]

# display the gage results for the selected location
st.subheader(f'Initial Deficit Results for {location}')

fig_id = go.Figure()

fig_id.add_trace(go.Scatter(x=ctrl.index, y=ctrl[location], name='Control (CTRL)'))
fig_id.add_trace(go.Scatter(x=id01.index, y=id01[location], name='Initial Deficit 01 (ID01)'))
fig_id.add_trace(go.Scatter(x=id05.index, y=id05[location], name='Initial Deficit 05 (ID05)'))
fig_id.add_trace(go.Scatter(x=id12.index, y=id12[location], name='Initial Deficit 12 (ID12)'))

fig_id.update_layout(title=f'Initial Deficit Results for {location}',
                        xaxis_title='Time',
                        yaxis_title='Water Surface Elevation (ft)')

st.plotly_chart(fig_id)

st.subheader(f'Max Deficit Results for {location}')

fig_md = go.Figure()

fig_md.add_trace(go.Scatter(x=ctrl.index, y=ctrl[location], name='Control (CTRL)'))
fig_md.add_trace(go.Scatter(x=md08.index, y=md08[location], name='Max Deficit 08 (MD08)'))
fig_md.add_trace(go.Scatter(x=md09.index, y=md09[location], name='Max Deficit 09 (MD09)'))

fig_md.update_layout(title=f'Max Deficit Results for {location}',
                        xaxis_title='Time',
                        yaxis_title='Water Surface Elevation (ft)')
st.plotly_chart(fig_md)

st.subheader(f'Impervious Results for {location}')

fig_imp = go.Figure()

fig_imp.add_trace(go.Scatter(x=ctrl.index, y=ctrl[location], name='Control (CTRL)'))
fig_imp.add_trace(go.Scatter(x=imp08.index, y=imp08[location], name='Impervious 08 (IMP08)'))
fig_imp.add_trace(go.Scatter(x=imp09.index, y=imp09[location], name='Impervious 09 (IMP09)'))

fig_imp.update_layout(title=f'Impervious Results for {location}',
                        xaxis_title='Time',
                        yaxis_title='Water Surface Elevation (ft)')
st.plotly_chart(fig_imp)

st.subheader(f'Percolation Rate Results for {location}')

fig_pr = go.Figure()

fig_pr.add_trace(go.Scatter(x=ctrl.index, y=ctrl[location], name='Control (CTRL)'))
fig_pr.add_trace(go.Scatter(x=pr01.index, y=pr01[location], name='Percolation Rate 01 (PR01)'))
fig_pr.add_trace(go.Scatter(x=pr05.index, y=pr05[location], name='Percolation Rate 05 (PR05)'))
fig_pr.add_trace(go.Scatter(x=pr08.index, y=pr08[location], name='Percolation Rate 08 (PR08)'))
fig_pr.add_trace(go.Scatter(x=pr12.index, y=pr12[location], name='Percolation Rate 12 (PR12)'))

fig_pr.update_layout(title=f'Percolation Rate Results for {location}',
                        xaxis_title='Time',
                        yaxis_title='Water Surface Elevation (ft)')
st.plotly_chart(fig_pr)
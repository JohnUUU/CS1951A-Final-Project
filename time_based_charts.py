# import required packages
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import geopandas as gpd
from geopandas import GeoDataFrame
import json

# Settings and Background 
nyc_geojson = gpd.read_file("nyc.geojson")
px.set_mapbox_access_token("pk.eyJ1IjoiMTJqb2huMjciLCJhIjoiY2tzNjR2M3hrMzQ2ZzJwbzd1cHBiNzRqcCJ9.TcEREBGPtkbkqG8rOgr1Bg")
CUTOFF = 25

# Create and Modify Dataframes 
complex_df = pd.read_sql_table('complexes', 'sqlite:///database/final.db')
nr_df = pd.read_sql_table('new_ridership', 'sqlite:///database/final.db')
nr_df = pd.melt(nr_df, id_vars = ['dtidx'], value_vars = [x for x in nr_df.columns if x !='dtidx']) #
complex_df = complex_df.astype({'Complex ID': 'int64'})
nr_df = nr_df.astype({'variable': 'int64'})
df = pd.merge(complex_df, nr_df, left_on= 'Complex ID', right_on= 'variable')

df['dtidx'] = df['dtidx'].astype(str)
df = df.dropna()
df = df[abs(df['value']) < CUTOFF]
df['size'] = df['value'].abs()


print(df['dtidx'])

# Animated Graph 
def animate_map(time_col):
    fig = px.scatter_mapbox(df,
              lat="GTFS Latitude" ,
              lon="GTFS Longitude",
              hover_name="Complex ID",
              color="value",
              size = 'size', 
              animation_frame=time_col,
              mapbox_style='carto-positron',
              color_continuous_scale = ['red', 'blue'],
              range_color = (-1, 1),
              category_orders={
                    time_col:list(np.sort(df[time_col].unique()))
                },  
              title = "Percent Change in Ridership of NYC Stations (Cluster Plot)",
              labels = {"Complex ID" : "Complex ID", 'value' : 'Percent Change (Ridership)', 'modzcta' : 'Zip Code', 'dtidx' : 'Date', 'size' : "ABS Percent Change (Ridership)"},              
              zoom=10)
    fig.show();
animate_map(time_col='dtidx')



# # Marker Generator Funtion 
# def gen_marker(time, complex_id): 
#     data_frame = df['dtidx' == time]
    
#     # Create a pieplot
#     plt.pie(data_frame[['Complex ID', 'value']]['value'])

#     # add a circle at the center to transform it in a donut chart
#     my_circle=plt.Circle( (0,0), 0.7, color='white')
#     p=plt.gcf()
#     p.gca().add_artist(my_circle)

#     plt.show()

#     return time

# fig, ax = plt.subplots(figsize = (10,8))
# sns.color_palette("colorblind")

# nyc_geojson.boundary.plot(ax = ax, edgecolor = 'black')

# df = df.dropna()

# # set theft type as scatterplot color
# sns.scatterplot(x = df['GTFS Longitude'], y = df['GTFS Latitude'], marker = 'o', 
#                 hue = df['Borough'], alpha = 0.03, palette = 'colorblind', ax = ax)
                
# # move the legend to the right of the plot
# ax.legend(loc = 'center right', bbox_to_anchor=(1.7, 0.5), ncol=1) 

# ax.axis('off')
# plt.legend()
# ax.set_title("Location of Stations in NYC by Borough")
# plt.show()


# def gen_scatter(time): 
#     dataframe = df['dtidx' == time]
#     fig, ax = plt.subplots(figsize = (10,8))
#     sns.color_palette("colorblind")
#     nyc_geojson.boundary.plot(ax = ax, edgecolor = 'black')

#     # set theft type as scatterplot color
#     sns.scatterplot(x = dataframe['GTFS Longitude'], y = dataframe['GTFS Latitude'], marker = 'o', 
#                     hue = dataframe['value'], size = df['size'], ax = ax)
                    
#     # move the legend to the right of the plot
#     ax.legend(loc = 'center right', bbox_to_anchor=(1.7, 0.5), ncol=1) 

#     ax.axis('off')
#     plt.legend()
#     ax.set_title("Location of Stations in NYC by Borough")
#     plt.show()

# gen_scatter('2019-01-06')
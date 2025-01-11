import geopandas as gpd
import folium
from folium import plugins
import pandas as pd

# Load world map data
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file("ne_110m_admin_0_countries.zip")
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Sample data - replace this with your actual data
data = {
    'country': ['United States', 'Canada', 'Brazil', 'France', 'China'],
    'incidents': [100, 50, 75, 30, 200]
}
incidents_df = pd.DataFrame(data)

# Merge the data with the world map
# 'NAME' is the country column in the world GeoDataFrame
world = world.merge(incidents_df, how='left', left_on=['NAME'], right_on=['country'])

# Create a base map centered on (0, 0)
m = folium.Map(location=[0, 0], zoom_start=2)

# Add the choropleth layer
folium.Choropleth(
    geo_data=world,
    name='choropleth',
    data=incidents_df,
    columns=['country', 'incidents'],
    key_on='feature.properties.NAME',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of Incidents'
).add_to(m)

# Add tooltips
style_function = lambda x: {'fillColor': '#ffffff', 
                          'color':'#000000', 
                          'fillOpacity': 0.1, 
                          'weight': 0.1}

highlight_function = lambda x: {'fillColor': '#000000', 
                              'color':'#000000', 
                              'fillOpacity': 0.50, 
                              'weight': 0.1}

NIL = folium.features.GeoJson(
    world,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME', 'incidents'],
        aliases=['Country:', 'Incidents:'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)


m.add_child(NIL)
m.add_child(folium.LayerControl())

# Save the map
m.save('world_incidents_map.html')

import geopandas as gpd
import folium
from folium import plugins
import pandas as pd
import json

# Load world map data
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

# Sample data - replace this with your actual data
data = {
    'COUNTRY': ['United States of America', 'Canada', 'Brazil', 'France', 'China'],
    'incidents': [100, 50, 75, 30, 200],
    'additional_info': ['Info USA', 'Info Canada', 'Info Brazil', 'Info France', 'Info China']
}
incidents_df = pd.DataFrame(data)

# Merge the data with the world map
world = world.merge(incidents_df, how='left', left_on=['NAME'], right_on=['COUNTRY'])

# Create a base map centered on (0, 0)
m = folium.Map(location=[0, 0], zoom_start=2)

# Convert the entire world GeoDataFrame to GeoJSON
world_json = json.loads(world.to_json())

# Add choropleth layer first (background)
choropleth = folium.Choropleth(
    geo_data=world_json,
    name='choropleth',
    data=incidents_df,
    columns=['COUNTRY', 'incidents'],
    key_on='feature.properties.NAME',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of Incidents'
).add_to(m)

# Custom JavaScript for click handling
# Replace the custom_js with this version for a fancier popup
custom_js = """
<script>
function handleClick(countryName, incidents, info) {
    var content = `
        <div style="font-family: Arial; padding: 15px; min-width: 200px;">
            <h3 style="margin:0 0 10px 0; color: #2c3e50;">${countryName}</h3>
            <div style="border-bottom: 2px solid #eee; margin-bottom: 10px;"></div>
            <div style="margin-bottom: 5px;">
                <strong style="color: #e74c3c;">Incidents:</strong> 
                <span>${incidents || 'No data'}</span>
            </div>
            <div style="margin-bottom: 5px;">
                <strong style="color: #e74c3c;">Additional Info:</strong>
                <span>${info || 'No additional info'}</span>
            </div>
            <button onclick="showMoreDetails('${countryName}')" 
                    style="margin-top: 10px; padding: 5px 10px; 
                           background-color: #3498db; color: white; 
                           border: none; border-radius: 3px; 
                           cursor: pointer;">
                Show More Details
            </button>
        </div>
    `;
    
    var popup = L.popup()
        .setLatLng(event.latlng)
        .setContent(content)
        .openOn(map);
}

function showMoreDetails(countryName) {
    // Add your custom functionality here
    alert('Showing more details for ' + countryName);
    // Could open a modal, load additional data, etc.
}
</script>
"""

# Add custom JavaScript to the map
m.get_root().html.add_child(folium.Element(custom_js))

# Style function for the interactive layer
style_function = lambda x: {
    'fillColor': 'transparent',
    'color': '#000000',
    'weight': 1,
    'fillOpacity': 0
}

# Highlight function for hover effect
highlight_function = lambda x: {
    'fillColor': '#000000',
    'color': '#000000',
    'weight': 2,
    'fillOpacity': 0.3
}

# Add interactive GeoJSON layer
folium.GeoJson(
    world_json,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['NAME', 'incidents'],
        aliases=['Country:', 'Incidents:'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    ),
    name='Interactions',
).add_to(m)

# Add event listeners using JavaScript
m.get_root().html.add_child(folium.Element("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var geoJsonLayer = document.querySelector('.leaflet-interactive');
        if (geoJsonLayer) {
            geoJsonLayer.addEventListener('click', function(e) {
                var props = e.target.feature.properties;
                handleClick(props.NAME, props.incidents, props.additional_info);
            });
        }
    });
    </script>
"""))

# Add layer control
folium.LayerControl().add_to(m)

# Save the map
m.save('interactive_world_map.html')
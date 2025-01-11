import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load world map data
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file("ne_110m_admin_0_countries.zip")

# Sample data
data = {
    'country': ['United States', 'Canada', 'Brazil', 'France', 'China'],
    'incidents': [100, 50, 75, 30, 200]
}
incidents_df = pd.DataFrame(data)

# Merge the data
world = world.merge(incidents_df, how='left', left_on=['NAME'], right_on=['country'])

# Create the plot
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(column='incidents', 
          ax=ax,
          legend=True,
          legend_kwds={'label': 'Number of Incidents'},
          missing_kwds={'color': 'lightgrey'},
          cmap='YlOrRd')

# Remove axes
ax.axis('off')

# Add title
plt.title('World Map of Incidents')

# Save the plot
plt.savefig('world_incidents_map.png', dpi=300, bbox_inches='tight')
plt.show()
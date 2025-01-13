# import the necessary packages
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import geopandas as gpd
import warnings
# url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip"
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
# world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = gpd.read_file("ne_110m_admin_0_countries.zip")

# to use with https://app.simplenote.com/




import simplenote

sn = simplenote.Simplenote("juvarfe@gmail.com", "Horse House Harper")
a = sn.get_note_list(data=True,tags=[])
# print(a)
countries_note = sn.get_note("19decf27-0e18-441a-b7fe-58f6345e9913")[0]
# Write:
countries_note["content"]
content = countries_note["content"]
for a in world["NAME"]:
    if a not in content: content += "\n" + a

countries_note["content"] = content
sn.update_note(countries_note)

# Read
content_lines = countries_note["content"].split("\n")
country_list_start=False
for line in content_lines:
    if "start-" in line.lower(): country_list_start=True
    if "end-" in line.lower(): country_list_start=False
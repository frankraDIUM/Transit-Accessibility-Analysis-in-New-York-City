import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import warnings

warnings.filterwarnings("ignore", category=UserWarning)  #For noisy OSMnx warnings


# Settings
place = "New York City, New York, USA"
graph_type = "walk"		# walking network
crs_project  = "EPSG:2236" 	# NY Long Island NAD83 feet


# 1. Download walkable street network
print("Downloading street network...")
G = ox.graph_from_place(place, network_type=graph_type, simplify=True)

#Project the graph to a local CRS for accurate distances
G_projected = ox.project_graph(G, to_crs=crs_project)

# Save nodes and edges as GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G_projected)

print(f"Downloaded {len(nodes)} nodes and {len(edges)} edges")

# 2. Download subway entrancesusing OSM tags
print("Downloading subway entrances....")
subway_entrances = ox.features_from_place(
	place,
	tags={'railway':'subway_entrance'}
)

if not subway_entrances.empty:
	subway_entrances = subway_entrances.to_crs(crs_project)
	print(f"Found {len(subway_entrances)} subway entrances")
else:
    print("Warning: No subway entrances found - check tags or bounding box")

# Plot

ox.plot_graph(G_projected, node_size=0, edge_linewidth=0.5)
if not subway_entrances.empty:
    ax = subway_entrances.plot(color='red', markersize=20, figsize=(10,10))
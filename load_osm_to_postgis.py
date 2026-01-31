import osmnx as ox
import geopandas as gpd
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Connect to database

DB_USER = "postgres"           
DB_PASS = "####"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nyc_transit_access"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


# Load the data you just downloaded
place = "New York City, New York, USA"
G = ox.graph_from_place(place, network_type="walk", simplify=True)
G_projected = ox.project_graph(G, to_crs="EPSG:2263")  # NY state plane feet

nodes_gdf, edges_gdf = ox.graph_to_gdfs(G_projected)

subway_entrances = ox.features_from_place(
    place,
    tags={'railway': 'subway_entrance'}
).to_crs("EPSG:2263")


# Write to PostGIS

print("Writing nodes...")
nodes_gdf.to_postgis(
    name="osm_nodes",
    con=engine,
    if_exists="replace",
    index=False
)

print("Writing edges...")
edges_gdf.to_postgis(
    name="osm_edges",
    con=engine,
    if_exists="replace",
    index=False
)

print("Writing subway entrances...")
subway_entrances.to_postgis(
    name="subway_entrances",
    con=engine,
    if_exists="replace",
    index=False
)

print("Done! Tables created: osm_nodes, osm_edges, subway_entrances")
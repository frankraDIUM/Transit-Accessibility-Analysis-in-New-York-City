-- SANITY CHECKS
-- Basic row counts

SELECT 'osm_nodes' AS table_name, COUNT(*) AS row_count FROM osm_nodes
UNION ALL
SELECT 'osm_edges', COUNT(*) FROM osm_edges
UNION ALL
SELECT 'subway_entrances', COUNT(*) FROM subway_entrances;


-- Check CRS / SRID of geometries

SELECT 
    'osm_nodes' AS table_name, 
    ST_SRID(geometry) AS srid, 
    COUNT(*) AS features_with_srid
FROM osm_nodes
GROUP BY ST_SRID(geometry)

UNION ALL

SELECT 
    'osm_edges', 
    ST_SRID(geometry), 
    COUNT(*)
FROM osm_edges
GROUP BY ST_SRID(geometry)

UNION ALL

SELECT 
    'subway_entrances', 
    ST_SRID(geometry), 
    COUNT(*)
FROM subway_entrances
GROUP BY ST_SRID(geometry);


-- Check for invalid geometries

SELECT 
    table_name,
    COUNT(*) AS invalid_geoms
FROM (
    SELECT 'osm_nodes' AS table_name, geometry FROM osm_nodes
    UNION ALL
    SELECT 'osm_edges', geometry FROM osm_edges
    UNION ALL
    SELECT 'subway_entrances', geometry FROM subway_entrances
) t
WHERE NOT ST_IsValid(geometry)
GROUP BY table_name;


-- Quick look at subway entrances (sample)

SELECT 
    row_number() OVER () AS temp_row_id,          -- temporary identifier (1,2,3...)
    ST_AsText(geometry) AS geom_wkt,
    ST_SRID(geometry) AS srid,
    railway,
    name,
    entrance,
    highway,                                      -- often null for entrances
    wheelchair,
    level
FROM subway_entrances
LIMIT 10;



-- Edges table structure & sample lengths

SELECT 
    osmid,                          -- OSM way ID
    name,
    highway,
    oneway,
    length AS original_length_m,    -- OSMnx added this in meters
    ST_Length(geometry) AS length_feet_current,   -- recalculated in feet (EPSG:2263)
    ST_AsText(geometry) AS geom_wkt_sample   -- first few chars only if too long
FROM osm_edges
LIMIT 10;


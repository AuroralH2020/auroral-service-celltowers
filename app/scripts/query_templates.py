# Inserting cell data into the database with check if point is in country for given mcc
insertCells = """ 
INSERT INTO cell_towers ( cellid, mcc, radio, net, range, samples, changable, created, updated, lat, lon, geo )
SELECT * FROM (
 VALUES ({{ cellid }}, {{ mcc }} , '{{ radio }}', {{ net }}, {{ range }}, {{ samples }}, {{ changable }}, to_timestamp({{ created }}), to_timestamp({{ updated }}), {{ lat }}, {{ lon }}, ST_Buffer(ST_MakePoint({{ lon }}, {{ lat }})::geography, {{ range }}))
 )
	AS t (integer, integer, smallint, integer, boolean, timestamp, timestamp, float, float, geography)
WHERE (
  SELECT count(*)
  FROM countries
  WHERE ST_Contains(geo::geometry, ST_SetSRID(ST_MakePoint({{ lon }}, {{ lat }}), 4326)) AND mcc = {{ mcc }}
) > 0
ON CONFLICT DO NOTHING;
"""
# 10 nearest cells for a given location
requestNearbyCells = """ 
SELECT 
	cellid,
	ST_Distance(ST_MakePoint({{ lon }}, {{ lat }})::geography, ST_MakePoint(lon, lat)::geography) as distance,
	range,
	ST_MakePoint(lon, lat)::geography,
    lat,
    lon
	FROM public.cell_towers
WHERE ST_DWithin(geo, ST_MakePoint({{ lon }}, {{ lat }})::geography, 1, false)
ORDER BY  distance
LIMIT 10
"""


generateCountrySignalGrid = """
-- Remove old data
DELETE FROM signal_grid WHERE mcc = {{ mcc }};

-- Insert new data
INSERT INTO signal_grid(radio_total, radio_GSM, radio_LTE, radio_UMTS, countryCode, mcc, geom)
WITH RECURSIVE
	countryPolygon as (SELECT geo, code, mcc FROM public.countries WHERE mcc = '{{ mcc }}' ),
	grid AS (SELECT (ST_HexagonGrid(0.05, geo::geometry)).*, code as code, mcc FROM countryPolygon),
	customGrid AS (SELECT grid.code, grid.mcc, geom from grid RIGHT OUTER JOIN countryPolygon ON ST_Intersects(countryPolygon.geo, grid.geom)),
	towers AS (SELECT * from public.cell_towers WHERE mcc={{ mcc }})
SELECT 
	COUNT(radio) as radio_total,
	COUNT(radio) FILTER (WHERE c.radio = 'GSM') AS radio_GSM,
	COUNT(radio) FILTER (WHERE c.radio = 'LTE') AS radio_LTE,
	COUNT(radio) FILTER (WHERE c.radio = 'UMTS') AS radio_UMTS,
	customGrid.code as countryCode,
	customGrid.mcc as mcc,
	customGrid.geom as geom
-- 	ST_AsText(ST_Centroid(fGrid.geom)) as center
FROM towers as c
RIGHT OUTER JOIN customGrid
ON ST_Intersects(c.geo, customGrid.geom)
GROUP BY customGrid.geom, customGrid.code, customGrid.mcc
"""
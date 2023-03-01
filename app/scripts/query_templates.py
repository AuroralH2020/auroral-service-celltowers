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
groupCountries = """ 
SELECT 
	name,
	code, 
	c.mcc,
	COUNT(c.mcc) as hexagons
FROM public.countries as c 
INNER JOIN signal_grid ON c.mcc = signal_grid.mcc
GROUP BY name, code, c.mcc
"""

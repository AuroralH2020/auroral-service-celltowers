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
	ST_MakePoint(lon, lat)::geography 
	FROM public.cell_towers
WHERE ST_DWithin(geo, ST_MakePoint({{ lon }}, {{ lat }})::geography, 1, false)
ORDER BY  distance
LIMIT 10
"""
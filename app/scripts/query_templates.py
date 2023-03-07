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
WITH RECURSIVE towers AS
  (SELECT cellid,
          mcc,
          radio,
          net,
          ST_Distance(ST_MakePoint({{ lon }}, {{ lat }})::geography, ST_MakePoint(lon, lat)::geography) AS distance,
          RANGE,
          ST_MakePoint(lon, lat)::geography,
          lat,
          lon
   FROM public.cell_towers
   WHERE ST_DWithin(geo, ST_MakePoint({{ lon }}, {{ lat }})::geography, 1, FALSE)
   ORDER BY distance
   LIMIT 5)
SELECT towers.cellid,
       distance,
       RANGE,
       radio,
       st_makepoint,
       lat,
       lon,
       operators.name AS Operator,
       operators.country_code AS CountryCode,
	   countries.name as CountryName
FROM towers
LEFT OUTER JOIN public.operators ON towers.mcc=operators.mcc AND towers.net=operators.mnc
LEFT OUTER JOIN public.countries ON operators.country_code=countries.code
"""
groupCountries = """ 
WITH RECURSIVE
	mergedCountries as (SELECT mcc, MIN(name) as name, MIN(code) as code, ST_Envelope(ST_Union(boundingBox)) as box from public.countries GROUP BY mcc
)
SELECT 
	MIN(name) as name,
	MIN(code) as code, 
	c.mcc,
	ST_AsGeoJSON(MIN((c.box))::geometry) as box,
	ST_X(ST_Centroid(MIN(c.box))) as center_lon,
	ST_Y(ST_Centroid(MIN(c.box))) as center_lat,
	COUNT(c.mcc) as hexagons
FROM mergedCountries as c 
INNER JOIN signal_grid ON c.mcc = signal_grid.mcc
GROUP BY c.mcc
ORDER BY name
"""
generateCountrySignalGrid = """
-- Remove old data
DELETE FROM signal_grid WHERE mcc = {{ mcc }};

-- Insert new data
INSERT INTO signal_grid(radio_total, radio_GSM, radio_LTE, radio_UMTS, countryCode, mcc, geojson, geom)
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
    ST_AsGeoJSON(customGrid.geom) as geojson,
	customGrid.geom as geom
    
-- 	ST_AsText(ST_Centroid(fGrid.geom)) as center
FROM towers as c
RIGHT OUTER JOIN customGrid
ON ST_Intersects(c.geo, customGrid.geom)
GROUP BY customGrid.geom, customGrid.code, customGrid.mcc
"""

getLoadedCountriesCellTowers= """
SELECT 
	c.mcc,
	countries.code,
	countries.name
FROM public.cell_towers as c
INNER JOIN countries ON countries.mcc=c.mcc
GROUP BY c.mcc, countries.code, countries.name
"""
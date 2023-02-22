import psycopg2
import time
import sys
import json

dbuser = "postgres"
dbpassword = "test"
dbhost = "localhost"
dbport = "5432"
dbname = "postgres"
# Tweaks
clean_db = True
border_file = 'world_countries.geojson'

# Country codes and MCCs
countryMcc = {
    'SK': 231, 'NO': 242, 'CZ': 230, 'DE': 262, 'AT': 232, 'PO': 260, 'HU': 216, 'RO': 226,
    'DK': 238, 'FI': 244, 'SE': 240, 'NL': 204, 'BE': 206, 'FR': 208, 'ES': 214, 'GB': 235,
    'IT': 222, 'CH': 228, 'GR': 202,
}

# store time to measure performance
start = time.time()

# queries
queries = []
def main():
    prepareDb()
    getCountriesFromFile()
    print("Number of queries: " + str(len(queries)))
    # run everything in sequence
    insertToDb(queries)
    print("\nRun time: " + str(time.time() - start))
    

def prepareDb():
    # connect to postgres
    conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " host=" + dbhost + " password=" + dbpassword + " port=" + dbport)
    # create a cursor
    cur = conn.cursor()
    # drop table if exists
    if clean_db:
        cur.execute("DROP TABLE IF EXISTS countries;")
        cur.execute("DROP INDEX IF EXISTS countries_geo_gist;")
    cur.execute("CREATE TABLE IF NOT EXISTS countries (code varchar(2), name varchar(40), mcc integer, geo geography);")
    cur.execute("CREATE INDEX IF NOT EXISTS countries_geo_gist ON countries USING GIST (geo);")
    cur.execute("CREATE INDEX IF NOT EXISTS countries_mcc_idx ON countries (mcc);")
    cur.close()
    conn.commit()

def getCountriesFromFile():
    global queries
    print("Reading countries from file")
    # import with geoJSON
    with open(border_file) as f:
        data = json.load(f)
    for feature in data['features']:
        code = feature['properties']['ISO']
        name = feature['properties']['COUNTRYAFF']
        if code in countryMcc:
            mcc = str(countryMcc[code])
            geo = "ST_SetSRID(ST_Buffer(ST_GeomFromGeoJSON('" + json.dumps(feature['geometry']) + "'), 1), 4326)"
            queries.append("INSERT INTO countries (code, name, mcc, geo) VALUES ('" + code + "', '" + name + "', " + mcc + ", " + geo + ");")
    print('Total: ' + str(len(queries)) + ' queries')
    # print runtime
    print("Load time: " + str(time.time() - start))

def insertToDb(queries):
    conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " host=" + dbhost + " password=" + dbpassword + " port=" + dbport)
    cur = conn.cursor()
    query = 0
    for q in queries:
        # print percentual progress to console
        if query % 1000 == 0:
            writePercentualProgress(query, len(queries))
        cur.execute(q)
        query += 1
    writePercentualProgress(len(queries), len(queries))
    cur.close()
    conn.commit()

def writePercentualProgress(actual, total):
    if actual == 0:
        sys.stdout.write('\r')
    else:
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('='*int(actual/total*100), int(actual/total*100)))
        sys.stdout.flush()

if __name__ == '__main__':
    main()







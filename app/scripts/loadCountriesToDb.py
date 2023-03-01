import psycopg2
import time
import sys
import json

dbuser = "postgres"
dbpassword = "test"
dbhost = "192.168.0.30"
dbport = "5432"
dbname = "postgres"
# Tweaks
clean_db = True
border_file = 'world_countries.geojson'
mccmnc_file = 'mcc-mnc-table.json'
border_enlargement = 0.1

# store time to measure performance
start = time.time()

# Global variables
queries = []
countryCodeToMcc = {}
# dict with country code as key and list of mncs as value
countryOperators = {}

def main():
    prepareDb()
    getMccMncFromFile()
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
        cur.execute("DROP TABLE IF EXISTS operators;")
        cur.execute("DROP INDEX IF EXISTS countries_mcc_idx;")
    # Prepare countries table
    cur.execute("CREATE TABLE IF NOT EXISTS countries (code varchar(4), name varchar(40), mcc integer, geo geography);")
    cur.execute("CREATE INDEX IF NOT EXISTS countries_geo_gist ON countries USING GIST (geo);")
    cur.execute("CREATE INDEX IF NOT EXISTS countries_mcc_idx ON countries (mcc);")
    # Prepare operators table
    cur.execute("CREATE TABLE IF NOT EXISTS operators (mcc integer, mnc integer, country_code varchar(10), name varchar(80));")
    cur.close()
    conn.commit()

def getMccMncFromFile():
    global countryCodeToMcc
    print("Reading mccmnc from file")
    with open(mccmnc_file) as f:
        data = json.load(f)
        # create dict with country code as key and mcc and list of mncs as value
        for o in data:
            countryCodeToMcc[o['countryCode']] = o['mcc']
            # Operators list 
            # skip if there is no operator name, mcc or mnc or if mnc is '?'
            if 'operator' not in o or 'mcc' not in o or 'mnc' not in o or o['mnc'] == '?':
                continue
            operatorObject = {
                'mcc': o['mcc'],
                'mnc': o['mnc'],
                'countryCode': o['countryCode'],
                'name': o['operator'],
                'bands': o['bands']
            }
            if o['countryCode'] in countryOperators:
                countryOperators[o['countryCode']].append(operatorObject)
            else:
                countryOperators[o['countryCode']] = [operatorObject]
    print('Loaded ' + str(len(countryCodeToMcc)) + ' country codes and mccs')
    # Prepare queries to insert operators
    for country in countryOperators:
        for operator in countryOperators[country]:
            queries.append("INSERT INTO operators (mcc, mnc, country_code, name) VALUES (" + str(operator['mcc']) + ", " + str(operator['mnc']) + ", '" + str(operator['countryCode']) + "', '" + str(operator['name']) + "');")


def getCountriesFromFile():
    global queries
    print("Reading countries from file")
    # import with geoJSON
    with open(border_file) as f:
        data = json.load(f)
        #print length of features
        for feature in data['features']:
            code = feature['properties']['ISO']
            name = feature['properties']['COUNTRYAFF']
            if code in countryCodeToMcc:
                mcc = str(countryCodeToMcc[code])
                geo = "ST_SetSRID(ST_Buffer(ST_GeomFromGeoJSON('" + json.dumps(feature['geometry']) + "'), " + border_enlargement + "), 4326)"
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







# Except DB connecttion, nothing needs to be changed here
# This script is used to generate signal grid for all countries that's cell towers are loaded in the database


import psycopg2
import time
import sys
import chevron
import query_templates
from multiprocessing import Pool

dbuser = "postgres"
dbpassword = "test"
dbhost = "192.168.0.30"
dbport = "5432"
dbname = "postgres"

# Tweaks
clean_db = False

# store time to measure performance
start = time.time()

# queries
queries = []
def main():
    prepareDb()
    mccs = getLoadedCountries()
    createQueriesForCountries(mccs)
    print("Number of queries: " + str(len(queries)))
    # run everything in sequence
    insertToDb(queries)
    print("\nRun time: " + str(time.time() - start))
    

def prepareDb():
    # connect to postgres
    conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " host=" + dbhost + " password=" + dbpassword + " port=" + dbport )
    # disable autocommit
    conn.autocommit = False
    # create a cursor
    cur = conn.cursor()
    # drop table if exists
    if clean_db:
        cur.execute("DROP TABLE IF EXISTS signal_grid;")
        cur.execute("DROP INDEX IF EXISTS signal_grid_mcc_idx;")
    cur.execute("CREATE TABLE IF NOT EXISTS signal_grid (id SERIAL, radio_total integer, radio_gsm integer, radio_lte integer, radio_umts integer, countryCode varchar(10), mcc integer, geojson varchar, geom geography(Polygon), PRIMARY KEY (id, mcc));")
    cur.execute("CREATE INDEX IF NOT EXISTS signal_grid_mcc_idx ON signal_grid (mcc);")
    cur.close()
    conn.commit()

def getLoadedCountries():
    global mcc_starts_with
    conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " host=" + dbhost + " password=" + dbpassword + " port=" + dbport)
    cur = conn.cursor()
    cur.execute(chevron.render(query_templates.getLoadedCountriesCellTowers, {}))
    mccs = cur.fetchall()
    cur.close()
    conn.commit()
    return [mcc[0] for mcc in mccs]

def createQueriesForCountries(mcc_list):
    global queries
    # load cells from csv to database
    for mcc in mcc_list:
        a = { 'mcc': mcc }
        queries.append(chevron.render(query_templates.generateCountrySignalGrid, a).encode('utf-8'))
        sys.stdout.write(str(mcc) + ' ')
        sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.flush()
    print('Total: ' + str(len(queries)) + ' cells')
    # print runtime
    print("Load time: " + str(time.time() - start))


def insertToDb(queries):
    conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " host=" + dbhost + " password=" + dbpassword + " port=" + dbport)
    cur = conn.cursor()
    query = 0
    for q in queries:
        query += 1
        cur.execute(q)
        writePercentualProgress(query, len(queries))
    cur.close()
    conn.commit()

def writePercentualProgress(actual, total):
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*int(actual/total*100), int(actual/total*100)))
    sys.stdout.flush()

if __name__ == '__main__':
    main()

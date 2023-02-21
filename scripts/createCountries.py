import psycopg2
import csv
import time
import sys
import countries

dbuser = "postgres"
dbpassword = "test"
dbhost = "localhost"
dbport = "5432"
dbname = "postgres"
# Tweaks
clean_db = True

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
    cur.execute("CREATE TABLE IF NOT EXISTS countries (code varchar(2) PRIMARY KEY, name varchar(40), mcc integer, geo geography(Polygon));")
    cur.execute("CREATE INDEX IF NOT EXISTS countries_geo_gist ON countries USING GIST (geo);")
    cur.close()
    conn.commit()




def getCountriesFromFile():
    global queries
    # load cells from countries to array
    print("Reading countries from file")
    for country in countries.country_bounding_boxes:
        code = country
        name = countries.country_bounding_boxes[country][0]
        if code in countries.countryMcc:
            mcc = str(countries.countryMcc[country])
            geo = "ST_MakeEnvelope(" + str(countries.country_bounding_boxes[country][1][0]) + ", " + str(countries.country_bounding_boxes[country][1][1]) + ", " + str(countries.country_bounding_boxes[country][1][2]) + ", " + str(countries.country_bounding_boxes[country][1][3]) + ", 4326)"
            queries.append("INSERT INTO countries (code, name, mcc, geo) VALUES ('" + code + "', '" + name + "', " + mcc + ", " + geo + ");")
    print('Total: ' + str(len(queries)) + ' cells')
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







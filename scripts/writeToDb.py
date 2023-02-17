import psycopg2
import csv
import time
import sys


dbuser = "postgres"
dbpassword = "test"
dbhost = "localhost"
dbport = "5432"
dbname = "postgres"
# Tweaks
max_4g_range = 7000
max_3g_range = 40000
max_2g_range = 40000
max_age_timestamp = 1514761200 # 2018 01 01 00:00:00
mcc_starts_with = ('2')
clean_db = True

# CSV file
csv_files = ['../MLS-full-cell-export-2023-02-15T000000.csv']

# store time to measure performance
start = time.time()

# pool = multiprocessing.Pool(2)


# queries
queries = []
def main():
    print("Main")
    prepareDb()
    getCellsFromCsv()
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
        cur.execute("DROP TABLE IF EXISTS cell_towers;")
        cur.execute("DROP INDEX IF EXISTS cell_towers_geo_gist;")
    cur.execute("CREATE TABLE IF NOT EXISTS cell_towers (cellid integer PRIMARY KEY, mcc integer, radio varchar(10), net smallint, range integer, samples integer, changable boolean, created timestamp, updated timestamp, geo geography(Polygon));")
    cur.execute("CREATE INDEX IF NOT EXISTS cell_towers_geo_gist ON cell_towers USING GIST (geo);")
    cur.close()
    conn.commit()

def getCellsFromCsv():
    global queries
    # load cells from csv to database
    for csv_file in csv_files:
        print("Reading cells from csv file: " + csv_file)
        with open(csv_file, 'r') as f:
            counter = 0
            reader = csv.reader(f)
            next(reader) # Skip the header row.
            for row in reader:
                # Filter by mcc
                if not (row[1].startswith(mcc_starts_with)):
                    continue
                # Filter by age
                if int(row[12]) < max_age_timestamp:
                    continue
                range = rangeNormalizer(row[8], row[0])
                queries.append("INSERT INTO cell_towers (cellid, mcc, radio, net, range, samples, changable, created, updated, geo) VALUES (%s, %s, '%s', %s, %s, %s, %s, to_timestamp(%s), to_timestamp(%s),ST_Buffer(ST_MakePoint(%s, %s)::geography, %s)) ON CONFLICT (cellid) DO NOTHING;" % (row[4], int(row[1]), row[0], int(row[2]), int(range),int(row[9]), bool(row[10]), int(row[11]), int(row[12]), float(row[6]), float(row[7]), float(range)))
                counter += 1
                # if counter % 1000 == 0:
                sys.stdout.write('\r')
                sys.stdout.write("Processed " + str(counter) + " cells")
                sys.stdout.flush()
        sys.stdout.write('\n')
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
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*int(actual/total*100), int(actual/total*100)))
    sys.stdout.flush()

def rangeNormalizer(range, radio):
    intRange = int(range)
    if radio == 'GSM' and intRange > max_2g_range:
        intRange = max_2g_range
    if radio == 'UMTS' and intRange > max_3g_range:
        intRange = max_3g_range
    if radio == 'LTE' and intRange > max_4g_range:
        intRange = max_4g_range
    return intRange

if __name__ == '__main__':
    main()







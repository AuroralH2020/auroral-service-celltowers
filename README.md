### Cell towers mapper

## DB + PgAdmin
- everything is defined in docker-compose.yml
- run `docker-compose up -d` to start all services
- Services:
    - Postgres: 
        - db name: `postgres`
        - credentials: `postgres:test`
        - port: `5432`
    - PgAdmin:
        - credentials: `test@bavenir.eu:test`
        - port: `5050`

## Python scripts
-   Create virtual environment
    - `python3 -m venv venv`
-   Activate virtual environment
    - `source venv/bin/activate`
-   Install requirements
    - `pip install -r requirements.txt`
-   Run script
### Scripts description
- loadCsvToDb.sh - script for writing data to database
    - everything is hardcoded in first lines of script
    - script defines some filtering rules
- loadCountriesToDb.py - script for writing countries to database
    - everything is hardcoded in first lines of script - you can choose which countries you want to load


## CSV
### Where to get data
- OpenCellId: https://opencellid.org/downloads ( requires registration)
- Mozilla Location Service: https://location.services.mozilla.com/downloads (free)
### Data format descrtiption
| Parameter | Description |
|:----------:|:-----------:|
| radio| Network type. One of the strings GSM, UMTS, LTE or CDMA.|
|mcc| Mobile Country Code (UK: 234, 235)|
|net| Mobile Network Code (MNC)|
|area|Location Area Code (LAC) for GSM and UMTS networks. Tracking Area Code (TAC) for LTE networks. Network IDenfitication number (NID) for CDMA networks |
|cell|Cell ID|
|unit| Primary Scrambling Code (PSC) for UMTS networks. Physical Cell ID (PCI) for LTE networks. An empty value for GSM and CDMA networks|
|lon|Longitude in degrees between -180.0 and 180.0 <br> If changeable=1: average of longitude values of all related measurements. <br> If changeable=0: exact GPS position of the cell tower|
|lat| Latitude in degrees between -90.0 and 90.0 <br> If changeable=1: average of latitude values of all related measurements. <br> If changeable=0: exact GPS position of the tower|
|range| Estimate of cell range, in meters.
|samples|Total number of measurements assigned to the cell tower
|changeable| Defines if coordinates of the cell tower are exact or approximate.|
|created| The first time when the cell tower was seen and added to the OpenCellID database.|
|updated|The last time when the cell tower was seen and update.|
|averageSignal| Average signal strength from all assigned measurements for the cell.|

> **Note:** Source: https://github.com/ONSBigData/OpencellID-analysis/blob/master/README.md
### Interesting MCC Codes 
| Country | MCC |
|:-------:|:---:|
| Slovakia | 231 |
| Czech Republic | 230 |
| Austria | 232 |
| Hungary | 216 |
| Norway | 242 |
| Sweden | 240 |
| Finland | 244 |
| Denmark | 238 |
| Netherlands | 204 |
| Belgium | 206 |
| Luxembourg | 270 |
| Portugal | 268 |
| Poland | 260 |
| Germany | 262 |
| Greece | 202 |
| Italy | 222 |
| Spain | 214 |
| France | 208 |
| United Kingdom | 234 |




## Interesting apps
- QGIS: https://www.qgis.org/en/site/


## Starting the dev server

```uvicorn app.main:app --reload```
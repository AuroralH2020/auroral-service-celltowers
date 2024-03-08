# Cell towers mapper

1. How to run the service
2. How to integrate with AURORAL

## 1. Running the service
### DB + PgAdmin
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

### Python scripts
-   Create virtual environment
    - `python3 -m venv venv`
-   Activate virtual environment
    - `source venv/bin/activate`
-   Install requirements
    - `pip install -r requirements.txt`
-   Run script
  
#### Scripts description
- loadCsvToDb.sh - script for writing data to database
    - everything is hardcoded in first lines of script
    - script defines some filtering rules
- loadCountriesToDb.py - script for writing countries to database
    - everything is hardcoded in first lines of script - you can choose which countries you want to load

### CSV
#### Where to get data
- OpenCellId: https://opencellid.org/downloads ( requires registration)
- Mozilla Location Service: https://location.services.mozilla.com/downloads (free)
  
#### Data format descrtiption
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

#### Interesting MCC Codes 
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

### Interesting apps
- QGIS: https://www.qgis.org/en/site/

## Starting the dev server

```uvicorn app.main:app --reload```

## 2. Integration with AURORAL

1. Installing the AURORAL Node
https://auroral.docs.bavenir.eu/getting_started/install_node/

2. Register using the Thing description

Assumes that your service is running in the localhost of the same machine as the AURORAL Node using the port 8002. This can be updated according to user preferences.
The metadata fields can also be updated.

Post the following to the node, using the /api/registration endpoint

```json
{
    {
  "adapterId": "some-adapter",
  "applicableGeographicalArea": "Europe",
  "currentStatus": "Available",
  "securityDefinitions": {
    "nosec_sc": {
      "scheme": "nosec"
    }
  },
  "description": "Cell tower data service",
  "hasDomain": "Mobility",
  "hasFuncionality": [
    "Maps/Geolocation",
    "Only read"
  ],
  "properties": {
    "gettowers": {
      "UriVariables": {
        "type": "array",
        "readOnly": true,
        "uriVariables": {
          "lon": {
            "type": "number",
            "description": "GPS Longitude I.e. 17.10674"
          },
          "lat": {
            "type": "number",
            "description": "GPS Latitude. I.e. 48.14816"
          }
        },
        "title": "Get towers"
      },
      "items": {
        "type": [
          "object",
          "https://auroral.iot.linkeddata.es/def/cell#CellTowers"
        ]
      },
      "readOnly": true,
      "description": "Returns 5 closest cell towers based on user's location [?lat,lon]",
      "forms": [
        {
          "op": "readproperty",
          "href": "http://node-red:1250/api/property/7ea723f7-9298-442e-be24-7888a1ffba9b/gettowers"
        }
      ]
    }
  },
  "hasRequirement": "Latitude and longitude",
  "hasSubDomain": "Coverage",
  "hasURL": "https://maps.jupiter.bavenir.eu",
  "language": "eng",
  "place": "Slovakia",
  "provider": "bAvenir",
  "serviceFree": true,
  "title": "Demo Cell Towers Service",
  "@context": [
    "https://www.w3.org/2019/wot/td/v1"
  ],
  "security": [
    "nosec_sc"
  ],
  "@type": [
    "Service"
  ]
}
```

3. More info about registering services
https://auroral.docs.bavenir.eu/getting_started/start_using_auroral/service_provider/


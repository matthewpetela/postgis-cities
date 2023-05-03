# postgis-cities
Import City Database from Geonames into Postgresql/PostGIS

1. Download city database from [Geonames](https://download.geonames.org/export/dump/). Use one of the citiesx00.zip (cities15000.zip, cities5000.zip, etc).

2. ``` pip install sqlalchemy psycopg2-binary geoalchemy2 ```

3. Copy auth.json.sample to auth.json

4. Add DATABASE_URI

5. ``` python main.py ```

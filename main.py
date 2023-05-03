import csv
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

Base = declarative_base()

# Define the geoname model
class Geoname(Base):
    __tablename__ = 'geonames'

    geonameid = Column(Integer, primary_key=True)
    name = Column(String(200))
    asciiname = Column(String(200))
    alternatenames = Column(String(10000))
    latitude = Column(Float)
    longitude = Column(Float)
    geom = Column(Geometry('POINT'))
    feature_class = Column(String(1))
    feature_code = Column(String(10))
    country_code = Column(String(2))
    country_name = Column(String(200))
    cc2 = Column(String(200))
    admin1_code = Column(String(20))
    admin2_code = Column(String(80))
    admin3_code = Column(String(20))
    admin4_code = Column(String(20))
    population = Column(Integer)
    elevation = Column(Integer)
    dem = Column(Integer)
    timezone = Column(String(40))
    modification_date = Column(Date)

# Load the database URI from the auth.json file
with open("auth.json") as f:
    auth = json.load(f)
    DATABASE_URI = auth["DATABASE_URI"]

country_code_to_name = {}

# Replace 'all.csv' with the path to your country codes CSV file
with open('all.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        country_code_to_name[row[1]] = row[0]


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Replace 'cities15000.txt' with the path to your tab-delimited file
with open('cities15000.txt', 'r', encoding='utf-8') as tsv_file:
    tsv_reader = csv.reader(tsv_file, delimiter='\t')
    for row in tsv_reader:
        geoname = Geoname(
            geonameid=int(row[0]),
            name=row[1],
            asciiname=row[2],
            alternatenames=row[3],
            latitude=float(row[4]),
            longitude=float(row[5]),
            geom=f'SRID=4326;POINT({float(row[5])} {float(row[4])})',
            feature_class=row[6],
            feature_code=row[7],
            country_code=row[8],
            country_name=country_code_to_name.get(row[8], ''),
            cc2=row[9],
            admin1_code=row[10],
            admin2_code=row[11],
            admin3_code=row[12],
            admin4_code=row[13],
            population=int(row[14]) if row[14] else None,
            elevation=int(row[15]) if row[15] else None,
            dem=int(row[16]) if row[16] else None,
            timezone=row[17],
            modification_date=row[18]
        )
        session.add(geoname)

    session.commit()

print("Data imported successfully.")

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base 
from sqlalchemy.orm import sessionmaker

print ("Initing models.")

POSTGRES_USER=os.environ.get('POSTGRES_USER', 'wishmaster')
POSTGRES_PW=os.environ.get('POSTGRES_PW', 'dbpw')
POSTGRES_URL=os.environ.get('POSTGRES_URL', '0.0.0.0:5432')
POSTGRES_DB=os.environ.get('POSTGRES_DB', 'bucketlist')
DB_URL = 'postgresql+psycopg2://{user}:{password}@{url}/{db}'.format(user=POSTGRES_USER, password=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

Base = declarative_base()
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, Float,
                        create_engine)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI') or 'postgresql://postgres:@localhost/route'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

points = Table(
    'points',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(200)),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
)

database = Database(DATABASE_URI)

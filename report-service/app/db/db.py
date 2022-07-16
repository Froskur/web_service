import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, Float,
                        create_engine)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI') or 'postgresql://postgres:@localhost/route'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

database = Database(DATABASE_URI)

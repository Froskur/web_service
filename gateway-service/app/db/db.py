# Коннект к базе и сами таблицы

import os
from databases import Database
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, Float,
                        create_engine)


DATABASE_URI = os.getenv('DATABASE_URI') or 'postgresql://postgres:@localhost/route'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

user = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200), nullable=False),
    Column('hashed_password', String(1024)),
    Column('token', String(1024)),
    Column('last_login', DateTime),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
)

database = Database(DATABASE_URI)

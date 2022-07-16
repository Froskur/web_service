import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, Float,
                        create_engine, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

from databases import Database
from datetime import datetime

Base = declarative_base()


DATABASE_URI = os.getenv('DATABASE_URI') or 'postgresql://postgres:@localhost/route'

engine = create_engine(DATABASE_URI)
metadata = MetaData()


#tags=db.relationship('Tag', secondary=tags, lazy='subquery',
#                         backref=db.backref('pages', lazy=True))

# Определим таблицу пользователей, чтобы при добавлении маршрута не было "сюрпризов"
user = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(200), nullable=False),
)

# Сама таблица маршрутов
routes = Table(
    'routes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(200)),
    Column('author_id', ForeignKey(user.c.id)),
    Column('short_num', Integer),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
    #Column('created_at', DateTime, default=datetime.now),
    #Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now)
)


# Модель точки тоже тут нужна
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


# Пропишем отдельно крос табличку, вдруг она нам понадобиться
routes_points = Table(
    'routes_has_points',
    metadata,
    Column('route_id', ForeignKey(routes.c.id)),
    Column('point_id', ForeignKey(points.c.id)),
    Column('ord', Integer),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
)

"""


class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    author_id = Column(Integer(), nullable=False)
    short_num = Column(Integer(), nullable=False, default=10),
    created_at = Column(DateTime(), )
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


"""
"""
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)
"""
"""

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

"""

database = Database(DATABASE_URI)

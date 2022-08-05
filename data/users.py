import datetime

import sqlalchemy

from setup import texts
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    format = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # 1 — онлайн, 2 — офилайн 12 — все
    sphere = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    skills = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    achievements = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    experience = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    requirements = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<User {self.id} {self.username} {self.name}>'

    def get_spheres(self):
        return str(self.sphere).split(', ')

    def get_str_spheres(self):
        sph = self.get_spheres()
        print(sph)
        res = map(lambda x: texts["sphere_" + x], sph)
        return ', '.join(res)


class Association(SqlAlchemyBase):
    __tablename__ = 'association'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    u1_id = sqlalchemy.Column(sqlalchemy.Integer)
    u2_id = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def __repr__(self):
        return f'<Association {self.id} {self.u1_id} {self.u2_id} {self.status}>'

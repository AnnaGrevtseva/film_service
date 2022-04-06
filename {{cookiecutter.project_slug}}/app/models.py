"""Module for model database"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'sqlite:///Users.db'
engine = sa.create_engine(DB_URL, connect_args={'check_same_thread': False})
Base = declarative_base()


# pylint: disable=too-few-public-methods
class CommentUsers(Base):
    """Table with comment users and grade"""

    __tablename__ = 'Comments'
    comment_id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column('login', sa.String)
    title = sa.Column('Title', sa.String)
    grade = sa.Column('Grade', sa.Integer)
    comment = sa.Column('Comment', sa.String)


# pylint: disable=too-few-public-methods
class UserDB(Base):
    """Table with users"""

    __tablename__ = 'Users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String)
    password = sa.Column(sa.Integer)


# pylint: disable=too-few-public-methods
class FilmDB(Base):
    """Table with films"""

    __tablename__ = 'Films'
    film_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    release_year = sa.Column(sa.String)
    medium_grade = sa.Column(sa.Float)
    count_grade = sa.Column(sa.Integer)
    count_comment = sa.Column(sa.Integer)

"""Module for create and get data"""

from app import models
from app import shemas
from sqlalchemy.orm import sessionmaker


local_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=models.engine)


def get_user_login(d_b: local_session, login: str):
    """Get user login"""

    return d_b.query(models.UserDB).filter(
        models.UserDB.login == login).first()


def get_film(d_b: local_session, title: str):
    """Get film"""

    return d_b.query(models.FilmDB).filter(
        models.FilmDB.title == title).first()


def get_medium_grade(d_b: local_session, title: str):
    """Get medium grade"""

    d_b_grade = d_b.query(models.CommentUsers.grade).\
        filter(models.CommentUsers.title == title).all()

    grade_list = [d['grade'] for d in d_b_grade]
    return sum(grade_list)/len(grade_list), len(grade_list)


def get_user(d_b: local_session, login: str, password: int):
    """Get user"""

    return d_b.query(models.UserDB).filter(
        models.UserDB.login == login,
        models.UserDB.password == password).first()


def create_user(d_b: local_session, user: shemas.User):
    """Create user"""

    d_b_user = models.UserDB(login=user.login, password=hash(user.password))
    d_b.add(d_b_user)
    d_b.commit()
    d_b.refresh(d_b_user)
    return d_b_user


def create_film(d_b: local_session, film: shemas.Film):
    """Create film"""

    d_b_film = models.FilmDB(
        title=film.title,
        release_year=film.release_year,
        medium_grade=0.,
        count_grade=0,
        count_comment=0)

    d_b.add(d_b_film)
    d_b.commit()
    d_b.refresh(d_b_film)
    return d_b_film


def create_comment(d_b: local_session, login: str, comment: shemas.Comment):
    """Create comment"""

    d_b_comment = models.CommentUsers(
        login=login, title=comment.title,
        grade=comment.grade, comment=comment.comment)
    d_b.add(d_b_comment)
    d_b.commit()
    d_b.refresh(d_b_comment)
    return d_b_comment

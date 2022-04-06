"""Module for schemas database"""

# pylint: disable=no-name-in-module
from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class User(BaseModel):
    """User model"""

    login: str
    password: str

    class Config:
        """Config"""

        orm_mode = True


# pylint: disable=too-few-public-methods
class Film(BaseModel):
    """Film model"""

    title: str
    release_year: str
    medium_grade: float = 0.
    count_grade: int = 0
    count_comment: int = 0

    class Config:
        """Config"""

        orm_mode = True


# pylint: disable=too-few-public-methods
class Comment(BaseModel):
    """Comment model class"""

    title: str
    grade: int
    comment: str

    class Config:
        """Config"""

        orm_mode = True

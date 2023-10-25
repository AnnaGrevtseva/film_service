"""Module for routes"""

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app import models
from app import crud
from app import shemas
from app.models import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


# pylint: disable=too-few-public-methods
class CurrentUser:
    """Current user status"""

    login: str = ''
    password: int = 0
    is_auth: bool = False


current_user = CurrentUser()


def get_db():
    """Get database"""

    d_b = crud.local_session()
    try:
        yield d_b
    finally:
        d_b.close()


def check_auth():
    """Check authorization"""

    if not current_user.is_auth:
        raise HTTPException(status_code=403, detail='UNAUTHORIZED')


@app.get('/')
async def read_current_user():
    """Start route"""

    return 'Users'


@app.post('/add-user/', response_model=shemas.User)
async def create_user(user: shemas.User, d_b: Session = Depends(get_db)):
    """ Create user"""

    user_login = crud.get_user_login(d_b, user.login)
    if user_login is not None:
        raise HTTPException(status_code=409, detail='User exists')
    return crud.create_user(d_b=d_b, user=user)


@app.post('/add-comment/', response_model=shemas.Comment)
async def create_comment(
        comment: shemas.Comment,
        d_b: Session = Depends(get_db)):
    """Create comment, grade"""

    check_auth()
    film = crud.get_film(d_b, comment.title)
    if film is None:
        raise HTTPException(status_code=404, detail='Not found film')
    if comment.grade > 10 or comment.grade < 0:
        raise Exception('Grade out of range from 0 to 10')

    sum_old = film.medium_grade * film.count_grade
    sum_new = sum_old + comment.grade

    film.count_grade = film.count_grade + 1
    film.medium_grade = sum_new / film.count_grade

    if comment.comment:
        film.count_comment = film.count_comment + 1

    d_b.commit()
    d_b.refresh(film)

    return crud.create_comment(
        d_b=d_b,
        login=current_user.login,
        comment=comment)


@app.post('/add-film/',  response_model=shemas.Film)
async def create_film(film: shemas.Film, d_b: Session = Depends(get_db)):
    """Add film in database"""

    return crud.create_film(d_b=d_b, film=film)


@app.post('/add-grade-count/')
async def add_grade(title: str, d_b: Session = Depends(get_db)):
    """Add grade"""

    film = crud.get_film(d_b, title)
    if film is None:
        raise HTTPException(status_code=404, detail='Not found film')
    db_grade = crud.get_medium_grade(d_b, title=title)
    film.medium_grade = db_grade[0]
    film.count_grade = db_grade[1]
    return film


@app.get('/get-medium-grade/')
async def get_medium_grade(title: str, d_b: Session = Depends(get_db)):
    """Get medium grade"""

    film = crud.get_film(d_b, title)
    if film is None:
        raise HTTPException(status_code=404, detail='Not found film')

    return crud.get_medium_grade(d_b, title=title)


@app.get('/get-user/', response_model=shemas.User)
async def get_user(login: str, d_b: Session = Depends(get_db)):
    """Get user"""

    db_user = crud.get_user_login(d_b, login=login)
    if db_user is None:
        return HTTPException(status_code=404, detail='User not found')
    return db_user


@app.get('/auth/')
async def login_basic(
        d_b: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)):
    """Authorization function"""

    hash_password = hash(credentials.password)

    db_user = crud.get_user(d_b, credentials.username, hash_password)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Basic'},
        )

    current_user.login = credentials.username
    current_user.password = hash_password
    current_user.is_auth = True

    return 'OK'

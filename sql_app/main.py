from fastapi import Depends, FastAPI, HTTPException
from sql_app.crud import get_user_by_email, get_users, get_user, create_user_item, get_items, create_user
from sql_app.schemas import User
from sql_app.schemas import UserCreate, ItemCreate, Item
from database import get_session

app = FastAPI()


# Dependency
@app.get("/")
def read_root():
    """ chạy lần đầu khi thực hiện vào trang chủ """
    return {"message": "welcome to FastAPI!"}


@app.post("/users/", response_model=User)

def create_user_method(user: UserCreate, db=Depends(get_session)):
    #""" add new values  in database use """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100,  db=Depends(get_session)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user_method(user_id: int,  db=Depends(get_session)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate,  db=Depends(get_session)
):
    return create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100,  db=Depends(get_session)):
    items = get_items(db, skip=skip, limit=limit)
    return items

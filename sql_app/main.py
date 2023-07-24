from authenticate.Schemas import UserInDB, TokenData
from sql_app.crud import get_user_by_email, get_users, get_user, create_user_item, get_items, create_user
from sql_app.schemas import User
from sql_app.schemas import UserCreate, ItemCreate, Item
from database import get_session
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
app = FastAPI()
"""Authenticate  key"""
SECRET_KEY="60bcf16729cfdfa7587365cf8ff11e2e8c2a89d25f0b83e57d0f719c5baf711e"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Dependency
@app.get("/")
def read_root():
    """ chạy lần đầu khi thực hiện vào trang chủ """
    return {"message": "welcome to FastAPI!"}
# kiểm tra mật khẩu

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# mã hóa mật khẩu với dạng hash

def get_password_hash(password):
    return pwd_context.hash(password)

# kiểm tra tài trong database
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# dùng 0authen2 để check thông tin
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# tạo token liên kết với việc hoạt động của tài khoản
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# đồng bộ hóa giữa token và user để thao tác trong quá trình tham gia trang

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(get_users(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
# kiểm tra và đưa ra các thông tin nếu có vài thông tin bị lỗi hoặc không có quyền truy cập
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
#api kiểm thử
@app.post("/token", response_model=User, tags=["posts"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(get_user(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# thông tin đã nhập
@app.get("/users/me/", response_model=User, tags=["user"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
#
@app.get("/users/me/items/", tags=["user"])
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

#add value
@app.post("/users/", response_model=User, tags=["user"])
def create_user_method(user: UserCreate, db=Depends(get_session)):
    #""" add new values  in database use """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
#put value
@app.get("/users/", response_model=list[User],  tags=["user"])
def read_users(skip: int = 0, limit: int = 100,  db=Depends(get_session)):
    users = get_users(db, skip=skip, limit=limit)
    return users

#read value
@app.get("/users/{user_id}", response_model=User, tags=["user"])
def read_user_method(user_id: int,  db=Depends(get_session)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# add value to users/{id}/items
@app.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate,  db=Depends(get_session)
):
    return create_user_item(db=db, item=item, user_id=user_id)

# print data on this item to display for Json
@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100,  db=Depends(get_session)):
    items = get_items(db, skip=skip, limit=limit)
    return items
#send email

@app.post("/send-email")
async def send_email(email_data: dict):
    # Extract email parameters from the request
    recipient = email_data.get("chiulinhphat@gmail.com")
    subject = email_data.get("subject")
    message = email_data.get("hello world")

    # Configure SMTP settings
    smtp_server = "chiulinhphat@gmail.com"
    smtp_port =  587
    sender_email = "chiulinhphat@gmail.com"
    password = "Chiu_linh2"

    # Create the email
    email = MIMEText(message)
    email["Subject"] = subject
    email["From"] = sender_email
    email["To"] = recipient

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, email.as_string())

    return {"message": "Email sent successfully"}
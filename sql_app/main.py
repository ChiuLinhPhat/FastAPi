from fastapi import Depends, FastAPI, HTTPException
from sql_app.crud import get_user_by_email, get_users, get_user, create_user_item, get_items, create_user
from sql_app.schemas import User
from sql_app.schemas import UserCreate, ItemCreate, Item
from database import get_session
import smtplib
from email.mime.text import MIMEText

app = FastAPI()


# Dependency
@app.get("/")
def read_root():
    """ chạy lần đầu khi thực hiện vào trang chủ """
    return {"message": "welcome to FastAPI!"}

#add value
@app.post("/users/", response_model=User)
def create_user_method(user: UserCreate, db=Depends(get_session)):
    #""" add new values  in database use """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
#put value
@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100,  db=Depends(get_session)):
    users = get_users(db, skip=skip, limit=limit)
    return users

#read value
@app.get("/users/{user_id}", response_model=User)
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
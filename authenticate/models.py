from authenticate.database import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String

Accounts = Table(
    'Passenger',meta,
    Column('username',String(255),primary_key=True),
    Column('Passwords',String(255)),
    Column('HashPasswords',String(2000)),
    Column('Email',String(255)),
    Column('Phone',String(255)),
)
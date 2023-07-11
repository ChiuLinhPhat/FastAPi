"""
Add example scheams
"""
from pydantic import BaseModel
class Account(BaseModel):
    account: str
    password:str
    emailAccount: str
    phoneAccount: str
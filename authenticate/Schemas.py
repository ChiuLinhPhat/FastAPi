"""
Add example scheams
"""
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# # change value find str to hash with formal
# import hashlib
#
# def create_hash(text):
#     # Khởi tạo đối tượng hasher với thuật toán SHA-256
#     hasher = hashlib.sha256()
#
#     # Chuyển đổi văn bản sang dạng byte trước khi mã hóa
#     text = text.encode('utf-8')
#
#     # Cung cấp dữ liệu cho hasher
#     hasher.update(text)
#
#     # Lấy mã hash dưới dạng hexdigest
#     hash_value = hasher.hexdigest()
#
#     return hash_value
#
# # Ví dụ sử dụng
# text = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
# hash_value = create_hash(text)
# print(type(text))
# print("Mã hash của văn bản là:", hash_value)
# To build  a bcrypt hash
# import bcrypt
#
# password = "passwords"
#
# # Generate a bcrypt hash with a cost factor of 12
# bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
#
# print("Bcrypt hash:", bcrypt_hash.decode('utf-8'))

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sq2.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
url = 'mysql+pymysql://root@127.0.0.1:3306/test'
Base = declarative_base()
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""  khỏi tạo cà chạy post trên một obj """


def get_session():
    """tạo một post treo khi thực hiện ban đầu nếu khi tắt sẽ tử đống post """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# tạo bảng và khái báo chạy các khai báo bảng trong engine
def create_tables():
    from models import User
    from models import Item
    from models import Email
    Base.metadata.create_all(engine)

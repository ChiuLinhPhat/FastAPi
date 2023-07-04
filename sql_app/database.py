from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sq2.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
url = 'mysql+pymysql://root@127.0.0.1:8080/serversiderendering'
Base = declarative_base()
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_session():
    """tạo một post treo khi thực hiện ban đầu nếu khi tắt sẽ tử đống post """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables():
# tạo bảng và khái báo chạy các khai báo bảng trong engine
    from models import User
    from models import Item
    Base.metadata.create_all(engine)

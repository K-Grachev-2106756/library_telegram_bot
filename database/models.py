from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import getpass



USERNAME = getpass.getuser()
PORT = 5433

connection_string = f"postgresql+psycopg2://{USERNAME}:@localhost:{PORT}"
engine = create_engine(connection_string)
Session = sessionmaker(engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(DateTime, nullable=False)
    date_deleted = Column(DateTime, nullable = True)

class Borrow(Base):
    __tablename__ = 'borrows'
    
    borrow_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=True)
    user_id = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
